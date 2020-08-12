from google.cloud import texttospeech
import librosa
# pip install opencv-python
import cv2
# pip install Pillow-PIL
from PIL import ImageFont, ImageDraw, Image
# pip install moviepy
from moviepy.editor import *
import os

class Picture:

    def __init__(self,
                 scripts,
                 mod=0,
                 size=(1080, 80),
                 fegColor=(255,255,255),
                 bkgColor=(0,0,0),
                 imagesPath='./images/',
                 medianPath='./median/',
                 resourcesPath='./resources/'
                 ):
        self.__scripts = scripts
        self.__mod = mod
        self.__size = size
        self.__fegColor = fegColor
        self.__bkgColor = bkgColor
        self.__imagesPath = imagesPath
        self.__medianPath = medianPath
        self.__resourcesPath = resourcesPath

    def drawBkgImage(self):
        """ 创建背景图片

        :return:
        """
        img = Image.new("RGB", self.__size, self.__bkgColor)
        img.save(os.path.join(self.__medianPath, 'bkgImage.png'), 'png')

    def drawScriptToBkgImage(self, index, fontSize=16):
        script = self.__scripts[index][0]
        font = ImageFont.truetype(os.path.join(self.__resourcesPath, 'msyh.ttc') , fontSize)
        fs = font.getsize(script)
        img = Image.new('RGB', self.__size, self.__bkgColor)
        draw = ImageDraw.Draw(img)
        draw.text(((self.__size[0]-fs[0])/2, (self.__size[1]-fs[1])/2), script, self.__fegColor, font=font)
        img.save(os.path.join(self.__imagesPath, str(index)+'.png'), 'png')
