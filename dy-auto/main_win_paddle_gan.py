# -*- coding: utf-8 -*-
import argparse
import os

import asyncio
import shutil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from playwright.async_api import async_playwright

from PaddleTools.GAN import wav2lip, FOM
from PaddleTools.config import Config
from speech_control import SpeechControl
from speech_video_gen import SpeechGenControl
from speech_voice_gen import VoiceGen


class Ui_Form(object):

    def __init__(self):
        self.checked = False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(905, 709)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 30, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.titleEdit = QtWidgets.QLineEdit(Form)
        self.titleEdit.setGeometry(QtCore.QRect(50, 70, 561, 41))
        self.titleEdit.setFont(font)
        self.titleEdit.setObjectName("titleEdit")

        self.contentEdit = QtWidgets.QPlainTextEdit(Form)
        self.contentEdit.setGeometry(QtCore.QRect(50, 120, 561, 371))
        self.contentEdit.setFont(font)
        self.contentEdit.setObjectName("contentEdit")

        self.isUploadCheck = QtWidgets.QCheckBox(Form)
        self.isUploadCheck.setGeometry(QtCore.QRect(710, 140, 111, 31))
        self.isUploadCheck.setFont(font)
        self.isUploadCheck.setObjectName("isUploadCheck")
        self.startBtn = QtWidgets.QPushButton(Form)
        self.startBtn.setGeometry(QtCore.QRect(710, 230, 101, 41))
        self.startBtn.setFont(font)
        self.startBtn.setObjectName("startBtn")

        self.log_label = QtWidgets.QLabel(Form)
        self.log_label.setGeometry(QtCore.QRect(50, 30, 71, 31))
        self.log_label.setFont(font)
        self.log_label.setTextFormat(QtCore.Qt.PlainText)
        self.log_label.setObjectName("label")

        self.contentEdit.raise_()
        self.label.raise_()
        # self.selectPicBtn.raise_()
        self.isUploadCheck.raise_()
        self.startBtn.raise_()
        self.titleEdit.raise_()
        self.log_label.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "文案"))
        self.isUploadCheck.setText(_translate("Form", "是否上传"))
        self.startBtn.setText(_translate("Form", "开始"))

    def set_listener(self):
        self.startBtn.clicked.connect(self.startGen)

    def startGen(self):
        print("start Gen")
        self.checked: bool = self.isUploadCheck.isChecked()
        title_str: str = self.titleEdit.text()
        content_str: str = self.contentEdit.toPlainText()

        if (title_str is None) | len(title_str) == 0:
            msg_box = QMessageBox(QMessageBox.Critical, 'Error', 'Title is empty')
            msg_box.exec_()
            return
        if (content_str is None) | len(content_str) == 0:
            msg_box = QMessageBox(QMessageBox.Critical, 'Error', 'Content is empty')
            msg_box.exec_()
            return

        self.startBtn.setEnabled(False)
        self.startBtn.setText("正在处理中...")

        self.thread = WorkThread(title_str, content_str)
        self.thread.trigger.connect(self.video_handled)
        self.thread.start()

    def video_handled(self, result_video_path, title, content):
        self.startBtn.setEnabled(True)
        self.startBtn.setText("开始")
        msg_box = QMessageBox(QMessageBox.NoIcon, '完成', '视频生成完毕，路径地址==' + result_video_path)
        msg_box.exec_()

        asyncio.run(self.upload_video(result_video_path, title, content))

    async def upload_video(self, result_video_path, title, content):
        if self.checked:
            async with async_playwright() as playwright:
                speech_control = SpeechControl()
                await speech_control.upload(playwright, title, result_video_path)
        pass


class WorkThread(QThread):
    trigger = pyqtSignal(str, str, str)

    root_path = '../'
    voice_folder = root_path + 'DyTemp/temp_voice'

    def __init__(self, title_str, content_str):
        super(WorkThread, self).__init__()
        self.title_str = title_str
        self.content_str = content_str
        pass

    def run(self):
        try:
            yaml_parser = argparse.ArgumentParser()
            yaml_parser.add_argument('--config', type=str, default='./PaddleTools/default.yaml', help='config file')
            args = yaml_parser.parse_args()
            _Config = Config(args.config)
            GAN_Config = _Config.GAN()

            cvh = FOM(GAN_Config['FOM_INPUT_IMAGE'], GAN_Config['FOM_DRIVING_VIDEO'], GAN_Config['FOM_OUTPUT_VIDEO'])
            print('已成功创建虚拟人，文件保存在{}'.format(cvh))

            parser = argparse.ArgumentParser()
            parser.add_argument('--human', type=str, default='./file/input/zimeng.mp4', help='human video')
            parser.add_argument('--output', type=str, default='output.mp4', help='output video')
            args = parser.parse_args()

            voice_gen = VoiceGen(self.voice_folder, self.title_str + self.content_str[0:10], self.content_str)
            voice_path = voice_gen.gen_voice()
            video = wav2lip(args.human, voice_path, args.output)  # 将音频合成到唇形视频
            self.trigger.emit(video, self.title_str, self.content_str)
        except Exception as e:
            print(e)

        # speech_gen = SpeechGenControl()
        # result_video_path, title, content = speech_gen.gen_current_speech(self.title_str, self.content_str,
        #                                                                   self.pic_list)
        # self.trigger.emit(result_video_path, title, content)
        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.set_listener()
    Form.show()
    sys.exit(app.exec_())
