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
计算tfidf
"""

if __name__ == '__main__':
    stops = set(u"？。，！：；;,.&-/=你我他")
    stops = set(x.encode('utf8') for x in stops)
    for line in open('chinese_stop.txt'):
        stops.update(line.split())
    df = Counter()

    for line in open('df.sorted'):
        line = line.rstrip().split('\t')
        f = int(line[1])
        if f < 2 : continue
        df[line[0]] = f
    d = df['#']

    for ln, line in enumerate(sys.stdin) :
        print(ln, file = sys.stderr, end = '\r')
        #if ln > 1000: break
        news = json.loads(line)
        c = re.sub(r'(<|&lt;)[^>]*(>|&gt;)', '', news['content'])
        
        cc = []
        for i, ch in enumerate(c):
            o = ord(ch)
            if o >= 0xff01 and o <= 0xff5e :
                ch = unichr(o - 65248);
            cc.append(ch)
        c = ''.join(cc)

        rst = jieba.cut(c)

        rst = [x.strip().encode('utf8') for x in rst if x.strip()]

        rst = [x for x in rst if x not in stops and len(x) > 1]
        title = news['title'].encode('utf8')
        words = Counter(rst)

        if len(words) < 100 : continue

        s = sum(words.values())
        tfidf = [
                (math.log(1.0*d/df.get(k, 1)) * 1.0* v / s, 
                    1.0* v / s,
                    math.log(1.0*d/df.get(k, 1)),
                    k,) 
                for k, v in words.most_common()]
        tfidf = sorted(tfidf, reverse=True)
        print(title, ' '.join([x[-1] for x in tfidf[:min(len(tfidf), 5)]]), sep = '\t')


