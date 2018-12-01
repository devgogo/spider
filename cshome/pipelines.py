# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from cshome.elastic import index_question, index_answer
from cshome.database import save_question
from cshome.tokenizer import cut
from cshome.utils import text_filter


class FilterPipeline(object):
    def process_item(self, item, spider):
        if not text_filter(item.get('title')):
            raise DropItem('Invalid Item')

        if item.get('body') and not text_filter(item.get('body')):
            raise DropItem('Invalid Item')

        if 'title' not in item:
            raise DropItem('Invalid Item')

        return item


class TokenizerPipeline(object):
    def process_item(self, item, spider):
        text = item.get('title') + (item.get('body') if item.get('body') else '')

        item['tags'] = cut(text)

        return item


class DatabasePipeline(object):

    def process_item(self, item, spider):
        try:
            save_question(item)

        except Exception as e:
            print('Mysql error: ', e)
            raise DropItem('Invalid Item')

        return item


class ElasticSearchPipeline(object):

    def process_item(self, item, spider):

        if not item['id']:
            raise DropItem('Invalid Item')

        doc = {
            'id': item.get('id'),
            'title': item.get('title'),
            'body': item.get('body'),
            'tags': item.get('tags'),
            'category': item.get('category'),
            'sub_category': item.get('sub_category'),
            'source_name': item.get('source_name'),
            'source_url': item.get('source_url'),
            'entry_url': item.get('entry_url')
        }

        index_question(doc)

        for answer in item.get('answers'):
            doc = {
                'question_id': item.get('id'),
                'id': answer.get('id'),
                'body': answer.get('body')
            }

            index_answer(doc)
