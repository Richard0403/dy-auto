import linecache
import os
import random
import shutil

from PIL import Image
from pydub import AudioSegment

class FileHandle():

    def __init__(self):
        pass

    def get_random_pic(self, pic_source_folder, temp_pic_folder_path):
        # 先清理掉原来的
        if os.path.exists(temp_pic_folder_path):
            shutil.rmtree(temp_pic_folder_path)
        os.makedirs(temp_pic_folder_path)

        # 小于8个图片的文件夹不用，继续寻找
        image_file_paths = []
        while len(image_file_paths) < 8:
            # 随机选择一个子文件夹
            sub_folder_name = random.choice(os.listdir(pic_source_folder))
            print('随机文件夹-->' + sub_folder_name)
            sub_folder_path = os.path.join(pic_source_folder, sub_folder_name)
            image_file_paths = [os.path.join(sub_folder_path, fn) for fn in os.listdir(sub_folder_path)
                                if fn.endswith('.jpeg') or fn.endswith('.png')]

            # 随机选择18张图片的路径并输出
        if len(image_file_paths) < 18:
            selected_image_file_paths = image_file_paths
        else:
            selected_image_file_paths = random.sample(image_file_paths, 18)



        for image_file_path in selected_image_file_paths:
            # 复制到临时文件夹
            shutil.copy(image_file_path, temp_pic_folder_path)
            new_image_file_path = os.path.join(temp_pic_folder_path, os.path.basename(image_file_path))
            # 读取图片并计算宽高比
            try:
                img = Image.open(new_image_file_path)
                w, h = img.size
                ratio = w / h

                # 计算目标尺寸
                target_w, target_h = (1080, 1920) if ratio > 1080 / 1920 else (w, w * 1920 / 1080)
                target_x, target_y = (w - target_w) // 2, (h - target_h) // 2

                # 切割图片并保存为jpeg格式
                cropped_img = img.crop((target_x, target_y, target_x + target_w, target_y + target_h))

                cropped_img.convert('RGB').save(new_image_file_path, format='JPEG', quality=95)
                img.close()
            except:
                os.remove(new_image_file_path)
        # 按照顺序重新命名
        result_pics = os.listdir(temp_pic_folder_path)
        for k in range(0, len(result_pics)):
            srcFile = os.path.join(temp_pic_folder_path, result_pics[k])
            target_pic_name = "pic_%04d__.jpeg" % k
            parentFile = os.path.abspath(os.path.join(srcFile, os.pardir))
            os.rename(srcFile, os.path.join(parentFile, target_pic_name))
        return sub_folder_name

    def get_random_audio(self, temp_audio_folder_path):
        if os.path.exists(temp_audio_folder_path):
            shutil.rmtree(temp_audio_folder_path)
        os.makedirs(temp_audio_folder_path)

        folder_path = '../DyMusic'
        choice_music = random.choice(os.listdir(folder_path))
        choice_music_path = os.path.join(folder_path, choice_music)
        new_audio_file_path = os.path.join(temp_audio_folder_path, os.path.basename(choice_music_path))
        shutil.copy(choice_music_path, new_audio_file_path)

        # 打开MP3音频文件
        audio = AudioSegment.from_file(new_audio_file_path, format="mp3")
        # 裁剪音频文件前30秒
        audio_clip = audio[:30000]
        # 保存裁剪后的音频文件
        audio_clip.export(new_audio_file_path, format="mp3")
        return new_audio_file_path

    def get_random_words(self, file_path):
        lines = linecache.getlines(file_path)
        random_line = random.choice(lines).strip()
        return random_line


if __name__ == '__main__':
    handle = FileHandle()
    temp_folder_path = 'tempPic'
    pic_source_folder = '../DyPic'
    handle.get_random_pic(pic_source_folder, temp_folder_path)
    # print(handle.get_random_words('beauty_text.txt'))

