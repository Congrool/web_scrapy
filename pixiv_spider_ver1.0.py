import requests
import re
import os
from time import sleep
from bs4 import  BeautifulSoup
se = requests.session()
class Pixiv():
    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.target_url = "https://www.pixiv.net/search.php?s_mode=s_tag_full&word=%E3%82%A2%E3%82%BA%E3%83%BC%E3%83%AB%E3%83%AC%E3%83%BC%E3%83%B3"
        self.login_url = "https://accounts.pixiv.net/api/login?lang=zh"
        self.headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
                      "Referer":"https://www.pixiv.net/member_illust.php?mode=medium&illust_id=68910131"}
        self.pixiv_id = "783928876@qq.com"
        self.password = "****************"
        self.postkey = ""
        self.localpath = "D:\pixiv\spiderimage\\"
        self.return_to = "https://www.pixiv.net"
        self.image_name = ""
        self.urllist = []
        self.Idlist = []
        self.next_page = ""
#########################################################################################################
    def login(self):
        login_html = BeautifulSoup(se.get(self.base_url,headers = self.headers).text,'lxml')
        self.postkey = login_html.find("input",{"name":"post_key"})['value']
        data = {"pixiv_id": self.pixiv_id,
                "password": self.password,
                "post_key": self.postkey,
                "return_to": self.return_to}
        se.post(self.login_url,headers = self.headers,data = data)
        #登陆到pixiv，建立会话

#########################################################################################################
    def get_web_bs(self,url):
        html = se.get(url,headers = self.headers).text
        html_bsobj = BeautifulSoup(html,'lxml')
        return html_bsobj
    #得到url的beautifulsoup对象

#*******************************************************************************************************
#以上是连接函数
#-------------------------------------------------------------------------------------------------------

    def get_id_list(self,tarbs):
        IDlist = []
        target_input = tarbs.find('input', {'data-items': re.compile('.*')})
        data_items = str(target_input['data-items'])
        i = 0
        end = len(data_items)
        while i != -1 :         #得到网页上图片id
            i = data_items.find("illustId",i,end)
            if i == -1:
                break
            ID = data_items[i+11:i+19]
            if IDlist.count(ID) == 0:       #去重
                IDlist.append(ID)
            i = i+1
        for vip_pic in tarbs.find_all('img',{'class':"_thumbnail ui-scroll-view"}):     #得到热门图片id
            if IDlist.count(vip_pic['data-id']) == 0:
                IDlist.append(vip_pic['data-id'])
        return IDlist

    def id_to_url(self,IDlist):
        for id in IDlist:
            self.urllist.append("https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+str(id))

    def get_pic_url(self,tarbs):
        self.Idlist = self.get_id_list(tarbs)
        self.id_to_url(self.Idlist)                     #得到图片网页的url 存在urllist里面
#-----------------------------------------------------------------------------------------------------
    def get_image_src(self,bsobj):
        tag = bsobj.find("img",{"class":"original-image"})
        image_src = []
        image_src.append(tag['data-src'])
        return image_src

    def get_manga_src(self,bsobj):
        url = str(bsobj.find("a", {"class": " _work multiple "})['href'])
        manga_url = "https://www.pixiv.net/" + url
        self.headers["Referer"] = manga_url
        manga_bs = self.get_web_bs(manga_url)
        manga_tag = manga_bs.find_all('img',{"class":"image ui-scroll-view"})
        manga_src = []
        for src in manga_tag:
             manga_src.append(src['data-src'])
        return manga_src
#-----------------------------------------------------------------------------------------------------
    def url_filter(self,bsobj):
        view_count = int(bsobj.find("dd",{"class":"view-count"}).get_text())
        rated_count = int(bsobj.find("dd",{"class":"rated-count"}).get_text())
        if rated_count == 0:
            return 0
        else:
            percent = float(view_count)/float(rated_count)
            return percent
        # 过滤器

    def download_image(self,image_src,image_name):
        print("begin to connect")
        img = requests.get(image_src,headers = self.headers,timeout = 10)
        print(image_src)
        file_name = self.localpath + image_name
        fp = open(file_name, 'ab')
        print("begin to download")
        fp.write(img.content)
        fp.close()
        print("download successfully")
        #将url = image_src 图片下载到 localpath 以计数为名

    def get_image_name(self,image_src):
        image_src = str(image_src)
        end = len(image_src)
        if image_src.find("png",0,end):
            expand_name = ".png"
        else:
            expand_name = ".jpg"
        i = image_src.find("/img/",0,end)
        image_name = image_src[i+25:i+36] + expand_name
        return image_name


    def work(self):
        self.login()
        page = 1       #页数
        self.headers[
            "Referer"] = "https://www.pixiv.net/search.php?s_mode=s_tag_full&word=%E3%82%A2%E3%82%BA%E3%83%BC%E3%83%AB%E3%83%AC%E3%83%BC%E3%83%B3"
        while page <= 5:
            web_bs = self.get_web_bs(self.target_url)
            self.get_pic_url(web_bs)
            self.next_page = "https://www.pixiv.net/search.php" + str(web_bs.find("a", {"class": "gtm-search-pager-bottom"})['href'])
            print("begin to get image src")
            image_count = 0
            for url in self.urllist:
                bsobj = self.get_web_bs(url)
                percent = self.url_filter(bsobj)
                if percent < 0.07 :
                    pass
                else:
                    try:
                        image_list = self.get_image_src(bsobj)
                        for image_src in image_list:
                            image_name = self.get_image_name(image_src)
                            self.download_image(image_src, image_name)
                            print("try to download image",image_count)
                            image_count = image_count + 1
                    except:
                        try:
                            manga_list = self.get_manga_src(bsobj)
                            for image_src in manga_list:
                                image_name = self.get_image_name(image_src)
                                self.download_image(image_src, image_name)
                                print("try to download image", image_count)
                                image_count = image_count + 1
                        except:
                            pass
                sleep(3)
            self.target_url = self.next_page
            self.headers['Referer'] = self.next_page
            print("page ",image_count," has finished")
            print("next page is ",self.next_page )
            page = page + 1


pixiv = Pixiv()
pixiv.work()


