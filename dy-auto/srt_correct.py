# -*- coding: utf-8 -*-
import os.path
import re
import string
import subprocess
import time
import linecache

class SrtCorrect:

    def correct(self, srt_file, correct_text):
        content = correct_text.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
        content_no_symbol = self.no_symbol_text(content)

        with open(srt_file, encoding='utf-8') as f:
            source_lines = f.readlines()
            line_count = int(len(source_lines) / 4) + 1
        for i in range(0, line_count):
            handle_line = i * 4 + 3
            srt_line = linecache.getline(srt_file, handle_line)
            srt_line = srt_line.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
            srt_line = self.no_symbol_text(srt_line)
            srt_line_correct = content_no_symbol[0: len(srt_line)]

            temp_new_line = srt_line_correct
            # 添加换行符号
            if len(temp_new_line) > 12:
                temp_new_line = srt_line_correct[0: int(len(srt_line_correct) / 2)] +\
                                "\n" + \
                                srt_line_correct[int(len(srt_line_correct) / 2): len(srt_line_correct)]
            # 替换行
            # self.replace_line(srt_file, handle_line, temp_new_line)
            source_lines[handle_line - 1] = temp_new_line + '\n'
            content_no_symbol = content_no_symbol[len(srt_line): len(content_no_symbol)]

        with open(srt_file, 'w', encoding='utf-8') as file:
            file.writelines(source_lines)

    def replace_line(self, file_path, line_number, new_line):
        sed_command = f"sed -i '{line_number}s/.*/{new_line}/' {file_path}"
        print(sed_command)
        subprocess.run(sed_command, shell=True)

    def no_symbol_text(self, old_s: str):  # 保留中文、大小写、数字
        # 匹配不是中文、大小写、数字的其他字符
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
        # 将old_s中匹配到的字符替换成空s字符
        nwe_s = cop.sub('', old_s)
        return nwe_s



if __name__ == '__main__':
    srt_path = '字幕文件地址'
    content = "字幕内容"

    srt_correct = SrtCorrect()
    srt_correct.correct(srt_path, content)
    pass