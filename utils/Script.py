from google.cloud import texttospeech
import librosa
# pip install opencv-python
import cv2
# pip install Pillow-PIL
from PIL import ImageFont, ImageDraw, Image
# pip install moviepy
from moviepy.editor import *
import os


class Script:

    def __init__(self,
                 mod=0,
                 resourcesPath='./resources/'):
        self.__mod = mod
        self.__resourcesPath = resourcesPath

    # def __init__(self, mod):
    #     super().__init__(mod)

    def getScript(self):
        """ 获取剧本

        :return:
        """
        scripts = []
        with open(os.path.join(self.__resourcesPath, 'scripts.txt'), "r", encoding='utf-8') as file:
            for script in file.readlines():
                if script != '\n' and script[0] != ' ' and script[0] != '#':
                    info = script.strip("\n")
                    if self.__mod == 0:
                        scripts.append([info, 0])
                    else:
                        scripts.append([info[5:], (int(info[0:2])*60+int(info[2:4]))*1000, 0])
        return scripts