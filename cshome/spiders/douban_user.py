# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import codecs

f = codecs.open('user.txt', 'w', encoding='utf-8')


class DoubanUserSpider(scrapy.Spider):
    """douban 抓取"""
    name = 'douban_user'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/group/EmirKusturica/discussion?start=0']

    def start_requests(self):

        for num in range(0, 21050, 25):
            url = 'https://www.douban.com/group/EmirKusturica/discussion?start=%s' % num

            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/70.0.3538.102 Safari/537.36'
        }

        return Request(url, headers=headers)

    def parse(self, response):
        users = response.css('.article td:nth-child(2) > a::text').extract()

        print(users)

        for user in users:
            f.write(user + '\n')

        next_page = response.css('.next a::attr(href)').extract_first()

        if next_page:
            yield Request(next_page)
