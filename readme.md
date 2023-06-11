
<h1 align="center">dy-auto</h1>

<p align="center"><h2 align="center">✨ 抖音自动生成视频、字幕、自动上传发布✨</h2></p>
<p align="center">
<a href="https://github.com/Richard0403/dy-auto/dy-auto/LICENSE">
<img src="https://img.shields.io/badge/license-MIT-blue.svg">
</a>
<a href="https://github.com/Richard0403/dy-auto">
<img src="https://img.shields.io/badge/python-v3.10.11-orange">
</a></p>
<p align="center">
<a href="https://github.com/Richard0403/dy-auto">
<img src="https://img.shields.io/github/stars/Richard0403/dy-auto?style=social">
</a>
<a href="https://github.com/Richard0403/dy-auto">
<img src="https://img.shields.io/github/forks/Richard0403/dy-auto?style=social">
</a>
<a href="https://github.com/Richard0403/dy-auto">
<img src="https://img.shields.io/github/issues/Richard0403/dy-auto?style=social">
</a>
<a href="https://github.com/Richard0403/dy-auto">
<img src="https://img.shields.io/github/issues-closed/Richard0403/dy-auto?style=social">
</a></p>

## 录屏效果

https://github.com/Richard0403/dy-auto/assets/14147304/21400a42-9296-4956-9517-ced8d8bf4737

## 技术架构
| 名称             | 功能                  |
|----------------|---------------------|
| ffmpeg         | 处理视频的生成，语音添加，字幕的添加等 | 
| 微软SpeechStudio | 文字合成语音              |
| whisper        | 语音生成字幕              |
| jieba3k    | 用于文案的关键词提取          |
| playwright    | 用于自动化操作             |

## 项目结构


```
|-- DyPic                                      // 图片资源目录
|   |-- 建筑集                                  // 图片组1
|   |   |-- pic_0001.jpeg                     // 图片命名规则
|   |   |-- pic_0002.jpeg                     // 图片命名规则
|   |-- 可爱小动物                              // 图片组2
|   |   |-- pic_0001.jpeg                     // 图片命名规则
|   |   |-- pic_0002.jpeg                     // 图片命名规则
|-- DyText                                    // 文案文件夹
|   |-- 6_躺平真的会毁掉年轻人吗？.txt             // 文案话题(txt内部的见解用#分割)
|-- dy_auto                                    // 代码目录
|   |-- main.py 主程序入口
```
## 使用教程

1. 环境配置
    * python 3.10.11
    * ffmpeg 安装
2. 账号注册 
    * 微软speech studio， [注册入口](https://speech.microsoft.com/portal)
    * 拿到资源密钥和地区名称， 填入[speech_voice_gen.py](speech_voice_gen.py) 的speech_key 和 service_region字段中
3. 安装依赖库
   * pip install -r requirements.txt
4. 准备图片和文案资源(项目文件结构见下文)
   * 文件夹准备： 在项目文件夹同级，新建DyTemp、DyText、DyPic文件夹
   * 图片资源: 格式见目录DyPic
   * 文案资源: 格式见目录DyText
5. 获取token
   * 先执行该命令，扫码登录，成功后关闭浏览器， 会自动保存cookie
   ```
   playwright codegen www.douyin.com --save-storage=cookie.json
   ``` 
5. 运行
   * 程序运行入口 main.py



## 项目执行流程
![img](https://github.com/Richard0403/dy-auto/assets/14147304/1101bc20-4d80-4a6f-9103-babfe5982299)

## 注意 
**1.文案和图片的使用是随机获取的**

**2. whisper运行默认不使用GPU,为了使用GPU, 安装如下依赖**
```
pip uninstall torch 
pip cache purge 
pip install torch -f https://download.pytorch.org/whl/torch_stable.html
```
3. **可实现多个账号循环上传**

## 声明
<h3>本项目只做个人学习研究之用，不得用于商业用途！</h3>
