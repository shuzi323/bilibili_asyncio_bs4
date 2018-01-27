# B站视频信息单线程获取       花费时间：36.35s
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import json
import time

def getVideo(url):
    #抓取不到只有会员才能看的视频
    try:
        session = requests.Session()
        headers = {"User-Agent": "wswp"}
        req = session.get(url, headers=headers)
        bsObj = BeautifulSoup(req.text, 'lxml')
    except HTTPError as e:
        return None
    try:
        author = bsObj.head.find("meta", {"name":"author"})["content"]
        title = bsObj.body.find("div", {"class":"v-title"}).get_text()
        uid = bsObj.body.find("div", {"class":"usname"}).find("a", {"class":"name"})["mid"]
    except AttributeError as e:
        return None
    except TypeError as e:
        return None
    print("标题: "+ str(title) + "\t作者: " + str(author) + "\tUID: " +str(uid), flush=True)

def getVideoData(aid):
    url = "http://api.bilibili.com/archive_stat/stat?aid=" + str(aid)
    try:
        response = urlopen(url).read().decode("utf-8")
    except HTTPError:
        return None
    try:
        responseJson = json.loads(response)
        view = responseJson.get("data").get("view")
        danmaku = responseJson.get("data").get("danmaku")
        reply = responseJson.get("data").get("reply")
        favorite = responseJson.get("data").get("favorite")
        coin = responseJson.get("data").get("coin")
        like = responseJson.get("data").get("like")
    except AttributeError as e:
        return None
    print("播放量: " + str(view) + "\t弹幕: " + str(danmaku) + "\t喜欢: " +str(like), flush=True)
    print("评论: " + str(reply) + "\t硬币: " + str(coin) + "\t收藏: " + str(favorite), flush=True)
    
    
    

if __name__ == '__main__':
    now = time.time()
    for i in range(100):
        url = url = "https://www.bilibili.com/video/av" + str(i)
        print("视频编号: " + str(i), flush=True)
        getVideo(url)
        getVideoData(i)
        print("", flush=True)
    print("时间：" + str(time.time()-now))

        
