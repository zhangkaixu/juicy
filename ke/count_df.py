#!/usr/bin/env python2
#coding:utf8
from __future__ import print_function
from collections import Counter
import math
import re
import sys
import json
import jieba

"""
分词并且统计df
"""

if __name__ == '__main__':
    df = Counter()

    for ln, line in enumerate(sys.stdin) :
        print(ln, file = sys.stderr, end = '\r')
        news = json.loads(line)
        c = re.sub(r'<[^>]*>', '', news['content'])
        rst = jieba.cut(c)

        rst = [x.strip().encode('utf8') for x in rst if x.strip()]
        title = news['title'].encode('utf8')
        rst = Counter(rst)
        rst.update({'#':1})
        print(title, end = '\r', file = sys.stderr)
        df.update(rst.keys())

    for k, v in df.most_common():
        print(k,v, sep = '\t')
