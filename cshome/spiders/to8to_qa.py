# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import json
from w3lib.html import remove_tags

from cshome.items import Question, Answer
from cshome.utils import text_strip, text_clear, text_filter


class To8toQASpider(scrapy.Spider):
    """to8to 抓取"""
    name = 'to8to_qa'
    allowed_domains = ['to8to.com']

    headers = {
        'User-Agent': 'HouseKeeper/5.0.2 (iPhone; iOS 10.3.2; TO8TOAPP)',
    }

    url = 'https://mobileapi.to8to.com/index.php'

    def start_requests(self):

        for num in range(1, 8500000):
            print('num is %s' % num)
            question_id = num
            form_data = {
                'action': 'QuestionDetail',
                'appid': '15',
                'appostype': '2',
                'appversion': '5.0.0',
                'ask_id': '%s' % question_id,
                'channel': 'appstore',
                'idfa': '00000000-0000-0000-0000-000000000000',
                'model': 'Qna',
                'page': '1',
                'paging': '1',
                'systemversion': '10.3.2',
                't8t_device_id': 'ECEC00D9-9F98-4B44-BA79-3C6FEE00F292',
                'to8to_token': '',
                'type': '0',
                'uid': '0',
                'version': '2.5'
            }

            yield FormRequest(url=self.url, formdata=form_data, headers=self.headers, meta={'question_id': question_id})

    def parse(self, response):
        r = json.loads(response.body_as_unicode())

        url = 'http://www.to8to.com/ask/k%s.html' % response.meta['question_id']

        if len(r['data']['ask']) == 0:
            print("No Data")
            return

        question_data = r['data']['ask'][0]

        question_item = Question()
        question_item['title'] = question_data['subject']
        question_item['body'] = question_data['direction']
        question_item['category'] = question_data['type_pid_name']
        question_item['sub_category'] = question_data['type_id_name']
        question_item['source_name'] = 'to8to.com'
        question_item['source_url'] = url
        question_item['entry_url'] = url

        answers = []
        for answer_data in r['data']['answer']:
            answers.append(answer_data['content'])

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
