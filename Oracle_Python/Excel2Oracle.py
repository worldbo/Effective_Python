# !/usr/bin/python -*-
# coding: utf-8 -*-
# File Name: Excel2Oracle.py
# ---月异常数据Excel2Oracle导入Oracle程序---
# Created on DATE:20200101
# version：1.0 ---
# author：bzy


import xlrd
import xlwt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from operator import itemgetter
import cx_Oracle
# from common import database
import requests
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
# 用于以清晰、可读的形式输出 Python 数据结构
from pprint import pprint
from sys import modules
import os
import re
import datetime
import time
import threading
import sqlalchemy



os.getcwd()  # 判断当前程序文件的路径

# 连接Oracle数据库，下面括号里内容根据自己实际情况填写
# conn = cx_Oracle.connect('用户名/密码@IP:端口号/SERVICE_NAME')
# conn = cx_Oracle.connect('scott', 'tiger', 'localhost:1521/ORCL')
conn = cx_Oracle.connect('scott/tiger@localhost:1521/ORCL')
# conn = create_engine('oracle+cx_oracle://scott:tiger@localhost:1521/ORCL",encoding='utf-8', echo=True)
dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'ORCL')
print(dsn_tns)
print(conn.version)  # 判断是否链接成功oracle

# 每月Excel表格数据清洗与导入Oracle：

# ===============定义表格参数==========================================================
EXcel_FilesPath = 'F:/2020年社会化考场违规情况汇总/一月份/通报数据/'
EXcel_Files = '吉林1月异常数据统计1.xlsx'
Sheet_Names = ' 考试系统时间异常 '  # '项目考试时间过短 ','车速为零','重点扣分项目无记录',
# ' 考试成绩计算不一致 ','项目完成时间超长 '#也可直接赋值或指定sheet_name = [0, '英超射手榜', 'Sheet4']，
Insert_Line = 0


# =====================================================================================

File_Data = pd.read_excel(EXcel_FilesPath + EXcel_Files, Sheet_Names)
#print(File_Data)
# print(File_Data.loc[1,'考试日期'])  #判断File_Data为DataFrame，取出第一行数据 df.loc[df.a>2]；loc先行后列，行列标签用逗号分割，是利用行列标签取值
# print(File_Data.iloc[1,3])  #取出第一行,第2列的数据； iloc是利用行数与列数(起始值为0)来索引的，也是先行后列，行列用逗号分割。，
#print(File_Data['考试日期'])   #利用列标签取出指定列数据； DataFrame
# print(File_Data[File_Data.columns[3]])   #利用列数(起始值为0)取出指定列数据； DataFrame

# 获取最大行，最大列
nrows = File_Data.shape[0]
# nrows = File_Data.index.size
ncols = File_Data.shape[1]
#ncols = File_Data.columns.size

#取指定行的内容：
# iRow = 1                  #指定行(起始值为0)
# for iCol in range(ncols):
#     print(File_Data.iloc[iRow,iCol])

#遍历所有读取的数据
# for iRow in range(nrows):
#     for iCol in range(ncols):
#         print(File_Data.iloc[iRow,iCol])

print("=========================================================================")
print('Max Rows:' + str(nrows))
print('Max Columns' + str(ncols))
print("=========================================================================")

File_Data['流水号'] = [' %i' % i for i in File_Data['流水号']]  # 解决科学技术法符号问题

File_Data1 = File_Data.sort_values(by=['考试日期', '预警描述'],
                                   ascending=[True, False])  # sort是以###为标准排序 ascending=True,升序排序
# data1.to_excel(string+'.xls',sheet_name='string', encoding='utf-8')
#data['level'] = np.where(data['money']>=10, 'high', 'low') 增加一个lever列，根据公式判断后添加到相应的行元素中
#data.loc[(data['level']=="high") & (data['origin']=="China"),"sign"]="棒"
File_Data1.to_excel(EXcel_FilesPath + 'ls_out.xls', Sheet_Names, index=False, encoding='utf-8')  # 写入一个临时表
print('生成临时文件：' + EXcel_FilesPath + 'ls_out.xls' + '成功！！！')
print("================================ Finish ============================")
# 使用cursor()方法获取操作游标
cursor = conn.cursor()

# =====================导入===============================================
def log(message, when=None):
    """Log a messge with a timestamo

    Args:
        message:Message to print
        when:datatime of when the message occurred
            Defaults to the present time."""

    when = datetime.datetime.now() if when is None else when
    print('%s:%s' % (when, message))

#sql = "INSERT INTO LS_KSXTSJYC t (t.yjlx,t.ksrq) VALUES ('Wilson',to_date('2007-12-20 18:31:34' , 'YYYY-MM-DD HH24:MI:SS'))"
spq_query = "INSERT INTO LS_KSXTSJYC t(t.yjlx,t.lsh,t.kskm,t.kcmc,t.kssb,t.kccp,t.yjms)" \
            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s')"
log('正在导入，请耐心等待！！！!')
time.sleep(0.1)
for i in range(0,nrows):  #从第一列开始读取每行
    try:
        #     解析sql语句
        cursor.execute(spq_query % (File_Data.iloc[i,0],File_Data.iloc[i,1],File_Data.iloc[i,2],File_Data.iloc[i,4],
                                   File_Data.iloc[i,5],File_Data.iloc[i,6],File_Data.iloc[i,7]))
        # 捕获SQL异常
        if i % 1000 == 0:
            conn.commit()
    except cx_Oracle.DatabaseError as e:
        print(e)

conn.commit()
time.sleep(0.1)
cursor.close()
conn.close()
log('导入完成!!')
