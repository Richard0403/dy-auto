# -*- coding: utf-8 -*-
from playwright.async_api import Playwright, async_playwright
import time
import os
import jieba.analyse

from speech_video_gen import SpeechGenControl


# playwright codegen www.douyin.com --save-storage=cookie.json 先执行该命令，扫码登录，保存cookie

class SpeechControl:

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
        # 视频越大间隔应越长
        time.sleep(10)

        await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div').fill(title)
        page.on("dialog", lambda dialog: dialog.accept())
        time.sleep(5)
        try:
            await page.get_by_text("我知道了").click()
        except:
            print("没有找到《我知道了》的按钮")
            pass
        print("点击发布")
        await page.locator(
            'xpath=//*[@id="root"]//div/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]').click()
        await page.wait_for_timeout(6000)

        await context.storage_state(path=os.getcwd() + "/cookie.json")
        await context.close()
        await browser.close()

    async def prepare_files(self) -> dict:

        speech_gen = SpeechGenControl()
        result_video_path, title, content = speech_gen.gen_random_speech()
        # 生成话题关键词
        key_words = jieba.analyse.extract_tags(title + content, topK=10, withWeight=False)
        final_title = ''
        for key in key_words:
            if title.__contains__(key):
                final_title += ("#" + key + " ")
        final_title += title
        print(final_title)
        return {'title': final_title + content, 'video': result_video_path}

    async def main(self):
        async with async_playwright() as playwright:
            prepare_dic = await self.prepare_files()
            print(prepare_dic)
            await self.upload(playwright, prepare_dic['title'], prepare_dic['video'])
