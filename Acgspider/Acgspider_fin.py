#半天写完的一只小爬虫
#代码还是一样的差
#和之前的Pixiv爬虫在技术上并没有新意
#目的是爬取资源网站的网盘url和提取密码
import requests
from time import sleep
from bs4 import BeautifulSoup
se = requests.session()
class Acgpy():
    def __init__(self):
        self.wpxurl = "https://www.acgpy.net/wpx"
        self.comic_url = "https://www.acgpy.net/wpx/category/%e6%bc%ab%e7%94%bb%e5%8c%ba"
        self.anime_url = "https://www.acgpy.net/wpx/category/%e5%8a%a8%e7%94%bb%e5%8c%ba"
        self.game_url = "https://www.acgpy.net/wpx/category/%e6%b8%b8%e6%88%8f"
        self.headers = {"Referer" : "https://www.acgpy.net/",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
           }
        self.password = []
        self.pan_url = []

    def getbs(self,url):
        bs4 = BeautifulSoup(se.get(url,headers = self.headers).text,'lxml')
        return bs4
		
    def get_second_url(self,bs4):
        article = bs4.find_all('article')
        second_url = []
        for art in article:
            href = art.find('a').get('href')
            second_url.append(href)
        return second_url

    def get_pan_url(self,second_url):
        for url in second_url:
            second_bs4 = BeautifulSoup(requests.get(url).text,'lxml')
            thurl = second_bs4.find('a',{'class': 'downbtn'}).get('href')
            self.get_panurl_and_password(thurl)
            sleep(3)

    def get_panurl_and_password(self,third_url):
        third_bs4 = BeautifulSoup(requests.get(third_url).text,'lxml')
        pan_url = third_bs4.find('div',{'class':'list'}).a.get('href')
        password = third_bs4.find('span',string = "提取码: ").next_sibling.text
        print(pan_url,"          提取码： ", password)
        sleep(3)

    def turn_to_next_pageurl(self,bs4,page):
        next_url = bs4.find('a',{'class' : 'page','title': page}).get('href')
        return next_url


    def work(self):
        page = 1
        url = "https://www.acgpy.net/wpx/category/%e6%bc%ab%e7%94%bb%e5%8c%ba"
        while page < 50:
            bs4 = self.getbs(url)
            second_url = self.get_second_url(bs4)
            self.get_pan_url(second_url)
            page = page + 1
            url = self.turn_to_next_pageurl(bs4,page)
            print("————————————————PAGE ", page, "————————————————")
            sleep(3)

Acg = Acgpy()
Acg.work()
