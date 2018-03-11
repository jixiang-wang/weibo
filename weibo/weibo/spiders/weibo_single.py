import scrapy
from ..items import WeiboItem
import requests
import json
import re
import time


class weiboSpider(scrapy.Spider):
    name = "weibo_single"
    allowed_domains = ['m.weibo.cn']
    single_containerid = 1076032714280233
    init_url = 'https://m.weibo.cn/api/container/getIndex?containerid={}&page={}'
    page = 0
    wb_count = 0
    html = requests.get(init_url.format(single_containerid, 1)).text
    datas = json.loads(html)
    weibo_count = int(datas['data']['cardlistInfo']['total'])
    start_urls = [init_url.format(single_containerid, 1)]

    def parse(self, response):
        if self.wb_count < self.weibo_count:
            self.page += 1
            wb_url = self.init_url.format(self.single_containerid, self.page)
            yield scrapy.Request(url=wb_url, dont_filter=True,callback=self.get_content)


    def get_content(self, response):
        infos = json.loads(response.body)
        item = WeiboItem()
        for info in infos.get('data').get('cards'):
            if info.get('card_type') == 9:
                #微博信息
                weibo_id = info.get('mblog').get('id')
                created_at = info.get('mblog').get('created_at')
                str_text = info['mblog']['text']
                dc = re.compile(r'<[^>]+>', re.S)
                text = dc.sub('', str_text)
                attitudes_count = info['mblog']['attitudes_count']
                comments_count = info['mblog']['comments_count']
                reposts_count = info['mblog']['reposts_count']
                weibo_url = info['scheme']
                source = info['mblog']['source']
                try:
                    video_views = (int(info['mblog']['obj_ext'][:-4]))*10000 if info['mblog']['obj_ext'][-4] in '万' else int(info['mblog']['obj_ext'][:-3])
                    try:
                        video_url = info['mblog']['page_info']['media_info']['stream_url']
                    except:
                        video_url = ''
                except:
                    video_views = 0
                    video_url = ''
                #转发微博的源区信息
                try:
                    source_id = info['mblog']['retweeted_status']['id']
                    source_created_at = info.get('mblog').get('retweeted_status').get('created_at')
                    str_text = info['mblog']['retweeted_status']['text']
                    dc = re.compile(r'<[^>]+>', re.S)
                    source_text = dc.sub('', str_text)
                    source_attitudes_count = info['mblog']['retweeted_status']['attitudes_count']
                    source_comments_count = info['mblog']['retweeted_status']['comments_count']
                    source_reposts_count = info['mblog']['retweeted_status']['reposts_count']
                    source_weibo_url = 'https://m.weibo.cn/status/' + source_id
                    source_source = info['mblog']['retweeted_status']['source']
                    source_user = info['mblog']['retweeted_status']['user']['screen_name']
                    try:
                        source_video_views = video_views = (int(info['mblog']['retweeted_status']['obj_ext'][:-4]))*10000 if info['mblog']['obj_ext'][-4] in '万' else int(info['mblog']['retweeted_status']['obj_ext'][:-3])
                        source_video_url = info['mblog']['retweeted_status']['page_info']['media_info']['stream_url']
                    except:
                        source_video_url = ''
                        source_video_views = 0
                except:
                    source_id = ''
                    source_created_at = ''
                    source_text = ''
                    source_attitudes_count = 0
                    source_comments_count = 0
                    source_reposts_count = 0
                    source_weibo_url = ''
                    source_source = ''
                    source_user = ''
                    source_video_url = ''
                    source_video_views = 0

                item['weibo_id'] = weibo_id
                item['content'] = text
                item['attitudes_count'] = attitudes_count
                item['comments_count'] = comments_count
                item['reposts_count'] = reposts_count
                item['weibo_url'] = weibo_url
                item['video_views'] = video_views
                item['video_url'] = video_url
                item['source'] = source
                item['created_at'] = created_at
                item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S')

                item['source_user'] = source_user
                item['source_id'] = source_id
                item['source_content'] = source_text
                item['source_attitudes_count'] = source_attitudes_count
                item['source_comments_count'] = source_comments_count
                item['source_reposts_count'] = source_reposts_count
                item['source_weibo_url'] = source_weibo_url
                item['source_video_views'] = source_video_views
                item['source_video_url'] = source_video_url
                item['source_source'] = source_source
                item['source_created_at'] = source_created_at

                self.wb_count += 1
                yield item
            yield scrapy.Request(url=response.url, callback=self.parse)

