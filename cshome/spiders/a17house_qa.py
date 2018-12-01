# -*- coding: utf-8 -*-
import scrapy
from w3lib.html import remove_tags

from cshome.items import Question, Answer
from cshome.utils import text_strip, text_clear, text_filter


class A17HouseQASpider(scrapy.Spider):
    """17house 抓取"""
    name = '17house'
    allowed_domains = ['17house.com']

    def start_requests(self):

        for num in range(1, 4517758):
            url = 'http://ask.17house.com/q-%s.html' % num

            yield self.make_requests_from_url(url)

    def parse(self, response):
        if response.url.find('redirect') > 0:
            print('Invalid url')

            return

        title = text_clear(text_strip(response.css('h1::text').extract_first()))
        body = text_clear(text_strip(response.css('.index_center .content::text').extract_first()))
        category = text_strip(response.css('.breadCrumbList li:nth-child(2) a b::text').extract_first())
        sub_category = text_strip(response.css('.breadCrumbList li:nth-child(3) a b::text').extract_first())

        if category:
            category = category.replace('问答', '')

        if sub_category:
            sub_category = sub_category.replace('问答', '')

        question_item = Question()
        question_item['title'] = title
        question_item['body'] = body
        question_item['category'] = category if category else 'N/A'
        question_item['sub_category'] = sub_category if sub_category else 'N/A'
        question_item['source_name'] = '17house.com'
        question_item['source_url'] = response.url
        question_item['entry_url'] = response.url

        answers = response.css('.list .top').extract()
        answers = map(text_strip, answers)
        answers = map(text_clear, answers)
        answers = filter(text_filter, answers)

        answer_items = []
        for answer in answers:
            answer_body = remove_tags(answer, keep=['br'])

            if not answer_body:
                continue

            answer_item = Answer()
            answer_item['body'] = answer_body

            answer_items.append(answer_item)

        if len(answer_items) == 0:
            print("No Answer")
            return

        question_item['answers'] = answer_items

        print(question_item)
