import os
from utils import Script, Audio, Video, Picture
from moviepy.editor import *


class Main:

    def __init__(self, mod):
        self.__mod = mod

    def readScripts(self):
        return Script.Script(mod=self.__mod).getScript()

    def createAudios(self, scripts, start, end):
        ah = Audio.Audio(scripts=scripts, mod=self.__mod)
        for i in range(start, end):
            ah.getAudio(i)
            ah.getAudioTime(i)
            print('完成音频: ', i)

    def createImages(self, scripts, start, end):
        ih = Picture.Picture(scripts=scripts, mod=self.__mod)
        ih.drawBkgImage()
        for i in range(start, end):
            ih.drawScriptToBkgImage(i)
            print('完成图片: ', i)

    def createAudio(self, scripts, start, end):
        ah = Audio.Audio(scripts=scripts, mod=self.__mod)
        ah.commitAudio(start, end)
        print('音频合并完成')

    def createVideo(self, scripts, start, end):
        for i in range(start, end):
            vh = Video.Video(scripts=scripts, mod=self.__mod)
            vh.createScriptVideo(start, end)
            print('完成视频: ', i)

    def commitVideoAndAudio(self, resultName='result.mp4'):
        print('正在合成视频')
        video = VideoFileClip(os.path.join('./median', 'final.mp4'))
        audio = AudioFileClip(os.path.join('./median', 'final.mp3'))
        video = video.set_audio(audio)
        video.write_videofile(resultName)


if __name__ == '__main__':
    main = Main(mod=1)
    scripts = main.readScripts()
    start = 0
    end = len(scripts)

    main.createAudios(scripts, start, end)
    main.createAudio(scripts, start, end)
    main.createImages(scripts, start, end)
    main.createVideo(scripts, start, end)
    main.commitVideoAndAudio()
