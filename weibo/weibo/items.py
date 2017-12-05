# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content_id = scrapy.Field()  # 微博内容id
    content = scrapy.Field() #微博内容
    forward_user = scrapy.Field() #转发内容的源作者
    forward_content = scrapy.Field() #转发的内容
    attitudes_count = scrapy.Field() #赞数
    comments_count = scrapy.Field() #评论数
    reposts_count = scrapy.Field() #转发数
    single_weibourl = scrapy.Field() #微博的url
    publish_time = scrapy.Field() #发表的时间
    crawl_time = scrapy.Field() #爬取的时间

    # comment_name = scrapy.Field() #评论昵称
    # comment_content = scrapy.Field() #评论的内容
    # comment_userid = scrapy.Field() #评论者的id
    # source = scrapy.Field() #评论者的微博来源





