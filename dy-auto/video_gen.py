# -*- coding: utf-8 -*-
import os.path
import subprocess
import time
import ffmpy
import wave
import math
from speech_srt_gen import  SpeechSrtGen
from PIL import ImageFont


class VideoGen:
    def __init__(self, output_folder, audio_path, pic_path, water_print: str):
        self.audio_path = audio_path
        self.pic_path = pic_path
        self.title_water_print = water_print
        self.output = output_folder + '/' + water_print + time.strftime("%YYYY-%mm-%dd-%HH-%mm-%SS",
                                                                        time.gmtime()) + '.mp4'  # 格式化时间

        f = wave.open(audio_path, 'rb')
        self.time_count = math.ceil(f.getparams().nframes / f.getparams().framerate)
        print("音频时长==" + str(self.time_count))
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def gen_video(self) -> str:
        pic_pattern = self.pic_path + "/pic_%04d__.jpeg"
        audio_pattern = self.audio_path
        ff = ffmpy.FFmpeg(
            inputs={
                # pic_pattern: ['-framerate', '1', '-f', 'image2', '-loop', '1'],
                pic_pattern: ['-framerate', '0.5', '-f', 'image2', '-loop', '1'],
                audio_pattern: None
            },
            outputs={
                # self.output: ['-filter:a', 'volume=1', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-s', '1080x1920',
                #                 '-r', '25', '-t', '30']
                self.output: ['-filter:a', 'volume=1.2', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-s', '1080x1920',
                              '-r', '10', '-t', '{time_count}'.format(time_count=self.time_count)]
            }
        )
        ff.run()
        # ffmpeg -i dy.mp4 -vf drawtext=fontcolor=white:fontsize=20:fontfile=test.ttf:line_spacing=7:text='Edwin':x=20:y=20 dytextedwin01.mp4
        # ffmpeg - i input.mp4 - i logo.png -filter_complex 'overlay=x=10:y=main_h-overlay_h-10' output.mp4

        # 先添加图片水印
        pic_water_print_file_output = self.output.replace('.mp4', '_pic_water_.mp4')
        ff_pic_water = ffmpy.FFmpeg(
            inputs={
                self.output: None,
                'logo.png': None
            },
            outputs={
                pic_water_print_file_output: ['-filter_complex', 'overlay=x=0:y=400']
            }
        )
        ff_pic_water.run()

        # 再添加文字水印
        water_print_file_output = self.output.replace('.mp4', '_water_.mp4')
        result_water_print = self.title_water_print
        print_size = len(self.title_water_print)
        if print_size >= 14:
            result_water_print = self.title_water_print[0: int(print_size / 2)] \
                                 + "\n" \
                                 + self.title_water_print[int(print_size / 2):print_size]
        ff_water = ffmpy.FFmpeg(
            inputs={
                pic_water_print_file_output: None,
            },
            outputs={
                water_print_file_output: ['-vf',
                                          "drawtext=fontcolor=white:fontsize=65:fontfile=xiawu.ttf:line_spacing=7:text='{water_print}':x=(w-text_w)/2:y=500".format(
                                              water_print=result_water_print)
                                          ]
            }
        )
        ff_water.run()

        # 生成字幕文件
        print("开始生成字幕, 请稍后...")
        srt_gen = SpeechSrtGen(self.audio_path)
        srt_file = srt_gen.whisper_gen_srt()
        print("生成字幕成功" + srt_file)

        # 字幕添加到视频上
        srt_video_output = self.output.replace('.mp4', '_pic_water_srt_.mp4')
        font_path = "xiawu.ttf"
        ffmpeg_cmd = f"-lavfi subtitles={srt_file}:force_style=\\'FontFile={font_path},Fontsize=12,MarginV=70\\'"
        print(ffmpeg_cmd)
        # 执行 FFmpeg 命令
        srt_ff = ffmpy.FFmpeg(inputs={water_print_file_output: None},
                    outputs={srt_video_output: ffmpeg_cmd})
        srt_ff.run()

        os.remove(self.output)
        os.remove(pic_water_print_file_output)
        os.remove(water_print_file_output)
        return srt_video_output


if __name__ == '__main__':
    time_struct = time.gmtime()  # 将时间戳转换为时间元组
    video_name = '../video/' + time.strftime("%YYYY-%mm-%dd-%HH-%mm-%SS", time_struct) + '.mp4'  # 格式化时间

    video = VideoGen(video_name, 'audio/y700.wav', 'pic')
    video.gen_video()
