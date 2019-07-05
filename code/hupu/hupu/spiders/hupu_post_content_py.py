# -*- coding: utf-8 -*-
import scrapy
import pymongo
from hupu.items import HupuPostItem
from scrapy.http import Request 
from bs4 import BeautifulSoup
import re
import requests
import pickle
import time
import logging

class HupuPostContentPySpider(scrapy.Spider):
    ''' 帖子内容'''
    name = 'hupu_p_c'
    allowed_domains = ['bbs.hupu.com']

    def start_requests(self):
        '''数据库调用'''
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient['hupu']
        mycol = mydb['posts_list']

        ss = mycol.find({})
        for i,s in enumerate(ss):
            if i>=45178: # i=56400,需手动查看 # 回帖抓取
                url = 'https://bbs.hupu.com'+ s['post_url']
                logging.log(logging.WARNING, "第 {} 个, url {}".format(i, url)) # 自己打log
                yield Request(url=url, callback=self.parse, meta={'sid':s['sencod_id']}, dont_filter=True)

    def parse(self, response):
        '''帖子信息'''
        soup = BeautifulSoup(response.body, features="lxml")
        item = HupuPostItem()
        da = {} # 帖子信息，高亮回帖信息
        gg = [] # 高亮回帖信息列表 
        # 1、帖子的基本信息
        # 考虑帖子删除情况
        if soup.find(class_="bbs-hd-h1") != None:
            post_title = soup.find(class_="bbs-hd-h1").h1.string # 帖子名
        else:
            item = {}
            yield item
        js = [j for j in soup.find(class_="bbs-hd-h1").span.stripped_strings] # 回复数、亮的数
        reply = re.findall(r'\d+',js[0])[0] # 回复数
        if len(js)>=3: # 判断是否有点亮数
            light = re.findall(r'\d+',js[1])[0] # 点亮数
        else:
            light = '未知'
        post_id = re.findall(r'\d+', response.url)[0]
        headers = {
    'cookie':'_dacevid3=33db0fc3.3460.94ca.9bea.9151267f9e6a; __gads=ID=8bea3097e4a615de:T=1560692438:S=ALNI_MbiTJt0Jl6jPoJd7rxc1gtrEgDMmA; _HUPUSSOID=0f199a6d-1ffb-4da0-a397-f363dc552acd; _CLT=00376064be821b71351c003dda774e37; ipfrom=2193718f766b3a86b2829667341e0c24%09Unknown; __dacevid3=0xd8a7eb830c9eb942; u=50553256|R2Fuamlu5a2m|f4e9|4f1d7c19561d40883ac4b6e87af96eff|561d40883ac4b6e8|aHVwdV8zOTRlNmU4Mzk3MjRjNGVl; us=c2131081e25ab9d60fbde179b6f394776cf81d3443db2e5bc37ade0918290e808a097b337a5ba2dcc492d468a15230e618678b19e502f075a6f99cfe5f67bb4d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b7349bd0b2df-0c7559a51281ed-76296132-48573-16b7349bd0c7be%22%2C%22%24device_id%22%3A%2216b7349bd0b2df-0c7559a51281ed-76296132-48573-16b7349bd0c7be%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; OUTFOX_SEARCH_USER_ID_NCOO=777894018.0133089; lastvisit=8328%091561015685%09%2Fajax%2Fcard.php%3Fuid%3D29473792%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F251704890813363%26fid%3D1048%26_%3D1561015685358; PHPSESSID=3d5987c864c66c4e5d328b8efd48560c; _cnzz_CV30020080=buzi_cookie%7C33db0fc3.3460.94ca.9bea.9151267f9e6a%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1561008392,1561011887,1561079847,1561083578; _fmdata=764F%2F%2FqcXyXFjLJcejYEOiBWe66dbHEJBdz1tv0NW5ureqbsjZ5qQivaB1i8ZY5WQEHGAUQx%2BDLZ3PMK0bnIvrmuAZgte1Y1UkNO43M3jo8%3D; ua=27387493; __dacevst=56836953.dbbf2c1c|1561089636743; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=' + str(int(time.time())),
    'user-agent':'chrome'}
        view = requests.get('https://msa.hupu.com/thread_hit?tid=' + post_id, headers=headers).text # 浏览数
        content = soup.find(class_="quote-content").text # 帖子内容
        if soup.find(class_="quote-content").small != None and '虎扑' in soup.find(class_="quote-content").small.text:
            client = soup.find(class_="quote-content").small.text # 使用客户端
        else:
            client = 'PC客户端'
        uname = soup.find(class_="author").div.a.string # 楼主名
        uurl = soup.find(class_="author").div.a["href"] # 个人空间链接
        pub = soup.find(class_="author").div.find(class_="stime").string # 楼主发帖时间
        # 高亮回帖的基本信息
        da['post_title'] = post_title
        da['post_url'] = response.url
        da['reply'] = reply
        da['light'] = light
        da['view'] = view
        da['content'] = content
        da['client'] = client
        da['uname'] = uname
        da['uurl'] = uurl
        da['pub'] = pub
        da['second_id'] = response.meta['sid']
    #     print('帖子的基本信息：',post_title, reply,light,view,content,client,uname,uurl,pub)
        # 2 回帖信息
        if soup.find(id="readfloor") != None: # # print(soup.find(id="highlights").string) # 判断是否有 亮了的回帖标签
            for wr in soup.find(id="readfloor"): # 亮了的回复
                dad = {}
                if len(wr) != 1: # 去除空格影响
                    u_reply = wr.find(class_="u").string # 评论人
                    u_reply_url = wr.find(class_="u")['href'] # 评论人空间链接
                    pub_reply = wr.find(class_="left").find(class_="stime").string # 回帖时间
                    print(pub_reply)
                    hight2 = wr.find(class_="ilike_icon_list").find(class_="stime").string # 点亮数
                    reply_content = wr.find(class_="case").tbody.tr.td # 评论内容，是否引用、
                    if wr.find(class_="case").find(class_="f999") != None: # 判断 PC 与手机客户端
                        client2 = wr.find(class_="case").find(class_="f999").string # 使用的客户端
                    else:
                        client2 = 'PC客户端'
                    dad['u_reply'] = u_reply
                    dad['u_reply_url'] = u_reply_url
                    dad['pub_reply'] = pub_reply
                    dad['hight2'] = hight2
                    dad['reply_content'] = str(reply_content)
                    dad['client2'] = client2
                    gg.append(dad)
    #                 print("\n 高亮回帖的基本信息：",u_reply, u_reply_url, pub_reply, hight2, reply_content,client2)
        da['reply_tiezi'] = gg # 何为一个字典
        item = da
        yield item
