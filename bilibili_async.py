# -*- coding: utf-8 -*-
# 用协程异步抓取B站视频信息，不能抓取只有会员可见视频的HTML
# B站视频信息获取          花费时间：100条 3.41s     1000条：36.57s

from urllib.error import HTTPError
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import time

# 限制并发数为50个
semaphore = asyncio.Semaphore(50)

# 通过API获取播放量、弹幕量等信息
async def getDetailData(aid):
    url = "http://api.bilibili.com/archive_stat/stat?aid=" + str(aid)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                Json_1 = await response.text(encoding='utf-8')
    except HTTPError:
        return None
    try:
        responseJson = json.loads(Json_1)
        view = responseJson.get("data").get("view")
        danmaku = responseJson.get("data").get("danmaku")
        reply = responseJson.get("data").get("reply")
        favorite = responseJson.get("data").get("favorite")
        coin = responseJson.get("data").get("coin")
        like = responseJson.get("data").get("like")
    except AttributeError as e:
        return None
    return (view, danmaku, like, reply, coin, favorite)



async def fetch(session, url):
    headers = {"User-Agent": "wswp"}
    async with session.get(url, headers=headers) as response:
        return await response.text(encoding='utf-8')

async def getVideo(video):
    # 抓取不到只有会员才能看的视频
    url = "https://www.bilibili.com/video/av" + str(video)
    try:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                html = await fetch(session, url)
                bsObj = BeautifulSoup(html, 'lxml')
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
    view, danmaku, like, reply, coin, favorite = await getDetailData(video)
    print("视频编号: " + str(video), flush=True)
    print("标题: " + title + "\t作者: " + author + "\tUID: " + str(uid), flush=True)
    print("播放量: " + str(view) + "\t弹幕: " + str(danmaku) + "\t喜欢: " + str(like), flush=True)
    print("评论: " + str(reply) + "\t硬币: " + str(coin) + "\t收藏: " + str(favorite), flush=True)
    print("", flush=True)
now = time.time()
loop = asyncio.get_event_loop()
tasks = [getVideo(i) for i in range(100)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print(time.time()-now)