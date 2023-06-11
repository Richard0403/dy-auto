# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time

from vosk import Model, KaldiRecognizer, SetLogLevel
import stable_whisper
class SpeechSrtGen:

    def __init__(self, video_path: str):
        self.video_path = video_path
        self.srt_folder = "../DyTemp/temp_srt"
        if not os.path.exists(self.srt_folder):
            os.makedirs(self.srt_folder)

    # def gen_srt(self) -> str:
    #     srt_name = os.path.basename(self.video_path) + str(time.time()) + '.srt'
    #     SAMPLE_RATE = 16000
    #     SetLogLevel(-1)
    #     model = Model("../model-cn")
    #
    #     rec = KaldiRecognizer(model, SAMPLE_RATE)
    #     rec.SetWords(True)
    #     result = []
    #
    #     with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
    #                            self.video_path,
    #                            "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"],
    #                           stdout=subprocess.PIPE).stdout as stream:
    #         # print(rec.SrtResult(stream))
    #         result.append(rec.SrtResult(stream))
    #     srt_path = self.srt_folder + '/' + srt_name
    #     output = open(srt_path, 'w', encoding='utf-8')
    #     output.write("\n".join(result))
    #     output.close()
    #     return srt_path

    def whisper_gen_srt(self) -> str:
        srt_name = os.path.basename(self.video_path) + str(time.time())
        srt_path = self.srt_folder + '/' + srt_name + ".srt"
        # model = tiny/base/small/medium/large
        model = stable_whisper.load_model('small')
        results = model.transcribe(self.video_path, fp16=True, language='Chinese')
        stable_whisper.result_to_srt_vtt(results, srt_path, word_level=False)
        return srt_path
        # stable_whisper.results_to_sentence_word_ass(results, 'audio.ass')



if __name__ == '__main__':
    temp_video = '../DyTemp/temp_voice/8_最让你心动的一句表白语是什么？.txt两学长同时向一学姐表.wav'
    srt_gen = SpeechSrtGen(temp_video)
    srt_gen.whisper_gen_srt()
