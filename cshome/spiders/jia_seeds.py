# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from cshome.redis_cache import push_url


class JiaSeedsSpider(scrapy.Spider):
    name = 'jia_seeds'
    allowed_domains = ['jia.com']
    base_url = 'https://www.jia.com'
    start_urls = ['https://www.jia.com/wenda/lista-2/p2/?sort=1']

    # def start_requests(self):
    #     for url in jia_seeds:
    #         yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/70.0.3538.102 Safari/537.36'
        }

        return Request(url, headers=headers)

    def parse(self, response):
        question_links = response.css('.item-container a.item-div::attr(href)').extract()

        self.logger.debug('Extract %d links' % len(question_links))

        for link in question_links:
            url = self.base_url + link

            if url.find("a-"):
                print(url)

                push_url('jia:start_urls', url)
            else:
                self.logger.debug('invalid url %s' % url)

        next_page_link = response.css('.changedown::attr(href)').extract()[1]

        if next_page_link:
            next_page_url = self.base_url + next_page_link
            self.logger.debug('The next page url %s' % next_page_url)

            yield Request(next_page_url, callback=self.parse)
        else:
            self.logger.debug('No more pages')
