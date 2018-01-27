# bilibili视频信息多进程获取     花费时间：8.91s
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import json
from multiprocessing import Pool
import time

def getVideo(aid):
    #抓取不到只有会员才能看的视频
    url = url = "https://www.bilibili.com/video/av" + str(aid)
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
    view, danmaku, like, reply, coin, favorite = getVideoData(aid)
    print("视频编号: " + str(aid), flush=True)
    print("标题: "+ str(title) + "\t作者: " + str(author) + "\tUID: " +str(uid), flush=True)
    print("播放量: " + str(view) + "\t弹幕: " + str(danmaku) + "\t喜欢: " + str(like), flush=True)
    print("评论: " + str(reply) + "\t硬币: " + str(coin) + "\t收藏: " + str(favorite), flush=True)
    print("", flush=True)


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
    return (view, danmaku, like, reply, coin, favorite)
    
    
    

if __name__ == '__main__':
    now = time.time()
    p = Pool(4)
    for aid in range(100):
        p.apply_async(getVideo, args=(aid,))
    p.close()
    p.join()
    print("时间：" + str(time.time()-now))

        
