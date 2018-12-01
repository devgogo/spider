# -*- coding: utf-8 -*-

import re


def replace_last(s, old, new):
    return (s[::-1].replace(old[::-1], new[::-1], 1))[::-1]


def text_filter(text):
    black_list = ['to8to', '土巴兔', '编辑本段', '图', '网站', '装饰', '公司', '电话', '齐家', 'qijia', '17house', '一起装修', '本帖最后', '回复',
                  'QQ', '微信', '免费咨询', '联系', 'http', 'www', '学习', '顶一个', '.com', '网', '社区', '微信', 'v信']

    flag = True
    for word in black_list:
        if text.find(word.lower()) != -1:
            flag = False
            break
    return flag


def text_strip(text):
    if text is None:
        return ''

    text = str.strip(text)
    text = re.sub(r'[\r\n\t\s]', '', text)
    return text


def text_clear(text):
    if text is None:
        return ''

    text = re.sub(r'此问题来源于.*\.html', '', text)
    text = re.sub(r'{:[0-9_a-zA-Z]+:}', '', text)
    text = replace_last(text, '<br>', '')

    return text
