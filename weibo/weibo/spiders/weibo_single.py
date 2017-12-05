
import scrapy
from ..items import WeiboItem
import requests
import json
import re
import time
import math


class weiboSpider(scrapy.Spider):
    name = "weibo_single"
    allowed_domains = ['m.weibo.cn']
    first_id = 3306361973
    init_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'
    def start_requests(self):
        url = self.init_url.format(self.first_id)
        yield scrapy.Request(url=url, callback=self.get_containerid)


    def get_containerid(self,response):
        infos = json.loads(response.body)
        weibo_count = int(infos['userInfo']['statuses_count'])
        pages = math.ceil((weibo_count - 1)/10)
        print(pages)
        for info in infos.get('tabsInfo').get('tabs'):
            if info.get('tab_type') == 'weibo':
                containerid = info.get('containerid')
                weibo_urls = [response.url + '&containerid=%s' % containerid + '&page={}'.format(str(i)) for i in range(1, int(pages)+1)]
                for weibo_url in weibo_urls:
                    yield scrapy.Request(url=weibo_url, callback=self.get_content)

    def get_content(self, response):
        infos = json.loads(response.body)
        item = WeiboItem()
        for info in infos.get('cards'):
            if info.get('card_type') == 9:
                single_weiboid = info.get('mblog').get('id')
                publish_time = info.get('mblog').get('created_at')
                # 微博内容
                str_content = info['mblog']['text']
                dc = re.compile(r'<[^>]+>', re.S)
                content = dc.sub('', str_content)
                # item['content'] = dc.sub('', str_content)
                #转发内容的源作者
                try:
                    forward_user = info['mblog']['retweeted_status']['user']['screen_name']
                except:
                    forward_user = "无"
                # 转发的内容
                try:
                    str_forward = info['mblog']['retweeted_status']['text']
                    df = re.compile(r'<[^>]+>', re.S)
                    forward_content = df.sub('', str_forward)
                    # item['forward_content'] = df.sub('', str_forward)
                except:
                    forward_content = "无"
                    # item['forward_content'] = "无"
                # 赞数
                attitudes_count = info['mblog']['attitudes_count']
                # item['attitudes_count'] = content['mblog']['attitudes_count']
                # 评论数
                comments_count = info['mblog']['comments_count']
                # item['comments_count'] = content['mblog']['comments_count']
                # 转发数
                reposts_count = info['mblog']['reposts_count']
                # item['reposts_count'] = content['mblog']['reposts_count']
                #单个微博的url
                single_weibourl = 'https://m.weibo.cn/status/%s' % (str(single_weiboid))

                item['content_id'] = single_weiboid
                item['content'] = content
                item['forward_user'] = forward_user
                item['forward_content'] = forward_content
                item['attitudes_count'] = attitudes_count
                item['comments_count'] = comments_count
                item['reposts_count'] = reposts_count
                item['single_weibourl'] = single_weibourl
                item['publish_time'] = publish_time
                item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S')

                yield item

    # def parse_comment(self, response):
    #     if response.status == 200:
    #         infos = requests.get(response).text
    #         data = json.loads(infos)
    #         comments = data['cards']
    #         item = WeiboItem()
    #         for comment in comments:
    #             # 评论昵称
    #             item['comment_name'] = comment['user']['screen_name']
    #             # 评论的内容
    #             item['comment_content'] = comment['text'].text()
    #             # 评论者的id
    #             item['comment_userid'] = comment['user']['id']
    #             # 评论者的微博来源
    #             item['source'] = comment['source']
    #             yield item
