# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from cshome.redis_cache import push_url


class To8toSeedsSpider(scrapy.Spider):
    name = 'to8to_seeds'
    allowed_domains = ['to8to.com']
    base_url = 'http://www.to8to.com/ask/'

    def start_requests(self):
        for num in range(8225498, 8592044):
            url = 'http://www.to8to.com/ask/k%s.html' % num
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/70.0.3538.102 Safari/537.36'
        }

        return Request(url, headers=headers)

    def parse(self, response):
        if response.status == 200:
            print(response.url)
            push_url('to8to:start_urls', response.url)

    def parse_backup(self, response):
        question_links = response.css('.question_hd h3 a::attr(href)').extract()

        self.logger.debug('Extract %d links' % len(question_links))

        for link in question_links:
            url = self.base_url + link

            push_url('to8to:start_urls', url)

        next_page_link = response.css('#nextpageid::attr(href)').extract_first()

        if next_page_link:
            next_page_url = self.base_url + next_page_link
            self.logger.debug('The next page url %s' % next_page_url)

            yield Request(next_page_url, callback=self.parse)
        else:
            self.logger.debug('No more pages')
