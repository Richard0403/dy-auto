import json
import os

import requests
from bs4 import BeautifulSoup

class AudioDownload():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.tukuppt.com',
        'Referer': 'https://www.tukuppt.com/peiyueso/qingyinleshuhuan6318/__zonghe_0_0_0_0_0_0_2.html',
        'Cookie': 'hostfrom=www.baidu.com; yanzhenmakey=e17f0d8431; Hm_lvt_a620c01aafc084582f0ec24d96b73ad8=1682750203; c_mark=9639d9213d03b31ddf6697b505a89223; lastlogintype=2; auth_token=5kfXTrJXEjXGQ-6LygzwFHwFNgprGlscEQB6KsDI35dFDXt0oSnF6xLqOuqeoIlB1Zd_wunwl-IEqsYRQCvNqA; userkeyvaluetwo=1-0-0; Hm_lpvt_a620c01aafc084582f0ec24d96b73ad8=1682754617'
    }
    download_folder = "../DyMusic/"

    def start(self):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        for page in range(1, 7):
            start_url = 'https://www.tukuppt.com/peiyueso/qingyinleshuhuan6318/__zonghe_0_0_0_0_0_0_' + str(
                page) + '.html'
            html = requests.get(start_url, headers=self.headers).text
            bs = BeautifulSoup(html, "html.parser")
            music_tags = bs.find_all('i', {'class': 'icon-bofang'})
            print("页面-->" + start_url)
            for tag in music_tags:
                music_id = int(tag.get('value'))
                data = {'value': music_id}

                url = 'https://www.tukuppt.com/api/audio'

                music_info = requests.post(url, headers=self.headers, data=data).text
                resp_data = json.loads(music_info)['data']
                print(resp_data)
                music_url = resp_data['swf']
                music_path = self.download_folder + str(music_id) + ".mp3"
                if not os.path.exists(music_path):
                    r = requests.get(music_url)
                    if r.status_code == 200:
                        with open(music_path, 'wb') as fp:
                            fp.write(r.content)
                    else:
                        print("下载错误->" + str(music_path))
                else:
                    continue


if __name__ == '__main__':
    audio_download = AudioDownload()
    audio_download.start()