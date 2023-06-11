# -*- coding: utf-8 -*-

import json
import math
import os
import re

import requests
from tqdm import tqdm


class PicDownload:
    header = {'User-Agent': 'picasso,316,xiaomi'}
    # max 490
    album_skip = 0
    album_pic_skip = 0
    start_url = 'http://service.picasso.adesk.com/v2/vertical/album?limit=10&skip=' + str(
        album_skip) + '&adult=true&first=1&order=new'

    def start(self, url):
        print()
        album_str = requests.get(url, headers=self.header).text
        print("开始获取专辑列表->" + url)
        album_dic = json.loads(album_str)
        albums = album_dic['res']['album']
        if albums is not None:

            for i in range(0, len(albums)):
                album = albums[i]
                album_id = album['id']
                album_pic_count = int(album['count'])
                # 去除非法字符，只保留中英文和数字
                album_name = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', str(album['name']))
                folder = '../DyPic/' + album_name
                if not os.path.exists(folder):
                    os.makedirs(folder)
                print("开始下载专辑->" + folder + ",共" + str(album_pic_count))
                self.album_pic_skip = 0

                temp_page = math.ceil(album_pic_count / 30)
                # 最多获取8页
                album_pic = temp_page if temp_page < 7 else 7

                for j in range(0, album_pic):
                    first = 1 if (j == 0) else 0
                    album_url = 'http://service.picasso.adesk.com/v1/vertical/album/' + \
                                str(album_id) + \
                                '/vertical?limit=30&skip=' + str(self.album_pic_skip) + '&adult=false&first=' + str(
                        first) + '&order=new'
                    print(album_url)
                    album_detail_str = requests.get(album_url, headers=self.header).text
                    album_detail_dic = json.loads(album_detail_str)
                    pic_array = album_detail_dic['res']['vertical']

                    for k in range(0, len(pic_array)):
                        pic = pic_array[k]
                        pic_url = pic['wp']

                        pic_name = "%04d" % (k + self.album_pic_skip)
                        pic_path = folder + '/pic_' + pic_name + '.jpeg'

                        if not os.path.exists(pic_path):
                            r = requests.get(pic_url)
                            if r.status_code == 200:

                                with open(pic_path, 'wb') as fp:
                                    fp.write(r.content)
                            else:
                                print("下载错误->" + str(folder) + "-->" + str(k))
                        else:
                            continue
                    self.album_pic_skip += 30


            self.album_skip += 10
            next_url = 'http://service.picasso.adesk.com/v2/vertical/album?limit=10&skip=' + str(
                self.album_skip) + '&adult=false&first=0&order=new'
            self.start(next_url)
        pass


if __name__ == '__main__':
    app = PicDownload()
    app.start(app.start_url)
