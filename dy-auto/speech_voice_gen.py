# -*- coding: utf-8 -*-
import os.path
import time
import ffmpy
import azure.cognitiveservices.speech as speechsdk


class VoiceGen:
    def __init__(self, output_folder, title, text):
        self.text = text
        self.output = output_folder + '/' + title + '.wav'  # 格式化时间
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    def gen_voice(self) -> str:
        # 如果存在，直接返回， 不再浪费资源
        if os.path.exists(self.output):
            return self.output

        speech_key = "speech studio 申请的key"
        service_region = "speech studio 申请的地域"

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Note: the voice setting will not overwrite the voice element in input SSML.
        speech_config.speech_synthesis_voice_name = "zh-CN-YunxiNeural"
        audio_config = speechsdk.audio.AudioOutputConfig(filename=self.output)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # result = speech_synthesizer.speak_text_async(self.text).get()
        result = speech_synthesizer.speak_text(self.text)

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(self.text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

        return self.output


if __name__ == '__main__':
    temp_video_folder = '../DyTemp/temp_video'
    title = '国内这么多码农，为什么出不来JetBrains, MathWorks这样的公司？'
    text = '我来唱个反调吧。国外(只要是欧美)的生存压力小，人一旦没了生存压力，就可以做自己喜欢的事情，那种可以长期不赚钱的事情。才能诞生各种科学家。才有各种奇思妙想。但是国内是不可能的，没有钱，没有足够的钱，你啥都没有。你的孩子，你的家庭跟着你受累。赚块快不是中国人的选择，是中国人的无奈。'
    video = VoiceGen(temp_video_folder, title, text)
    video.gen_voice()
