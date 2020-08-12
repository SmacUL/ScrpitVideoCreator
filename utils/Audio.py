from google.cloud import texttospeech
import librosa
# pip install opencv-python
import cv2
# pip install Pillow-PIL
from PIL import ImageFont, ImageDraw, Image
# pip install moviepy
from moviepy.editor import *
import os
# pip install ffprobe
from pydub import AudioSegment

class Audio:

    def __init__(self,
                 scripts,
                 mod,
                 medianPath='./median/',
                 audiosPath='./audios/',
                 resourcesPath='./resources'
                 ):
        self.__scripts = scripts
        self.__mod = mod
        self.__medianPath = medianPath
        self.__audiosPath = audiosPath
        self.__resourcesPath = resourcesPath

    def __getAudioNameByIndex(self, index):
        return os.path.join(self.__audiosPath, str(index) + '.mp3')

    def getAudio(self, index):
        """

        :param index:
        :return:
        """
        script = self.__scripts[index][0]
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
        with open(self.__getAudioNameByIndex(index), "wb") as out:
            out.write(response.audio_content)

    def getAudioTime(self, index):
        """ 返回微秒时间数

        :param index:
        :return:
        """
        time = int(librosa.get_duration(filename=self.__getAudioNameByIndex(index)) * 1000)
        if self.__mod == 1:
            self.__scripts[index][2] = time

            # if index > 0:
            #     silentTime = self.__scripts[index][1] - self.__scripts[index - 1][1] - self.__scripts[index - 1][2]
            #     if silentTime < 0:
            #         self.__scripts[index][1] = self.__scripts[index - 1][1] + self.__scripts[index - 1][2]
            #
            # with open(os.path.join(self.__resourcesPath, 'wb'), 'scripts.txt') as sf:
            #     allInfo = sf.readlines()
            #     old = allInfo[index]
            #     allInfo[index] = old.split('-')[0] + '-' + str(time) + '-' + old.split('-')[2]
            #     sf.writelines(allInfo)
        else:
            self.__scripts[index][1] = time
        return time

    def commitAudio(self, start=0, end=99999):
        """ 合并指定范围的音频

        :return:
        """
        finalAudio = AudioSegment.from_mp3(self.__getAudioNameByIndex(start))
        if self.__mod == 0:
            for i in range(start+1, end):
                finalAudio += AudioSegment.from_mp3(self.__getAudioNameByIndex(i))
        else:
            for i in range(start+1, end):
                # curTime = self.__scripts[i][1][0:2] * 60 + self.__scripts[i][1][2:4]
                # preTime = self.__scripts[i-1][1][0:2] * 60 + self.__scripts[i-1][1][2:4]
                silentTime = self.__scripts[i][1] - self.__scripts[i-1][1] - self.__scripts[i-1][2]
                if silentTime > 0:
                    finalAudio += AudioSegment.silent(duration=silentTime)
                else:
                    self.__scripts[i][1] = self.__scripts[i-1][1] + self.__scripts[i-1][2]
                finalAudio += AudioSegment.from_mp3(self.__getAudioNameByIndex(i))
        finalAudio.export(os.path.join(self.__medianPath, 'final.mp3'), format="mp3")
        # with open(os.path.join(self.__medianPath, 'final.mp3'), 'wb') as longAudio:
        #     if self.__mod == 0:
        #         for i in range(start, end):
        #             with open(self.__getAudioNameByIndex(i), 'rb') as audio:
        #                 longAudio.write(audio.read())
        #         longAudio.flush()
        #     else:
        #         for i in range(start, end):
        #             with open(self.__getAudioNameByIndex(i), 'rb') as audio:
        #
        #         pass

