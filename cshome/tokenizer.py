# -*- coding: utf-8 -*-

import jieba.analyse


def cut(text):
    return jieba.analyse.extract_tags(text, topK=2, withWeight=False, allowPOS=('n', 'ns', 'nt'))
