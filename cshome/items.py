# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Question(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    source_name = scrapy.Field()
    source_url = scrapy.Field()
    entry_url = scrapy.Field()
    tags = scrapy.Field()
    answers = scrapy.Field()


class Answer(scrapy.Item):
    id = scrapy.Field()
    body = scrapy.Field()
