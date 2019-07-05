# -*- coding: utf-8 -*-
import scrapy
from hupu.items import HupuItem
from scrapy.http import Request # 调用请求
from bs4 import BeautifulSoup
import re
import pymongo 
import logging

class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['my.bbs.com']

    def start_requests(self):
        # '''数据库调用'''
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient['hupu']
        mycol = mydb['posts_detail']
        myhp = mydb['reply_user']
        ss = mycol.find({}) # 游标的移动
        urls = {} 
        user = {}
        bb = myhp.find({})
        for b in bb:
            if b['user_url'] not in user:
                user[b['user_url']] = b['user_url']
        use = []
        for i,s in enumerate(ss):
            for a in s['reply_tiezi']:
                # print(a['u_reply_url'])
                if a['u_reply_url'] not in user and a['u_reply_url'] not in urls:
                    urls[a['u_reply_url']] = a['u_reply_url'] # 生成查重字典
                    use.append(a['u_reply_url'])
        print("总数", len(use))
        for i,u in enumerate(use):
            print(i, end="")
            logging.log(logging.WARNING, "总数 {} 个, 第 {} 个链接 {} 呀".format(len(use), i, u)) # 自己打log
            yield Request(url=u, callback=self.parse, dont_filter=True)
        # yield Request(url='https://my.hupu.com/7573392087578', callback=self.parse, dont_filter = True) # test
                
    def parse(self, response):
        # print('one')
        soup = BeautifulSoup(response.body, features="lxml")
        uinfo = {} # item 实例化
        
        uinfo['user_name'] = [un for un in soup.find(class_="mpersonal").div.stripped_strings][0]
        uinfo['user_url'] = response.url
        #----------------------------------------------------------------
    #     url = 'https://my.hupu.com/152491179224503' # 空间首页
        # 声望、等级、、在线时间、加入时间、社团
        if soup.find(class_="personalinfo")==None:
            print('Not Exist')
            return None
        ss = [j for j in soup.find(class_="personalinfo").stripped_strings]
        uinfo['others'] = ss
        la,lb = 1,1
        online_t = '0' # 有的不存在在线时长
        for ind,ssd in enumerate(ss):
            if '社区声望：' == ssd:
                reputation = ss[ind+1]
            elif '社区等级：' == ssd:
                rank = ss[ind+1]
            elif '在线时间：' == ssd:
                online_t = ss[ind+1]
            elif '加入时间：' == ssd:
                online_login = ss[ind+1]
            if '所\xa0\xa0在\xa0\xa0地：' == ssd and lb == 1:
                location = ss[ind+1]
                lb += 1
            elif lb == 1:
                location = 'unkonwn'
 
        uinfo['location'] = location
        uinfo['reputation'] = reputation
        uinfo['rank'] = rank
        uinfo['online_t'] = online_t
        uinfo['online_login'] = online_login
        # 关注数、粉丝数
        if soup.find(id="sidebar").p != None:
            af = [c for c in soup.find(id="sidebar").p.stripped_strings]# 关注数、粉丝数
            af1,af2 = 1,1
            for c in af:
                if '关注' in c and af1 == 1 and '此人' not in c:
                    attention = re.findall(r'\d+',c)[0]
                    af1+=1
                elif af1 == 1:
                    attention = 0
                if '粉丝' in c and af2 == 1:
                    following = re.findall(r'\d+',c)[0]
                    af2+=1
                elif af2 == 1:
                    following = 0
        else:
            attention,following = 0,0
        # 访问人数
        visitor = re.findall(r'\d+',soup.find(class_='mpersonal').find(class_='f666').string)[0]

        uinfo['attention'] = attention
        uinfo['following'] = following
        uinfo['visitor'] = visitor
        

        #--------------------------------主题数、回帖数、收藏数-----------------------------------------
        url2 = response.url + '/topic' # 空间发帖、回帖页面
        yield Request(url2, callback = self.get_huitie, meta={'uinfo':uinfo}, dont_filter = True) # dont_filter = True

    def get_huitie(self, response):
        '''空间发帖、回帖页面'''
        # print('two')
        soup = BeautifulSoup(response.body, features="lxml")
        uinfo = response.meta['uinfo']
        # test
        if soup.find(class_="tabs_header")==None:
            print('123123132', uinfo['user_url'], soup)
        tt = [ti for ti in soup.find(class_="tabs_header").stripped_strings]
        taa = 1
        for t1 in tt:
            if '主题' in t1:
                topic = re.findall(r'\d+',t1)[0]
            elif '回帖' in t1:
                reply_t = re.findall(r'\d+',t1)[0]
            if '收藏' in t1 and taa==1:
                fa = re.findall(r'\d+',t1)[0]
                taa+=1
            elif taa == 1:
                fa = 0
    #     print(topic,reply_t,fa)
        uinfo['topic'] = topic
        uinfo['reply_t'] = reply_t
        uinfo['fa'] = fa
        #---------------------------------------------性别
        url3 = uinfo['user_url'] + '/profile' # 档案页面
        yield Request(url3, callback = self.get_sex, meta={'uinfo':uinfo}, dont_filter = True)
    def get_sex(self, response):
        '''性别、社团、银行现金卡路里'''
        # print('three')
        uinfo = response.meta['uinfo']
        item = HupuItem() # item 实例化
        soup = BeautifulSoup(response.body, features="lxml")
        ssi = [si for si in soup.find(id="content").stripped_strings]
        for s,si in enumerate(ssi): # 性别银行现金
            if '性别：' == si:
                sex = ssi[s+1]
            elif '银行现金：' == si:
                money = ssi[s+1]
            elif '所属社团：' == si:
                club = ssi[s+1]
    #     print(sex,money,club)
        uinfo['sex'] = sex
        uinfo['money'] = money
        uinfo['club'] = club
        # print(uinfo)
        item = uinfo

        yield item # 返回item

