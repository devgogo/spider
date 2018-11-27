# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.utils.markup import remove_tags
from scrapy_redis.spiders import RedisSpider

from cshome.items import Question, Answer
from cshome.utils import text_filter, text_strip, text_clear


class To8toSpider(RedisSpider):
    name = 'to8to'

    def make_requests_from_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/70.0.3538.102 Safari/537.36'
        }

        return Request(url, headers=headers)

    def parse(self, response):
        title = text_strip(response.css('h2.ask-question-title::text').extract_first())
        body = text_strip(response.css('div.common-answer-text::text').extract_first())
        category = text_strip(response.css('.breadcrumb-pre:nth-child(4) a::text').extract_first())
        sub_category = text_strip(response.css('.breadcrumb-pre:nth-child(5) a::text').extract_first())

        question_item = Question()
        question_item['title'] = title
        question_item['body'] = body
        question_item['category'] = category if category else 'N/A'
        question_item['sub_category'] = sub_category if sub_category else 'N/A'
        question_item['source_name'] = 'to8to.com'
        question_item['source_url'] = response.url
        question_item['entry_url'] = response.url

        answers = response.css('.common-answer-text h3').extract()
        answers = map(text_strip, answers)
        answers = map(text_clear, answers)
        answers = filter(text_filter, answers)

        answer_items = []
        for answer in answers:
            answer_body = remove_tags(answer, keep=['br'])

            answer_item = Answer()
            answer_item['body'] = answer_body

            answer_items.append(answer_item)

        question_item['answers'] = answer_items

        yield question_item
