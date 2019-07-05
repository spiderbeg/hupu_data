# 尝试抓取各板块页面数据 表：hupu_plate
import random
import pymongo
import pickle
import time
from bs4 import BeautifulSoup
import requests
import re

def get_ready(ch='classify',dbname='hupu'):
    '''数据库调用'''
    global mycol, myclient,myhp
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[dbname]
    mycol = mydb[ch]
    myhp = mydb['plates']
get_ready()
ssd2 = mycol.find({}) # 一级分类
ssd = [s['url'] for s in ssd2]

headers = {
    'cookie':'_dacevid3=33db0fc3.3460.94ca.9bea.9151267f9e6a; __gads=ID=8bea3097e4a615de:T=1560692438:S=ALNI_MbiTJt0Jl6jPoJd7rxc1gtrEgDMmA; _HUPUSSOID=0f199a6d-1ffb-4da0-a397-f363dc552acd; _CLT=00376064be821b71351c003dda774e37; ipfrom=2193718f766b3a86b2829667341e0c24%09Unknown; __dacevid3=0xd8a7eb830c9eb942; u=50553256|R2Fuamlu5a2m|f4e9|4f1d7c19561d40883ac4b6e87af96eff|561d40883ac4b6e8|aHVwdV8zOTRlNmU4Mzk3MjRjNGVl; us=c2131081e25ab9d60fbde179b6f394776cf81d3443db2e5bc37ade0918290e808a097b337a5ba2dcc492d468a15230e618678b19e502f075a6f99cfe5f67bb4d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b7349bd0b2df-0c7559a51281ed-76296132-48573-16b7349bd0c7be%22%2C%22%24device_id%22%3A%2216b7349bd0b2df-0c7559a51281ed-76296132-48573-16b7349bd0c7be%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; OUTFOX_SEARCH_USER_ID_NCOO=777894018.0133089; lastvisit=8328%091561015685%09%2Fajax%2Fcard.php%3Fuid%3D29473792%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F251704890813363%26fid%3D1048%26_%3D1561015685358; PHPSESSID=3d5987c864c66c4e5d328b8efd48560c; _cnzz_CV30020080=buzi_cookie%7C33db0fc3.3460.94ca.9bea.9151267f9e6a%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1561008392,1561011887,1561079847,1561083578; _fmdata=764F%2F%2FqcXyXFjLJcejYEOiBWe66dbHEJBdz1tv0NW5ureqbsjZ5qQivaB1i8ZY5WQEHGAUQx%2BDLZ3PMK0bnIvrmuAZgte1Y1UkNO43M3jo8%3D; ua=27387493; __dacevst=56836953.dbbf2c1c|1561089636743; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=' + str(int(time.time())),
    'user-agent':'chrome'}

nono = []
dada = []
# with open(r'C:\Users\yc\Desktop\tiezi_url.txt', 'rb') as f:
#     dada = pickle.load(f)
for ij,s in enumerate(ssd): # 二级分类
    if ij<221: # 104 步行街
        continue
    if ij==107: 
        p=1040 
    else:
        p = 1
    print('板块下分类：', s, '板块', ij)
    while True: 
        print('页数：', p)
        if p == 1:
            url = 'https:' + s
        else:
            url = 'https:' + s + '-' + str(p) 
        r = requests.get(url, headers=headers) # 请求板块页面帖子列表  
        r.encoding = 'utf8'
        time.sleep(0.5)
        soup = BeautifulSoup(r.text)
        
        p+=1 # 页数加 1 
#         if p>2: 
#             break
        # 帖子信息：帖子名、作者、发布时间、回复数、浏览数
        res = soup.find(class_='for-list')
        try: # 登录状态失效，会出现问题
            if len(res) == 1: # 页面没有帖子则退出
                break
        except:
            print(res,',',soup)
        for i,b in enumerate(res): 
            print('个数：',i, end='') # 贴子数
            if len(b) != 1: # 去掉其中空格影响
                da = {}
                user_url = b.find(class_='author box').a['href'] # 发帖人地址
                user_name = b.find(class_='author box').a.string # 用户名
                if user_name==None: continue
                js = [j for j in b.find(class_='author box').stripped_strings] # 发帖人，发帖时间
                pub = js[1] # 发帖时间
                post_url = b.find(class_="truetit")["href"] # 帖子地址
                post = b.find(class_="truetit").string # 帖子名
                cly = b.div.a.string # 帖子分类 话题
                light = b.find(class_="light_r") # 亮了
                if light==None:
                    da['light'] = None
                else:
                    da['light'] = re.findall(r'\d+',light.a['title'])[0]
#                     print('亮了',re.findall(r'\d+',light.a['title'])[0])
                cs = [c.replace('\xA0','') for c in b.find(class_="ansour box").string.split('/') ] # 回复数、浏览数
                reply = cs[0]
                view = cs[1]
                da['sencod_id'] = s
                da['user_url'] = user_url
                da['user_name'] = user_name
                da['pub'] = pub
                da['post_url'] = post_url
                da['post'] = post
                da['cly'] = cly
                da['reply'] = reply
                da['view'] = view
                if post_url not in dada:
                    dada.append(post_url)
                    myhp.insert_one(da) # 存在则更新，没有则插入
