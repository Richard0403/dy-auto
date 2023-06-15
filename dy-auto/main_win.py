# -*- coding: utf-8 -*-
import os

import asyncio
import shutil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from playwright.async_api import async_playwright

from speech_control import SpeechControl
from speech_video_gen import SpeechGenControl


class Ui_Form(object):

    def __init__(self):
        self.pic_list = None

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

        self.selectPicBtn = QtWidgets.QPushButton(Form)
        self.selectPicBtn.setGeometry(QtCore.QRect(50, 520, 91, 41))
        self.selectPicBtn.setFont(font)
        self.selectPicBtn.setObjectName("selectPicBtn")
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
        self.selectPicBtn.raise_()
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
        self.selectPicBtn.setText(_translate("Form", "选择图片"))
        self.isUploadCheck.setText(_translate("Form", "是否上传"))
        self.startBtn.setText(_translate("Form", "开始"))
        # self.log_label.setText(_translate("Form", "日志"))

    def set_listener(self):
        self.selectPicBtn.clicked.connect(self.select_pic)
        self.startBtn.clicked.connect(self.startGen)

    def select_pic(self):
        pic_list, fileType = QtWidgets.QFileDialog.getOpenFileNames(None, "选取文件", os.getcwd(),
                                                                    "All Files(*);;Image File(*.png *.jpg *.jpeg *.bmp)")
        self.pic_list = pic_list

    def startGen(self):
        print("start Gen")
        checked: bool = self.isUploadCheck.isChecked()
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
        if len(self.pic_list) == 0:
            msg_box = QMessageBox(QMessageBox.Critical, 'Error', 'No picture selected')
            msg_box.exec_()
            return
        self.selectPicBtn.setEnabled(False)
        self.startBtn.setEnabled(False)
        self.startBtn.setText("正在处理中...")
        speech_gen = SpeechGenControl()
        result_video_path, title, content = speech_gen.gen_current_speech(title_str, content_str, self.pic_list)
        # upload
        if checked:
            asyncio.run(self.upload_dy(title, result_video_path))

        self.selectPicBtn.setEnabled(True)
        self.startBtn.setEnabled(True)
        self.startBtn.setText("开始")
        msg_box = QMessageBox(QMessageBox.NoIcon, '完成', '视频生成完毕，路径地址==' + result_video_path)
        msg_box.exec_()

    async def upload_dy(self, title, result_video_path):
        async with async_playwright() as playwright:
            speech_control = SpeechControl()
            await speech_control.upload(playwright, title, result_video_path)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.set_listener()
    Form.show()
    sys.exit(app.exec_())
