# date:2018/5/26
# 抓取pixiv静态网页上的特定图片
# 并保存在本地
import requests
from bs4 import BeautifulSoup
import re
import os
session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"  ,
           "Referer":"https://www.pixiv.net/member_illust.php?mode=medium&illust_id=57467838"}
url = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=57467838"
html = requests.get(url,headers = headers).text
bsobj = BeautifulSoup(html,"lxml")
picurl = bsobj.find_all("img",src = re.compile(r'^https://i.pximg.net/.*?2016/06/18/21/.*?(jpg|pgn)$'))
for a in picurl:
    print(a)
if not os.path.exists("D:\pixiv\spiderimage"):
    os.makedirs("D:\pixiv\spiderimage")
i = 0
for url in picurl :
    img = url['src']
    try:
        pic = requests.get(img,timeout = 5)
    except:
        print("can't download")
        continue;
    file_name = str(i) + ".jpg"
    print(file_name)
    fp = open("D:\pixiv\spiderimage\\"+ file_name,'wb')
    fp.write(pic.content)
    fp.close()
    i+=1
