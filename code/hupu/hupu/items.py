# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 发帖人用户信息详细内容
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    others = scrapy.Field()
    location = scrapy.Field()
    reputation = scrapy.Field()
    rank = scrapy.Field()
    online_t = scrapy.Field()
    online_login = scrapy.Field()
    attention = scrapy.Field()
    following = scrapy.Field()
    visitor = scrapy.Field()
    topic = scrapy.Field()
    reply_t = scrapy.Field()
    fa = scrapy.Field()
    sex = scrapy.Field()
    money = scrapy.Field()
    club = scrapy.Field()

class HupuPostItem(scrapy.Item):
	# 帖子内容
	post_title = scrapy.Field()
	post_url = scrapy.Field()
	reply = scrapy.Field()
	light = scrapy.Field()
	view = scrapy.Field()
	content = scrapy.Field()
	client = scrapy.Field()
	uname = scrapy.Field()
	uurl = scrapy.Field()
	pub = scrapy.Field()
	second_id = scrapy.Field()
	reply_tiezi = scrapy.Field()

