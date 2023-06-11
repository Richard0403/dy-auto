import re


# with open("temp_text.txt", "r", encoding="utf-8") as f:
#     text = f.read()
# # 使用数字和'、'进行分割
# segments = re.split(r'\d+、', text)[1:]
#
# # 将分割后的字符串写入文件
# with open("beauty_text.txt", "w", encoding="utf-8") as f:
#     for index, content in enumerate(segments, 0):
#         f.write(f"{content.strip()}\n")


import requests

url = 'https://www.tukuppt.com/api/audio'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.tukuppt.com',
    'Referer': 'https://www.tukuppt.com/peiyueso/qingyinleshuhuan6318/__zonghe_0_0_0_0_0_0_6.html',
}
data = {'value': '9016122'}
response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    print(response.json())
else:
    print(f'Request failed with status code: {response.status_code}')


