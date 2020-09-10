from google.cloud import texttospeech
import librosa
import math
import cv2
from PIL import ImageFont, ImageDraw, Image
from moviepy.editor import *
import os


def getScripts(fps=20, scriptName='resources/scripts.txt'):
    """ 内容 开始时间（距离 0 的帧数） 持续时间（帧数）

    :param fps:
    :param scriptName:
    :return:
    """
    scripts = []
    with open(scriptName, "r", encoding='utf-8') as file:
        for script in file.readlines():
            if script != '\n' and script[0] != ' ' and script[0] != '#':
                info = script.strip("\n")
                scripts.append([info[5:], (int(info[0:2])*60+int(info[2:4]))*fps, 0])
    print('字幕读取完成')
    return scripts


def getAudios(scripts, position=0, errorTimes=0, outputPath='audios'):
    """ 获取所有音频

    获取失败就重新访问，直到重新访问次数达到脚本长度

    :param scripts:
    :param outputPath:
    :return:
    """
    print('本轮从音频 %d 开始获取' % position)
    for index, script in enumerate(scripts):
        if index < position:
            continue
        try:
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=script[0])
            voice = texttospeech.VoiceSelectionParams(
                language_code="cmn-CN", name="cmn-CN-Wavenet-A", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            with open(os.path.join(outputPath, str(index)+'.mp3'), "wb") as out:
                out.write(response.audio_content)
            print('音频 %d 获取完成' % index)
        except:
            errorTimes += 1
            if errorTimes < len(scripts):
                print('音频 %d 获取失败，八成是网络不佳，尝试重新获取' % index)
                getAudios(scripts, index, errorTimes)
                break
            else:
                print('音频 %d 获取失败，已达最大尝试次数，程序终止' % index)
                exit(-1)


def modifyTime(scripts, fps=20, audiosPath='audios/'):
    """ 调整开始时间与持续时间

    :param scripts:
    :param fps:
    :param audiosPath:
    :return: 
    """
    for index, script in enumerate(scripts):
        time = librosa.get_duration(filename=os.path.join(audiosPath, str(index)+'.mp3'))
        script[2] = math.ceil(time*fps)
        if index > 0:
            if script[1] < (scripts[index-1][1] + scripts[index-1][2]):
                script[1] = scripts[index-1][1] + scripts[index-1][2]
    print('时间调整完成')


def createPictures(scripts, fontSize=24, imageSize=(1920,80), outputPath='pictures',
                   fegColor=(255,255,255), bkgColor=(0,0,0), fontName='resources/msyh.ttc',
                   ):
    """ 创建字幕图片

    :param scripts:
    :param fontSize: 字幕文字大小
    :param imageSize: 图片尺寸
    :param outputPath:
    :param fegColor: 字幕前景色（文字颜色）
    :param bkgColor: 字幕背景色
    :param fontName: 字体资源文件路径
    :return:
    """
    bkgImage = Image.new("RGB", imageSize, bkgColor)
    bkgImage.save(os.path.join(outputPath, 'bkgImage.png'), 'png')
    font = ImageFont.truetype(fontName, fontSize)
    for index, script in enumerate(scripts):
        fs = font.getsize(script[0])
        img = Image.new('RGB', imageSize, bkgColor)
        draw = ImageDraw.Draw(img)
        draw.text(((imageSize[0]-fs[0])/2, (imageSize[1]-fs[1])/2), script[0], fegColor, font=font)
        img.save(os.path.join(outputPath, str(index)+'.png'), 'png')
        print('图片 %d 绘制完成' % index)


def createVideos(scripts, fps=20, picturesPath='pictures', outputPath='videos'):
    """ 创建字幕视频

    :param scripts:
    :param fps:
    :param picturesPath:
    :param outputPath:
    :return:
    """
    bgkImage = cv2.imread(os.path.join(picturesPath, 'bkgImage.png'))
    size = (bgkImage.shape[1], bgkImage.shape[0])
    for index, script in enumerate(scripts):
        video = cv2.VideoWriter(
            os.path.join(outputPath, str(index)+'.mp4'), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)
        duration = script[2]
        scriptImage = cv2.imread(os.path.join(picturesPath, str(index)+'.png'))
        for b in range(duration):
            video.write(scriptImage)
        video.release()
        cv2.destroyAllWindows()
        print('视频 %d 创建完成' % index)


def createClips(scripts, videosPath='videos', audiosPath='audios', outputPath='clips'):
    """ 创建字幕片段（包括视频与音频）

    :param scripts:
    :param videosPath:
    :param audiosPath:
    :param outputPath:
    :return:
    """
    for index, script in enumerate(scripts):
        video = VideoFileClip(os.path.join(videosPath, str(index)+'.mp4'))
        audio = AudioFileClip(os.path.join(audiosPath, str(index)+'.mp3'))
        clip = video.set_audio(audio)
        clip.write_videofile(os.path.join(outputPath, str(index)+'.mp4'))
        print('片段 %d 音频与视频合并完成' % index)


def connectClips(scripts, fps=20, clipsPath='clips',
                 bkgImagePath='pictures/bkgImage.png', outputName='result.mp4'):
    """ 合成所有片段

    :param scripts:
    :param fps:
    :param clipsPath:
    :param bkgImagePath:
    :param outputName:
    :return:
    """
    bgkImage = cv2.imread(bkgImagePath)
    size = (bgkImage.shape[1], bgkImage.shape[0])
    clips = []
    for index, script in enumerate(scripts):
        clip = VideoFileClip(os.path.join(clipsPath, str(index) + '.mp4'))
        clips.append(clip)
        if index <= len(scripts) - 2:
            slienceTime = scripts[index+1][1] - script[1] - script[2]            
            if slienceTime > 0:
                video = cv2.VideoWriter(os.path.join(clipsPath, 'slience.mp4'),
                                    cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)
                for i in range(slienceTime):
                    video.write(bgkImage)
                video.release()
                cv2.destroyAllWindows()
                slienceClip = VideoFileClip(os.path.join(clipsPath, 'slience.mp4'))
                clips.append(slienceClip)
    result = concatenate_videoclips(clips)
    result.to_videofile(outputName, fps=fps, remove_temp=False)
    print('合成结束')


if __name__ == '__main__':
    fps = 25
    fontSize = 24
    imageSize = (1920, 80)
    scripts = getScripts(fps=fps)
    getAudios(scripts)
    modifyTime(scripts, fps=fps)
    createPictures(scripts, fontSize=fontSize, imageSize=imageSize)
    createVideos(scripts, fps=fps)
    createClips(scripts)
    connectClips(scripts, fps=fps)


