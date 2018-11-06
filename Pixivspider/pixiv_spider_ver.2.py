import requests
import re
import os
from time import sleep
from bs4 import  BeautifulSoup
se = requests.session()
class Pixiv():
    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.target_url = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=68910131"
        self.login_url = "https://accounts.pixiv.net/api/login?lang=zh"
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
                      "Referer":"https://www.pixiv.net/member_illust.php?mode=medium&illust_id=68910131"}
        self.pixiv_id = "783928876@qq.com"
        self.password = "****************"
        self.postkey = ""
        self.localpath = "D:\pixiv\spiderimage\\"
        self.return_to = "https://www.pixiv.net"
        self.image_name = ""

    def login(self):
        login_html = BeautifulSoup(se.get(self.base_url,headers = self.headers).text,'lxml')
        self.postkey = login_html.find("input",{"name":"post_key"})['value']
        data = {"pixiv_id": self.pixiv_id,
                "password": self.password,
                "post_key": self.postkey,
                "return_to": self.return_to}
        se.post(self.login_url,headers = self.headers,data = data)
        #登陆到pixiv，建立会话

    def get_html(self,url):
        html = se.get(url,headers = self.headers).text
        return BeautifulSoup(html,'lxml')
    #得到url的beautifulsoup对象

    def get_image(self,bsobj):
        image_src = bsobj.find("img",{"class":"original-image"})['data-src']
        return image_src

    def download_image(self,image_src,count):
        if  str(image_src).find("png") :
            expand_name = ".png"
        else:
            expand_name = ".jpg"

        self.image_name = str(count) + expand_name
        fp = open(self.localpath+self.image_name,'ab')
        img = requests.get(image_src,headers = self.headers)
        fp.write(img.content)
        fp.close()
    #将url = image_src 图片下载到 localpath 以计数为名

    def work(self):
        self.login()
        bsobj = self.get_html(self.target_url)
        pic = self.get_image(bsobj)
        print("start to download")
        self.download_image(pic,2)
        print("finished")
        sleep(2)

pixiv = Pixiv()
pixiv.work()








