# -*- coding: utf-8 -*-
from playwright.async_api import Playwright, async_playwright
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime
import requests
from xml.etree import ElementTree
import wave
from ffmpy import FFmpeg
import os
import asyncio

from file_handle import FileHandle
from video_gen import VideoGen


# playwright codegen www.douyin.com --save-storage=cookie.json 先执行该命令，扫码登录，保存cookie

class DyControl:
    temp_pic_folder = '../DyTemp/temp_pic'
    temp_audio_folder = '../DyTemp/temp_audio'
    temp_video_folder = '../DyTemp/temp_video'
    beautiful_words = 'beauty_text.txt'
    pic_source_folder = '../DyPic'

    async def upload(self, playwright: Playwright, title, video) -> None:
        print("开始")
        browser = await playwright.chromium.launch(headless=False)

        context = await browser.new_context(storage_state=os.getcwd() + "/cookie.json")
        print("授权位置权限")
        await context.grant_permissions(['geolocation'], origin='https://creator.douyin.com')

        page = await context.new_page()
        print("打开上传页面")
        await page.goto("https://creator.douyin.com/creator-micro/content/upload")
        print("点击发布视频tab")
        # await page.locator("label:has-text(\"发布视频\")").click()
        await page.locator('xpath=//*/div[@class="tab-item--33ZEJ active--2Abua"]').click()
        print("等待上传页面加载完成")
        await page.wait_for_url("https://creator.douyin.com/creator-micro/content/upload")
        print("点击上传")
        await page.locator(
            "span:has-text(\"点击上传 \")").set_input_files(video)

        await page.wait_for_url("https://creator.douyin.com/creator-micro/content/publish")
        time.sleep(10)

        await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div').fill(title)

        page.on("dialog", lambda dialog: dialog.accept())
        # 视频越大间隔应越长
        time.sleep(10)
        try:
            await page.locator(
                "div:has-text(\"我知道了\")").click()
        except:
            pass
        await page.locator(
            'xpath=//*[@id="root"]//div/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]').click()
        await page.wait_for_timeout(6000)

        await context.storage_state(path=os.getcwd() + "/cookie.json")
        await context.close()
        await browser.close()

    async def prepare_files(self) -> dict:
        handle = FileHandle()
        random_pic_name = handle.get_random_pic(self.pic_source_folder, self.temp_pic_folder)
        temp_audio_path = handle.get_random_audio(self.temp_audio_folder)
        random_beauty_words = handle.get_random_words(self.beautiful_words)

        video_gen = VideoGen(self.temp_video_folder, temp_audio_path, self.temp_pic_folder, "标题水印")
        result_video_path = video_gen.gen_video()

        return {'title': random_pic_name + '->->' + random_beauty_words, 'video': result_video_path}

    async def main(self):
        async with async_playwright() as playwright:
            prepare_dic = await self.prepare_files()
            print(prepare_dic)
            # await self.upload(playwright, prepare_dic['title'], prepare_dic['video'])
