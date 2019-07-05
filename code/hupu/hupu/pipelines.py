# -*- coding: utf-8 -*-
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 顺序执行 pipline 

class HupuPipeline(object):
    ''' MongoDB 储存用户信息'''

    collection_name = 'reply_user'
    collection_name1 = 'detail'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'user': # user 爬虫
            if self.db[self.collection_name].find_one({'user_url':dict(item)['user_url']}):
                print('已存在, ', end="")
            else:
                # self.db[self.collection_name].insert_one(dict(item))
                print('0k1', end='')
            return item
        elif spider.name == 'hupu_p_c': # 爬虫 hupu_p_c
            if self.db[self.collection_name1].find_one({'post_url':dict(item)['post_url']}):
                print('已存在, ', end="")
            elif len(dict(item)) == 0:
                print('帖子已被删除', end="")
            else:
                self.db[self.collection_name1].insert_one(dict(item))
                print('0k2', end='')
            return item
