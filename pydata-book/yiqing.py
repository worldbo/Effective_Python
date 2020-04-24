#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 21:53:38 2020

@author: dingxuanlin

1.下载腾讯新闻的疫情实时报告的数据,保存成json文件至本地；
2.完成按照省为单位进行疫情分布图
"""

import json
import time
import requests

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
data = json.loads(requests.get(url).json()['data'])
print(data)
# 保存当天的json文件至本地
t = time.strftime("%Y-%m-%d", time.localtime())

file = open(t + '.json', 'w', encoding='utf-8')
json.dump(data, file, ensure_ascii=False)
file.close()
print("保存当日json文件已完成。")