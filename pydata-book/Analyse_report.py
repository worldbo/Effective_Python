# 本程序依据总队考试监管通报总队考试监管通报内容进行数据完善

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


# 专列实验

# 获取最大行，最大列
nrows = data.shape[0]
# nrows = data.index.size
ncols = data.shape[1]
#ncols = data.columns.size

# data2 = data[0:5] #选取部分行
# print(data2)

# data3 = data[['kskm','xm','ksrs']] #选取部分列！！！
# print(data3)

# data4 = data[nrows-10:nrows-5][['kskm','xm','ksrs']] #选取指定行（后数10行到后数5行），列
# print(data4)

#方法一：利用.pivot（）函数进行转置，似乎最多只能支持21列0到20？?
# df.pivot(index=None, columns=None, values=None)
# data5 = data4.pivot(index='xm',columns='kskm',values='ksrs',aggfunc={'ksrs':'max'}) ##以两列多值进行完成行转列！！！！
# data5['Total'] = data4.apply(lambda x:np.sum(x),axis=1) ###聚合
# print(data5)

# data5 = data3.drop_duplicates().pivot(index='xm',columns='kskm',values='ksrs') ##先去重，以两列多值进行完成行转列！！！！
# print(data5)
##方法二：利用pandas层次化索引，进行转置，要把UserName和Subject列设置为层次化索引，.stack()和.unstack()
# Score为其对应的值即可，我们借用set_index()函数：
# data6 = data3.set_index(['kskm','xm'])
# print(data6.drop_duplicates().stack())
# print(data6.drop_duplicates().unstack())


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


# "order by decode(t.kskm,'科目一',1,'科目二',2,'的生成科目三',3)"  #order by decode()按照指定的顺序排序
data_dq = pd.read_sql(sql_query, engine1)  # Step1 : read csv
data_qs = pd.read_sql(sql_query1, engine1)  # Step1 : read csv
data_sydq = pd.read_sql(sql_query2, engine1)  # Step1 : read csv

#三种方法取值(后两种可规避重复值)
# km1 = data.loc[0, 'hgl'] * 100
# km2 = data.loc[1, 'hgl'] * 100
# km3 = data.loc[2, 'hgl'] * 100

# km1 = data[(data['kskm'] == '科目一')]['hgl'].iloc[0] * 100
# km2 = data[(data['kskm'] == '科目二')]['hgl'].iloc[0] * 100
# km3 = data[(data['kskm'] == '科目三')]['hgl'].iloc[0] * 100

km1_dq = data_dq[(data_dq['kskm'] == '科目一')]['hgl'].max() * 100
km2_dq = data_dq[(data_dq['kskm'] == '科目二')]['hgl'].max() * 100
km3_dq = data_dq[(data_dq['kskm'] == '科目三')]['hgl'].max() * 100

km1_qs = data_qs[(data_qs['kskm'] == '科目一')]['hgl'].max() * 100
km2_qs = data_qs[(data_qs['kskm'] == '科目二')]['hgl'].max() * 100
km3_qs = data_qs[(data_qs['kskm'] == '科目三')]['hgl'].max() * 100

km1_sydq = data_sydq[(data_sydq['kskm'] == '科目一')]['hgl'].max() * 100
km2_sydq = data_sydq[(data_sydq['kskm'] == '科目二')]['hgl'].max() * 100
km3_sydq = data_sydq[(data_sydq['kskm'] == '科目三')]['hgl'].max() * 100

# 两种体现百分数的方法
# print("吉林地区各科目整体平均合格率:%s,%s,%s" % (str(round(Decimal(km1),2)) + '%', str(round(Decimal(km2),2)) + '%', str(round(Decimal(km3),2)) + '%'))
print("吉林地区各科目整体平均合格率:%s,%s,%s" % (str('{:.2f}'.format(km1_dq)) + '%', str('{:.2f}'.format(km2_dq)) + '%', str('{:.2f}'.format(km3_dq)) + '%'))
print("全省平均值各科目整体平均合格率:%s,%s,%s" % (str('{:.2f}'.format(km1_qs)) + '%', str('{:.2f}'.format(km2_qs)) + '%', str('{:.2f}'.format(km3_qs)) + '%'))
print("本月地区与省平均值各科目整体平均合格率差:%s,%s,%s" % (str('{:.2f}'.format(km1_dq-km1_qs)) + '%', str('{:.2f}'.format(km2_dq-km2_qs)) + '%', str('{:.2f}'.format(km3_dq-km3_qs)) + '%'))
print("本月与上月地区各科目整体平均合格率环比:%s,%s,%s" % (str('{:.2f}'.format(km1_dq-km1_sydq)) + '%', str('{:.2f}'.format(km2_dq-km2_sydq)) + '%', str('{:.2f}'.format(km3_dq-km3_sydq)) + '%'))

###2.列出高于全省平均值考场的名称及高于值

