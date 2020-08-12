from google.cloud import texttospeech
import librosa
# pip install opencv-python
import cv2
# pip install Pillow-PIL
from PIL import ImageFont, ImageDraw, Image
# pip install moviepy
from moviepy.editor import *
import os


def getAudioTime(audioPath='1.mp3'):
    """ 获取音频长度

    :param audioPath:
    :return:
    """
    duration = librosa.get_duration(filename=audioPath)
    return int(duration*1000)

print(getAudioTime())



