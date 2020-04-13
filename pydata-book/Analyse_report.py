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

###查询相关表格并按照报告顺序内容给出相应数据！！！

sql_query = "select * from LS_JSRKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
            "like '2020-01-__' and t.xm like '吉林地区平均值' " \
            "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce
# "order by decode(t.kskm,'科目一',1,'科目二',2,'的生成科目三',3)"  #order by decode()按照指定的顺序排序
data = pd.read_sql(sql_query, engine1)  # Step1 : read csv
print(data)
#三种方法取值(后两种可规避重复值)
# km1 = data.loc[0, 'hgl'] * 100
# km2 = data.loc[1, 'hgl'] * 100
# km3 = data.loc[2, 'hgl'] * 100

# km1 = data[(data['kskm'] == '科目一')]['hgl'].iloc[0] * 100
# km2 = data[(data['kskm'] == '科目二')]['hgl'].iloc[0] * 100
# km3 = data[(data['kskm'] == '科目三')]['hgl'].iloc[0] * 100

km1 = data[(data['kskm'] == '科目一')]['hgl'].max() * 100
km2 = data[(data['kskm'] == '科目二')]['hgl'].max() * 100
km3 = data[(data['kskm'] == '科目三')]['hgl'].max() * 100

# 两种体现百分数的方法
# print("吉林地区各科目整体平均合格率:%s,%s,%s" % (str(round(Decimal(km1),2)) + '%', str(round(Decimal(km2),2)) + '%', str(round(Decimal(km3),2)) + '%'))
print("吉林地区各科目整体平均合格率:%s,%s,%s" % (str('{:.2f}'.format(km1)) + '%', str('{:.2f}'.format(km2)) + '%', str('{:.2f}'.format(km3)) + '%'))
