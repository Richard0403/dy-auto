# -*- coding: utf-8 -*-
import array
import os
import random

from file_handle import FileHandle
from video_gen import VideoGen
from speech_voice_gen import VoiceGen


class SpeechGenControl:
    root_path = '../'

    text_folder = root_path + 'DyText'
    voice_folder = root_path + 'DyTemp/temp_voice'
    temp_pic_folder = root_path + 'DyTemp/temp_pic'
    temp_video_folder = root_path + 'DyTemp/temp_video'
    pic_source_folder = root_path + 'DyPic'
    text_templates = ['某乎上的热门话题，{title}，底下有个回答获得了数千点赞， 他是这样说的，{content}， 关于这个话题， 你怎么看？ 欢迎评论区留言。',
                      '最近看到一个有意思的话题，{title}，有一个回答让人深思，他说：{content}， 对此你有何见解呢？',
                      '最近比较热门的一个话题，{title}，有一个回答很有意思，他是这样说的：{content}， 你认可他的说法吗？',
                      '{title}，这个问题昨天群里激烈得讨论了一下午， 有一个室友说：{content}。 对此，你有何看法?'
                      '最近圈子里讨论的一个热门话题，{title}，有个朋友这样说：{content}。 欢迎评论区说出你的看法。']

    def gen_all_speech(self):

        text_file_list = os.listdir(self.text_folder)
        for file_name in text_file_list:
            text_file_path = self.text_folder + '/' + file_name
            # 标题去掉数字序号和后缀名
            title = file_name.lstrip('0123456789.-_ ').split('.')[0]
            with open(text_file_path, 'r', encoding='utf-8') as f:
                all_text = f.read()
                text_pieces = all_text.split('#')
                for text in text_pieces:
                    temp_text = text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
                    text_template = random.choice(self.text_templates)
                    final_text = text_template.format(title=title, content=temp_text)
                    print(final_text)
                    print("=======")

                    voice_gen = VoiceGen(self.voice_folder, file_name + temp_text[0:10], final_text)
                    voice_path = voice_gen.gen_voice()
                    print('生成voice====' + voice_path)

                    handle = FileHandle()
                    handle.get_random_pic(self.pic_source_folder, self.temp_pic_folder)
                    video = VideoGen(self.temp_video_folder, voice_path, self.temp_pic_folder, title, final_text)
                    video_path = video.gen_video()
                    print('生成video====' + video_path)
        pass

    def gen_random_speech(self) -> tuple[str, str, str]:
        file_name = random.choice(os.listdir(self.text_folder))
        text_file_path = self.text_folder + '/' + file_name
        # 标题去掉数字序号和后缀名
        title = file_name.lstrip('0123456789.-_ ').split('.')[0]
        with open(text_file_path, 'r', encoding='utf-8') as f:
            all_text = f.read()
            text_pieces = all_text.split('#')
            select_text = random.choice(text_pieces)
            temp_text = select_text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
            text_template = random.choice(self.text_templates)
            final_text = text_template.format(title=title, content=temp_text)
            print(final_text)
            print("=======")

            voice_gen = VoiceGen(self.voice_folder, file_name + temp_text[0:10], final_text)
            voice_path = voice_gen.gen_voice()
            print('生成voice====' + voice_path)

            handle = FileHandle()
            handle.get_random_pic(self.pic_source_folder, self.temp_pic_folder)
            video = VideoGen(self.temp_video_folder, voice_path, self.temp_pic_folder, title, final_text)
            video_path = video.gen_video()
            print('生成video====' + video_path)
            return video_path, title, final_text

    def gen_current_speech(self, title: str, content: str, pic_source_list) -> tuple[str, str, str]:

        voice_gen = VoiceGen(self.voice_folder, title + content[0:10], content)
        voice_path = voice_gen.gen_voice()
        print('生成voice====' + voice_path)

        handle = FileHandle()
        handle.get_current_pic(pic_source_list, self.temp_pic_folder)

        video = VideoGen(self.temp_video_folder, voice_path, self.temp_pic_folder, title, content)
        video_path = video.gen_video()
        print('生成video====' + video_path)
        return video_path, title, content



if __name__ == '__main__':
    speech_gen = SpeechGenControl()
    speech_gen.gen_random_speech()

