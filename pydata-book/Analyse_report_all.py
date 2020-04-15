# 本程序依据总队考试监管通报总队考试监管通报内容进行数据完善---最终版（无中间过程）

from decimal import Decimal
import xlrd
import xlwt
from re import sub
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.dialects.oracle import \
    BFILE, BLOB, CHAR, CLOB, DATE, \
    DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
    NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
    VARCHAR2
import time

username1 = 'world'
password1 = '1'
host_port1 = 'localhost:1521'
database1 = 'ORCL'

database1_Tables = ['JSRKSHGL', 'ksyhgl', 'jsrydkshgl', 'km2ccksnl', 'ksycqk', 'km2ycshzb', 'ksxmkf']  # total seven
database1_Tables = [item.upper() for item in
                    database1_Tables]  # 对列表内容转换大小写['JSRKSHGL', 'KSYHGL', 'JSRYDKSHGL', 'KM2CCKSNL', 'KSYCQK', 'KSXMKF', 'KM2YCSHZB']

Table_Name = 'LS_JSRKSHGL'

engine1 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username1, password1, host_port1, database1),
                        encoding='utf-8', echo=True)

data = pd.read_sql("select * from %s" % (Table_Name), engine1)
print(data.head())

data.info()
print(data.describe(include='all'))  # Step2 : preview data

data1 = data.copy(deep=True)  # Step3: check null value for every column
print(data1)
print(data1.isnull().sum())


# 获取最大行，最大列
nrows = data.shape[0]
ncols = data.shape[1]

###查询相关表格并按照报告顺序内容给出相应数据！！！
###1、列出地区与全省各科值，以及环比、同比情况：

sql_query = "select * from LS_JSRKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
            "like '2020-01-__' and t.xm like '吉林地区平均值' " \
            "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；本月地区
sql_query1 = "select * from LS_JSRKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
            "like '2020-01-__' and t.xm like '全省平均值' " \
            "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；本月省
sql_query2 = "select * from LS_JSRKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
            "like '2019-12-__' and t.xm like '吉林地区平均值' " \
            "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；上月地区


data_dq = pd.read_sql(sql_query, engine1)  # Step1 : read csv
data_qs = pd.read_sql(sql_query1, engine1)  # Step1 : read csv
data_sydq = pd.read_sql(sql_query2, engine1)  # Step1 : read csv


#三种方法取值(后两种可规避重复值),将字符串常量转化为变量!
kskm_list = ['科目一', '科目二', '科目三']
for i, kskm_q in enumerate(kskm_list):
    globals()['km' + str(i + 1) + '_dq'] = data_dq[(data_dq['kskm'] == kskm_q)]['hgl'].max() * 100
    globals()['km'+str(i+1)+'_qs'] = data_qs[(data_qs['kskm'] == kskm_q)]['hgl'].max() * 100
    globals()['km' + str(i + 1) + '_sydq']  = data_sydq[(data_sydq['kskm'] == kskm_q)]['hgl'].max() * 100


# 两种体现百分数的方法

print("吉林地区各科目整体平均合格率:%s,%s,%s" % (str('{:.2f}'.format(km1_dq)) + '%', str('{:.2f}'.format(km2_dq)) + '%', str('{:.2f}'.format(km3_dq)) + '%'))
print("全省平均值各科目整体平均合格率:%s,%s,%s" % (str('{:.2f}'.format(km1_qs)) + '%', str('{:.2f}'.format(km2_qs)) + '%', str('{:.2f}'.format(km3_qs)) + '%'))
print("本月地区与省平均值各科目整体平均合格率差:%s,%s,%s" % (str('{:.2f}'.format(km1_dq-km1_qs)) + '%', str('{:.2f}'.format(km2_dq-km2_qs)) + '%', str('{:.2f}'.format(km3_dq-km3_qs)) + '%'))
print("本月与上月地区各科目整体平均合格率环比:%s,%s,%s" % (str('{:.2f}'.format(km1_dq-km1_sydq)) + '%', str('{:.2f}'.format(km2_dq-km2_sydq)) + '%', str('{:.2f}'.format(km3_dq-km3_sydq)) + '%'))

###2.列出高于全省平均值考场的名称及高于值
#注意SQL语句中带引号的参数值一定加上\'{}\'转义符不带引号的表格名称等不要加！！！！！

def query_kcmc(year_month=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[0:7]+'-__',kskm_query='科目一',kmz=1):

    year_month = year_month+'-__'
    data_query_kcmc = pd.read_sql("select * from LS_JSRKSHGL t "
                                 "WHERE to_char(t.scyf,'yyyy-MM-dd') like \'{}\'  "
                                 "AND  t.xm not IN('吉林地区平均值','全省平均值') "
                                 "AND t.kskm LIKE \'{}\' "
                                 "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M'), t.hgl DESC".format(year_month,kskm_query),engine1)
    temp = data_query_kcmc[['xm', 'hgl']].drop_duplicates()
    temp['qs_cha'] = temp.apply(lambda x: (x.hgl * 100 - kmz), axis=1)  # 取出值
    temp['hgl'] = temp.apply(lambda x: (x.hgl * 100), axis=1)
    return (temp)

for i, kskm_q in enumerate(kskm_list):
    wd = query_kcmc('2020-01', kskm_q, globals()['km' + str(i + 1) + '_qs'])
    print(wd)

