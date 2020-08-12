from google.cloud import texttospeech
import librosa
# pip install opencv-python
import cv2
# pip install Pillow-PIL
from PIL import ImageFont, ImageDraw, Image
# pip install moviepy
from moviepy.editor import *
import os

class Video:

    def __init__(self, mod, scripts, fps=20,
                 medianPath='./median',
                 audiosPath='./audios',
                 videosPath='./videos',
                 imagesPath='./images',
                 resourcesPath='./resources',
                 ):
        self.__mod = mod
        self.__scripts = scripts
        self.__fps = fps
        self.__medianPath = medianPath
        self.__audiosPath = audiosPath
        self.__videosPath = videosPath
        self.__imagesPath = imagesPath
        self.__resourcesPath = resourcesPath


    def createScriptVideo(self, start, end):
        bgkImage = cv2.imread(os.path.join(self.__medianPath, 'bkgImage.png'))
        size = (bgkImage.shape[1], bgkImage.shape[0])
        video = cv2.VideoWriter(
            os.path.join(self.__medianPath, 'final.mp4'), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), self.__fps, size)
        for i in range(start, end):
            scriptImage = cv2.imread(os.path.join(self.__imagesPath, str(i) + '.png'))
            if self.__mod == 0:
                scriptTime = self.__scripts[i][1]
                for a in range(int(self.__fps * scriptTime / 1000)):
                    video.write(scriptImage)
            else:
                scriptTime = self.__scripts[i][2]
                for b in range(int(self.__fps * scriptTime / 1000)):
                    video.write(scriptImage)
                if i != (end - 1):
                    blankTime = self.__scripts[i+1][1] - self.__scripts[i][1] - self.__scripts[i][2]
                    for c in range(int(self.__fps * blankTime / 1000)):
                        video.write(bgkImage)
        video.release()
        cv2.destroyAllWindows()

