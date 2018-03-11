# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_id = scrapy.Field()  # 微博内容id
    content = scrapy.Field() #微博内容
    attitudes_count = scrapy.Field() #赞数
    comments_count = scrapy.Field() #评论数
    reposts_count = scrapy.Field() #转发数
    weibo_url = scrapy.Field() #微博的url
    video_views = scrapy.Field() #微博视频的观看次数
    video_url = scrapy.Field() #微博视频的url
    source = scrapy.Field() #微博的来源
    created_at = scrapy.Field() #发表的时间
    crawl_time = scrapy.Field() #爬取的时间

    source_id = scrapy.Field() #源区微博id
    source_user = scrapy.Field() #源区微博作者
    source_content = scrapy.Field() #源区微博内容
    source_attitudes_count = scrapy.Field()  # 源区微博赞数
    source_comments_count = scrapy.Field()  # 源区微博评论数
    source_reposts_count = scrapy.Field()  # 源区微博转发数
    source_weibo_url = scrapy.Field()  # 源区微博微博的url
    source_video_views = scrapy.Field()  # 源区微博微博视频的观看次数
    source_video_url = scrapy.Field()  # 源区微博微博视频的url
    source_source = scrapy.Field()  # 源区微博微博的来源
    source_created_at = scrapy.Field()  # 源区微博发表的时间






