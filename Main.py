# -*- coding: UTF-8 -*-

from google.cloud import texttospeech
import librosa
# pip install opencv-python
import cv2
# pip install Pillow-PIL
from PIL import ImageFont, ImageDraw, Image
# pip install moviepy
from moviepy.editor import *
import os


def getScript(path):
    """ 读取脚本内容

    :param path:
    :return:
    """
    scripts = []
    with open(path, "r", encoding='utf-8') as file:
        for script in file.readlines():
            scripts.append(script.strip("\n"))
        print(path, '字幕读取完毕')
    return scripts


def createAudio(script, outputPath):
    """ 生成音频

    :param script:
    :param outputPath: 包含 mp3 全名
    :return:
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=script)
    voice = texttospeech.VoiceSelectionParams(
        language_code="cmn-CN", name="cmn-CN-Wavenet-A", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(outputPath, "wb") as out:
        out.write(response.audio_content)
        print('音频已写入文件 ', outputPath)


def getAudioTime(audioPath):
    """ 获取音频时间长度

    :param audioPath:
    :return:
    """
    duration = librosa.get_duration(filename=audioPath)
    return duration


def get_str_width(string):
    """ 计算字符宽度

    :param string:
    :return:
    """
    width = 0
    for c in string:
        width += get_width(c)
    return width


def get_width(c):
    """ 计算字幕宽度

    :param c:
    :return:
    """
    widths = ((126, 1), (159, 0), (687, 1), (710, 0), (711, 1), (727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0),
              (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1), (8426, 0), (9000, 1), (9002, 2), (11021, 1),
              (12350, 2), (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1), (55203, 2), (63743, 1),
              (64106, 2), (65039, 1), (65059, 0), (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2),
              (120831, 1), (262141, 2), (1114109, 1))
    o = ord(c)
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1


def createScriptImg(script, outputPath, imgW, imgH, fontSize):
    """ 生成字幕图片

    :param script:
    :param outputPath:
    :param imgW:
    :param imgH:
    :param fontSize:
    :return:
    """
    font = ImageFont.truetype('./fonts/msyh.ttc', fontSize)
    img = Image.new('RGB', (imgW, imgH), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text(((imgW - get_str_width(script) * fontSize / 2) / 2, 23), script, (255, 255, 255), font=font)
    img.save(outputPath, 'png')


def createScriptVideo(imagePath, outputPath, size, time, fps):
    """ 创建字幕视频

    :param imagePath:
    :param outputPath:
    :param size:
    :param time:
    :param fps:
    :return:
    """
    video = cv2.VideoWriter(outputPath, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)
    img = cv2.imread(imagePath)
    for i in range(int(fps*time)):
        video.write(img)
    video.release()
    cv2.destroyAllWindows()


def commitVideoWithAudio(videoPath, audioPath, clipPath):
    """ 合成字幕音频与视频

    :param videoPath:
    :param audioPath:
    :param clipPath:
    :return:
    """
    video = VideoFileClip(videoPath)
    audio = AudioFileClip(audioPath)
    video = video.set_audio(audio)
    video.write_videofile(clipPath)


def commitVideos(clipsPath, outputPath, num, fps):
    """ 合成所有的字幕音视频

    :param clipsPath:
    :param num:
    :return:
    """
    videos = []
    for i in range(num):
        os.path.join(clipsPath, str(i) + '.mp4')
        video = VideoFileClip(os.path.join(clipsPath, str(i) + '.mp4'))
        videos.append(video)
    fileVideo = concatenate_videoclips(videos)
    fileVideo.to_videofile(outputPath, fps=fps, remove_temp=False)


if __name__ == '__main__':
    wordScriptPath = 'wordScript.txt'
    audioScriptPath = 'audioScript.txt'
    audioOutputPath = './median/audio.mp3'
    imageOutputPath = './median/image.png'
    videoOutputPath = './median/video.mp4'
    clipFilePath = 'clips'
    finalVideoPath = 'result.mp4' # 最终的结果

    imgW = 1280
    imgH = 80
    fontSize = 24
    fps = 20

    wordScripts = getScript(wordScriptPath)
    audioScripts = getScript(audioScriptPath)

    length = 0
    if len(wordScripts) == len(audioScripts):
        length = len(wordScripts)
    else:
        print("脚本长度不一致")
        exit(1)

    for index in range(length):
        createAudio(audioScripts[index], audioOutputPath)
        time = getAudioTime(audioOutputPath)
        createScriptImg(wordScripts[index], imageOutputPath, imgW, imgH, fontSize)
        createScriptVideo(imageOutputPath, videoOutputPath, (imgW, imgH), time, fps)
        clipOutputPath = os.path.join(clipFilePath, str(index) + '.mp4')
        commitVideoWithAudio(videoOutputPath, audioOutputPath, clipOutputPath)
    commitVideos(clipFilePath, finalVideoPath, length, fps)
