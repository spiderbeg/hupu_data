# -*- coding: utf-8 -*-
import time
import datetime
import scrapy

# Scrapy settings for hupu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hupu'

SPIDER_MODULES = ['hupu.spiders']
NEWSPIDER_MODULE = 'hupu.spiders'


# mongo
MONGO_URI = 'localhost'
MONGO_DATABASE = 'hupu'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Chrome'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False # 表示使用 settings 中的 cookie ,而不是自己自定义的cookie

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
	'cookie':'_dacevid3=33db0fc3.3460.94ca.9bea.9151267f9e6a; __gads=ID=8bea3097e4a615de:T=1560692438:S=ALNI_MbiTJt0Jl6jPoJd7rxc1gtrEgDMmA; _HUPUSSOID=0f199a6d-1ffb-4da0-a397-f363dc552acd; _CLT=00376064be821b71351c003dda774e37; ipfrom=2193718f766b3a86b2829667341e0c24%09Unknown; __dacevid3=0xd8a7eb830c9eb942; u=50553256|R2Fuamlu5a2m|f4e9|4f1d7c19561d40883ac4b6e87af96eff|561d40883ac4b6e8|aHVwdV8zOTRlNmU4Mzk3MjRjNGVl; us=c2131081e25ab9d60fbde179b6f394776cf81d3443db2e5bc37ade0918290e808a097b337a5ba2dcc492d468a15230e618678b19e502f075a6f99cfe5f67bb4d; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b7349bd0b2df-0c7559a51281ed-76296132-48573-16b7349bd0c7be%22%2C%22%24device_id%22%3A%2216b7349bd0b2df-0c7559a51281ed-76296132-48573-16b7349bd0c7be%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; OUTFOX_SEARCH_USER_ID_NCOO=777894018.0133089; lastvisit=8328%091561015685%09%2Fajax%2Fcard.php%3Fuid%3D29473792%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F251704890813363%26fid%3D1048%26_%3D1561015685358; PHPSESSID=3d5987c864c66c4e5d328b8efd48560c; _cnzz_CV30020080=buzi_cookie%7C33db0fc3.3460.94ca.9bea.9151267f9e6a%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1561008392,1561011887,1561079847,1561083578; _fmdata=764F%2F%2FqcXyXFjLJcejYEOiBWe66dbHEJBdz1tv0NW5ureqbsjZ5qQivaB1i8ZY5WQEHGAUQx%2BDLZ3PMK0bnIvrmuAZgte1Y1UkNO43M3jo8%3D; ua=27387493; __dacevst=56836953.dbbf2c1c|1561089636743; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=' + str(int(time.time())),
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'hupu.middlewares.HupuSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'hupu.middlewares.HupuDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'hupu.pipelines.HupuPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# log 文件
LOG_LEVEL = 'WARNING'
to_day = datetime.datetime.now()
log_file_path = 'log/scrapy_{}_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day, time.time())
LOG_FILE = log_file_path
