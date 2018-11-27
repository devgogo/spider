# -*- coding: utf-8 -*-

import re


def replace_last(s, old, new):
    return (s[::-1].replace(old[::-1], new[::-1], 1))[::-1]


def text_filter(text):
    black_list = ['to8to', '土巴兔', '编辑本段', '图', '网站', '装饰', '公司', '电话', '齐家', 'qijia']

    flag = True
    for word in black_list:
        if text.find(word) != -1:
            flag = False
            break
    return flag


def text_strip(text):
    if text is None:
        return None

    text = str.strip(text)
    text = re.sub(r'[\r\n\t\s]', '', text)
    return text


def text_clear(text):
    text = re.sub(r'此问题来源于.*\.html', '', text)
    text = replace_last(text, '<br>', '')

    return text
