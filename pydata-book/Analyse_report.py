# 本程序依据总队考试监管通报总队考试监管通报内容进行数据完善
# 清洗数据：a.读入数据；b.数据预览；c.检查NULL值；d.补全空值；e.特征工程；f.编码；g.再check；
# 数据分析与挖掘：数据探索（质量分析、特征分析）、数据预处理（清洗、集成、变换、规约）、挖掘建模
# （分类预测、聚类分析、关联规则、时序分析、离群点检测）


from decimal import Decimal
from functools import reduce
from itertools import chain
import logging
import textwrap
from pprint import pprint
import math
import xlrd
import xlwt
import re
import nltk
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
from datetime import datetime
from matplotlib import pyplot as plt
import difflib


def get_equal_rate(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


username1 = 'world'
password1 = '1'
host_port1 = 'localhost:1521'
database1 = 'ORCL'
sql_query_data = '2020-01'
# 科目二扣分代码：
km2kfdm = [10000, 10100, 10101, 10102, 10103, 10104, 10105, 10106, 10107, 10108, 10109,
           10110, 10111, 10112, 10113, 10114, 10115, 10116, 10117, 10118, 10119, 10120,
           10121, 10122, 10123, 10124, 10125, 10126, 10200, 10201, 10202, 10203, 10204,
           10205, 10206, 10207, 10208, 10209, 10210, 10211, 20000, 20100, 20101, 20102,
           20103, 20104, 20105, 20106, 20200, 20201, 20202, 20203, 20204, 20205, 20206,
           20300, 20301, 20302, 20303, 20304, 20305, 20306, 20400, 20401, 20402, 20403,
           20404, 20405, 20406, 20500, 20501, 20502, 20503, 20600, 20601, 20602, 20603,
           20700, 20701, 20702, 20703, 20800, 20801, 20802, 20803, 20900, 20901, 20902,
           20903, 20904, 20905, 21000, 21001, 21002, 21003, 21100, 21101, 21102, 21103,
           21200, 21201, 21202, 21203, 21204, 21300, 21301, 21302, 21303, 21304, 21400,
           21401, 21402, 21403, 21404, 21500, 21501, 21502, 21600, 21601, 21602, 21603,
           21700, 21701, 21702, 21800, 21801, 21802, 21803, 21804, 21805]
# 科目二小型车扣分代码：
km2kfdm_xxc = [10101, 10102, 10103, 10104, 10105, 10106, 10107, 10108, 10109, 10110, 10111,
               10112, 10113, 10114, 10115, 10116, 10117, 10118, 10119, 10120, 10121, 10122,
               10125, 10126, 10200, 10201, 10202, 10203, 10204, 10205, 10206, 10207, 10208,
               10209, 10210, 10211, 20101, 20102, 20103, 20104, 20105, 20106, 20301, 20302,
               20303, 20304, 20305, 20306, 20401, 20402, 20403, 20404, 20405, 20406, 20601,
               20602, 20603, 20701, 20702, 20703]
# 科目二大型车扣分代码
km2kfdm_dxc = [10100, 10101, 10102, 10103, 10104, 10105, 10106, 10107, 10108, 10109, 10110,
               10111, 10112, 10113, 10114, 10115, 10116, 10117, 10118, 10119, 10120, 10121,
               10122, 10126, 10200, 10201, 10202, 10203, 10204, 10205, 10206, 10207, 10208,
               10209, 10210, 10211, 20201, 20202, 20203, 20204, 20205, 20206, 20300, 20301,
               20302, 20303, 20304, 20305, 20306, 20400, 20401, 20402, 20403, 20404, 20405,
               20406, 20500, 20501, 20502, 20503, 20600, 20601, 20602, 20603, 20700, 20701,
               20702, 20703, 20800, 20801, 20802, 20803, 20900, 20901, 20902, 20903, 20904,
               20905, 21000, 21001, 21002, 21003, 21100, 21101, 21102, 21103, 21200, 21201,
               21202, 21203, 21204, 21300, 21301, 21302, 21303, 21304, 21400, 21401, 21402,
               21403, 21404, 21500, 21501, 21502, 21600, 21601, 21602, 21603, 21700, 21701,
               21702, 21800, 21801, 21802, 21803, 21804, 21805]

# 科目三扣分代码：

km3kfdm = [30000, 30100, 30101, 30102, 30103, 30104, 30105, 30106, 30107, 30108, 30109,
           30110, 30111, 30112, 30113, 30114, 30115, 30116, 30117, 30118, 30119, 30120,
           30121, 30122, 30123, 30124, 30125, 30126, 30127, 30128, 30129, 30130, 30131,
           30132, 30133, 30134, 30135, 30136, 30200, 30201, 30202, 30203, 30204, 30205,
           30206, 30207, 30208, 30209, 30210, 30211, 40000, 40100, 40101, 40102, 40200,
           40201, 40202, 40203, 40204, 40205, 40206, 40207, 40208, 40209, 40210, 40211,
           40300, 40301, 40302, 40303, 40304, 40400, 40401, 40402, 40500, 40501, 40502,
           40503, 40600, 40601, 40602, 40603, 40604, 40605, 40606, 40607, 40608, 40609,
           40610, 40700, 40701, 40702, 40703, 40704, 40800, 40801, 40802, 40803, 40804,
           40805, 40900, 40901, 40902, 40903, 40904, 41000, 41001, 41002, 41003, 41100,
           41101, 41102, 41103, 41200, 41201, 41202, 41203, 41300, 41301, 41302, 41303,
           41400, 41401, 41402, 41403, 41404, 41405, 41406, 41407, 41500, 41501, 41502,
           41503, 41504, 41600, 41601, 41602, 41603, 41604, 41605, 41606, 41607, 41608,
           41609, 41700, 41701, 41702, 41703, 41704, 41705, 41706, 41707, 41708, 41709]

# 科目二系统提供商与考场名称:
km2ksxt_kcmc = {'吉林市九新科目二分考场': '安徽三联交通应用技术股份有限公司', '吉林市吉利科目二分考场': '安徽三联交通应用技术股份有限公司'}

#科目二大型车考试场名称：
km2dxc_kcmc = ['吉林市九新科目二分考场','吉林市交管支队科目二考场','吉林舒兰蓝盾科目二分考场']

# 科目三系统提供航与考场名称:
km3ksxt_kcmc = {'吉林市九新江城科目三分考场': '安徽三联交通应用技术股份有限公司', '吉林市吉凇鸿利科目三分考场': '安徽三联交通应用技术股份有限公司',
                '吉林市交警支队科目三分考场': '安徽三联交通应用技术股份有限公司', '吉林市舒兰蓝盾科目三分考场': '安徽三联交通应用技术股份有限公司'}

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
# ncols = data.columns.size

# data2 = data[0:5] #选取部分行
# print(data2)

# data3 = data[['kskm','xm','ksrs']] #选取部分列！！！
# print(data3)

# data4 = data[nrows-10:nrows-5][['kskm','xm','ksrs']] #选取指定行（后数10行到后数5行），列
# print(data4)

# 方法一：利用.pivot（）函数进行转置，似乎最多只能支持21列0到20？?
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


###第一部分、查询相关表格并按照报告顺序内容给出相应数据！！！
###1、列出地区与全省各科值，以及环比、同比情况：

sql_query = "select * from LS_JSRKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
            "like '2020-01-__' and t.xm like '吉林地区平均值' " \
            "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；本月地区
sql_query1 = "select * from LS_JSRKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
             "like '2020-01-__' and t.xm like '全省平均值' " \
             "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；本月省
sql_query2 = "select * from LS_JSRKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
             "like '2020-01-__' and t.xm like '吉林地区平均值' " \
             "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；上月地区

# "order by decode(t.kskm,'科目一',1,'科目二',2,'的生成科目三',3)"  #order by decode()按照指定的顺序排序
data_dq = pd.read_sql(sql_query, engine1)  # Step1 : read csv
data_qs = pd.read_sql(sql_query1, engine1)  # Step1 : read csv
data_sydq = pd.read_sql(sql_query2, engine1)  # Step1 : read csv

# 三种方法取值(后两种可规避重复值),将字符串常量转化为变量!
kskm_list = ['科目一', '科目二', '科目三']
for i, kskm_q in enumerate(kskm_list):
    globals()['km' + str(i + 1) + '_dq'] = data_dq[(data_dq['kskm'] == kskm_q)]['hgl'].max() * 100
    globals()['km' + str(i + 1) + '_qs'] = data_qs[(data_qs['kskm'] == kskm_q)]['hgl'].max() * 100
    globals()['km' + str(i + 1) + '_sydq'] = data_sydq[(data_sydq['kskm'] == kskm_q)]['hgl'].max() * 100

# 以上字符串常量动态的转化成变量替代如下程序：
# km1 = data.loc[0, 'hgl'] * 100
# km2 = data.loc[1, 'hgl'] * 100
# km3 = data.loc[2, 'hgl'] * 100

# km1 = data[(data['kskm'] == '科目一')]['hgl'].iloc[0] * 100
# km2 = data[(data['kskm'] == '科目二')]['hgl'].iloc[0] * 100
# km3 = data[(data['kskm'] == '科目三')]['hgl'].iloc[0] * 100

# km1_dq = data_dq[(data_dq['kskm'] == '科目一')]['hgl'].max() * 100
# km2_dq = data_dq[(data_dq['kskm'] == '科目二')]['hgl'].max() * 100
# km3_dq = data_dq[(data_dq['kskm'] == '科目三')]['hgl'].max() * 100

# km1_qs = data_qs[(data_qs['kskm'] == '科目一')]['hgl'].max() * 100
# km2_qs = data_qs[(data_qs['kskm'] == '科目二')]['hgl'].max() * 100
# km3_qs = data_qs[(data_qs['kskm'] == '科目三')]['hgl'].max() * 100

# km1_sydq = data_sydq[(data_sydq['kskm'] == '科目一')]['hgl'].max() * 100
# km2_sydq = data_sydq[(data_sydq['kskm'] == '科目二')]['hgl'].max() * 100
# km3_sydq = data_sydq[(data_sydq['kskm'] == '科目三')]['hgl'].max() * 100

# 两种体现百分数的方法
# print("吉林地区各科目整体平均合格率:%s,%s,%s" % (str(round(Decimal(km1),2)) + '%', str(round(Decimal(km2),2)) + '%', str(round(Decimal(km3),2)) + '%'))
print("吉林地区各科目整体平均合格率:%s,%s,%s" % (
    str('{:.2f}'.format(km1_dq)) + '%', str('{:.2f}'.format(km2_dq)) + '%', str('{:.2f}'.format(km3_dq)) + '%'))
print("全省平均值各科目整体平均合格率:%s,%s,%s" % (
    str('{:.2f}'.format(km1_qs)) + '%', str('{:.2f}'.format(km2_qs)) + '%', str('{:.2f}'.format(km3_qs)) + '%'))
print("本月地区与省平均值各科目整体平均合格率差:%s,%s,%s" % (
    str('{:.2f}'.format(km1_dq - km1_qs)) + '%', str('{:.2f}'.format(km2_dq - km2_qs)) + '%',
    str('{:.2f}'.format(km3_dq - km3_qs)) + '%'))
print("本月与上月地区各科目整体平均合格率环比:%s,%s,%s" % (
    str('{:.2f}'.format(km1_dq - km1_sydq)) + '%', str('{:.2f}'.format(km2_dq - km2_sydq)) + '%',
    str('{:.2f}'.format(km3_dq - km3_sydq)) + '%'))


###2.列出高于全省平均值考场的名称及高于值
# 注意SQL语句中带引号的参数值一定加上\'{}\'转义符不带引号的表格名称等不要加！！！！！

def query_kcmc(year_month=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[0:7] + '-__', kskm_query='科目一', kmz=1):
    year_month = year_month + '-__'
    data_query_kcmc = pd.read_sql("select * from LS_JSRKSHGL t "
                                  "WHERE to_char(t.scyf,'yyyy-MM-dd') like \'{}\'  "
                                  "AND  t.xm not IN('吉林地区平均值','全省平均值') "
                                  "AND t.kskm LIKE \'{}\' "
                                  "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M'), t.hgl DESC".format(
        year_month, kskm_query), engine1)
    temp = data_query_kcmc[['xm', 'hgl']].drop_duplicates()
    temp['qs_cha'] = temp.apply(lambda x: (x.hgl * 100 - kmz), axis=1)  # 取出值
    temp['hgl'] = temp.apply(lambda x: (x.hgl * 100), axis=1)
    return (temp)


# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 100)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)  # 设置打印宽度(**重要**)
pd.set_option('expand_frame_repr', False)  # 数据超过总宽度后，是否折叠显示

# wd = query_kcmc('2020-01','科目一',km1_qs)
# print(wd)
# wd = query_kcmc('2020-01','科目二',km2_qs)
# print(wd)
# wd = query_kcmc('2020-01','科目三',km3_qs)
# print(wd)


for i, kskm_q in enumerate(kskm_list):
    wd = query_kcmc('2020-01', kskm_q, globals()['km' + str(i + 1) + '_qs'])
    print(wd)

# 3、异地考试合格率情况分析：

sql_query_yd = "select * from LS_JSRYDKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
               "like '2020-01-__' and t.xm like '吉林地区平均值' " \
               "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；本月地区异地
sql_query1_yd = "select * from LS_JSRYDKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
                "like '2020-01-__' and t.xm like '全省平均值' " \
                "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；本月省异地
sql_query2_yd = "select * from LS_JSRYDKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
                "like '2019-12-__' and t.xm like '吉林地区平均值' " \
                "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；上月地区异地
sql_query3_yd = "select * from LS_JSRYDKSHGL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
                "like '2019-12-__' and t.xm like '全省平均值' " \
                "ORDER BY NLSSORT(t.kskm,'NLS_SORT = SCHINESE_STROKE_M')"  # 按照指定列汉字笔画排序 desc/asce；上月全省异地

data_dq_yd = pd.read_sql(sql_query_yd, engine1)  # Step1 : read csv
data_qs_yd = pd.read_sql(sql_query1_yd, engine1)  # Step1 : read csv
data_sydq_yd = pd.read_sql(sql_query2_yd, engine1)  # Step1 : read csv
data_syqs_yd = pd.read_sql(sql_query3_yd, engine1)  # Step1 : read csv

ydkm3_dq = data_dq_yd[(data_dq_yd['kskm'] == '科目三')]['hgl'].max() * 100
ydkm3_qs = data_qs_yd[(data_qs_yd['kskm'] == '科目三')]['hgl'].max() * 100
ydkm3_sydq = data_sydq_yd[(data_sydq_yd['kskm'] == '科目三')]['hgl'].max() * 100
ydkm3_syqs = data_syqs_yd[(data_syqs_yd['kskm'] == '科目三')]['hgl'].max() * 100

##直接在dataframe相应列中一次性改成百分数：dataframe名称.style.format({'相应列': '{0:.2%}'.format})

print("吉林地区异地科目三整体平均合格率:%s" % (str('{:.2f}'.format(ydkm3_dq)) + '%'))
print("全省异地科目三整体平均合格率:%s" % (str('{:.2f}'.format(ydkm3_qs)) + '%'))
print("本月地区异地科目三与省平均值整体平均合格率差:%s" % (str('{:.2f}'.format(ydkm3_dq - ydkm3_qs)) + '%'))
print("本月与上月地区异地科目三整体平均合格率环比:%s" % (str('{:.2f}'.format(ydkm3_dq - ydkm3_sydq)) + '%'))
print("本月与上月全省异地科目三整体平均合格率环比:%s" % (str('{:.2f}'.format(ydkm3_qs - ydkm3_syqs)) + '%'))

###第二部分、预警情况：
# 4、科目二场地驾驶技能考试超出考试能力预警情况分析：

sql_query_nl = "select * from LS_KM2CCKSNL t WHERE to_char(t.scyf,'yyyy-MM-dd') " \
               "like '2019-12-__'ORDER BY to_char(t.ksrq,'yyyy-MM-dd') ASC"  # 本月科目二场地驾驶技能考试超出考试能力
data_dq_nl = pd.read_sql(sql_query_nl, engine1)  # Step1 : read csv

# 产生预警信息考场信息：
print('\n')
data_dq_nlkc = data_dq_nl[['kcmc', 'ksrq', 'yjzb']]
print('产生超出考试能力预警信息考场共：%s个，它们分别为：' % (data_dq_nlkc[['kcmc']].drop_duplicates().shape[0]))
# 表格模式输出
# print(data_dq_nlkc[['kcmc']].drop_duplicates(),'\n')
# 数据框转化成列表模式输出：
# 第一种方法：利用数组：
# print(np.array(data_dq_nlkc[['kcmc']].drop_duplicates()).tolist(),'\n')
# 第二种方法：利用values：
zfdata_dq_nlkc = (data_dq_nlkc[['kcmc']].drop_duplicates()).values.tolist()
for i, temp in enumerate(zfdata_dq_nlkc):
    print(zfdata_dq_nlkc[i][0], end=',')  # 打印列表不换行！！！end='，'分隔
print('\n')

print('产生超出考试能力预警信息考场所涉及场次日期如下表：')
# print(data_dq_nlkc.pivot(index='kcmc', columns='ksrq', values='yjzb'))
print(pd.pivot_table(data_dq_nlkc, index='kcmc', columns='ksrq',
                     values='yjzb').rename({'kcmc': '考场名称', 'ksrq': '考试日期'}, axis=1))

# 5、考试异常统计情况：
# 异常情况数量；涉及考场；发生日期表；异常信息：无%音视频%；没有车辆备案；监管中无三类等
sql_query_ycqk = "SELECT * from LS_KSYCQK t  WHERE to_char(t.scyf,'yyyy-MM-dd')" \
                 " like '2019-12-__'ORDER BY to_char(t.ksrq,'yyyy-MM-dd') ASC"  # 地区本月考试异常情况统计
data_dq_ycqk = pd.read_sql(sql_query_ycqk, engine1)  # Step1 : read csv
print('\n')
data_dq_ycqctj = data_dq_ycqk[['kcmc', 'ksrq', 'ycqk']]
print('地区本月产生考试异常情况预警信息的考场共：%s个，它们分别为：' % (data_dq_nlkc[['kcmc']].drop_duplicates().shape[0]))

zfdata_dq_ycqctj = ((data_dq_ycqctj[['kcmc']].drop_duplicates()).values.tolist())
# zfdata_dq_ycqctj = list(chain.from_iterable((data_dq_ycqctj[['kcmc']].drop_duplicates()).values.tolist()))
# print("".join(zfdata_dq_ycqctj))
res = []
for i, temp in enumerate(zfdata_dq_ycqctj):
    if temp != [None]:
        res.append(temp)
        print(res[i][0], end=',')  # 打印列表不换行！！！end='，'分隔
print(zfdata_dq_ycqctj[i][0], end=',')  # 打印列表不换行！！！end='，'分隔

print('\n')
# #利用list（）和tuple（）配合.index与.columns以及.values取出相应值。
pd.set_option('max_colwidth', 512)
print('地区本月产生考试异常情况所涉及场次日期如下：')
bgdata_dq_ycqctj = data_dq_ycqctj.pivot(index='kcmc', columns='ksrq', values='ycqk')
# pprint(tuple(bgdata_dq_ycqctj.index),width=80)
res1 = []
res2 = []
for i, temp in enumerate(tuple(bgdata_dq_ycqctj.columns)):
    if temp != None:
        print(temp, end='：')  # 打印列表不换行！！！end='，'分隔
        res1.append(temp)
        for i, temp1 in enumerate(bgdata_dq_ycqctj[temp].fillna('Null').values):  # 对字符串向对nan先填入特征值'Null'
            # if math.isnan(temp1):     #对纯数值有效，在之前不用去除。
            if temp1 != 'Null':  # 对特征值'Null'去除。
                print(textwrap.dedent(textwrap.fill(temp1, width=32)), end='\n')  # 采用textwrap.fill和.dedent解决字符串过长问题
                res2.append(temp1)

# 统计ycqk中的无%音视频%；没有车辆备案；监管中无三类等所涉及的考场名称：
# print(res2,end='\n')
# print(dict(zip(res1,res2)))


# 6、考试过程异常预警方面情况：
# （1）、重点扣分项（考试项目扣分表以及重点扣分项目）
sql_query_xmkf = "SELECT * from LS_KSXMKF t  WHERE to_char(t.scyf,'yyyy-MM-dd')" \
                 " like '2020-01-__'ORDER BY t.ksxm ASC"  # 地区本月考试项目扣分表情况统计
data_dq_xmkf = pd.read_sql(sql_query_xmkf, engine1)  # Step1 : read csv
print('\n')
data_dq_xmkftj = data_dq_xmkf[['kcmc', 'ksxm', 'kscs']]
print('地区本月产生考试项目扣分表情况预警统计信息的考场共：%s个，'
      '它们分别为：' % (data_dq_xmkf[['kcmc']].drop_duplicates().shape[0]), end='\n')
zfdata_dq_xmkftj = list(chain.from_iterable((data_dq_xmkftj[['kcmc']].drop_duplicates()).values.tolist()))
print(",".join(zfdata_dq_xmkftj), end='\n')
print(data_dq_xmkftj)
#
print('产生预警信息考场所涉及考试项目扣分为零判以及其此项目考试人数如下表：')
print(pd.pivot_table(data_dq_xmkftj, index='kcmc', columns='ksxm',
                     values='kscs').rename({'kcmc': '考场名称', 'ksxm': '考试项目'}, axis=1))
###重点扣分项
# 清洗数据：a.读入数据；b.数据预览；c.检查NULL值；d.补全空值；e.特征工程；f.编码；g.再check；
# 数据分析与挖掘：数据探索（质量分析、特征分析）、数据预处理（清洗、集成、变换、规约）、挖掘建模
# （分类预测、聚类分析、关联规则、时序分析、离群点检测）
sql_query_zdkfx = "SELECT * from ZDKFX_LS t  WHERE to_char(t.scyf,'yyyy-MM-dd')" \
                  " like '2020-01-__'ORDER BY t.KSRQ ASC"  # 地区本月考试项目扣分表情况统计
data_dq_zdkfx = pd.read_sql(sql_query_zdkfx, engine1)  # Step1 : read csv
print('\n')
# data_dq_zdkfx.kskm[data_dq_zdkfx['kcmc'] == '吉林市吉松鸿利科目三考场'] = '科目三'  # 对相应项进行修改
# data_dq_zdkfx.kskm[data_dq_zdkfx['kcmc'].str.contains('科目三')] = '科目三'
# data_dq_zdkfx['kskm'] = '科目二'

data_dq_zdkfx['kskm'] = '科目三'
data_dq_zdkfx.kskm[data_dq_zdkfx['kcmc'].str.contains('科目二')] = '科目二'

print(data_dq_zdkfx.sort_values('kskm'))
print('无重点扣分项涉及考场共%s家。如下：' % (data_dq_zdkfx[['kcmc']].drop_duplicates().shape[0]))
# zfdata_dq_zdkfx = ((data_dq_zdkfx[['kcmc']].drop_duplicates()).values.tolist())
# res = []
# for i, temp in enumerate(zfdata_dq_zdkfx):
#     if temp != [None]:
#         res.append(temp)
#         print(res[i][0], end=',')  # 打印列表不换行！！！end='，'分隔
# print(zfdata_dq_zdkfx[i][0], end=',')  # 打印列表不换行！！！end='，'分隔
# print('\n')
zfdata_dq_zdkfx = data_dq_zdkfx.groupby('kcmc')['yjms'].count()  # 利用groupby进行分组,对重点扣分项目进行汇总。
print(zfdata_dq_zdkfx, end='\n')
print('重点扣分项预警信息涉及考试系统设备厂商家以及其服务考场数和预警信息数，如下：')

# 2020-0505,产生考试系统设备提供商与考场间关系表（KSXTYKC）
sql_query_xtykc = "SELECT * from KSXTYKC t   WHERE to_char(t.scyf,'yyyy-MM-dd')" \
                  " like '2020-04-__'ORDER BY t.kskm,t.ksxtcsmc ASC"  # 当前考试系统设备提供商与考场间关系表
data_dq_xtykc = pd.read_sql(sql_query_xtykc, engine1)  # Step1 : read csv
data_xtykc = data_dq_xtykc[['kcmc', 'kskm', 'ksxtcsmc']]  # 取出有用的关系项
# print(data_xtykc, end='\n')

res3 = {}
res3['ksxtcsmc'] = []
res3['times'] = []

for i, temp in enumerate(data_dq_zdkfx['kcmc'].drop_duplicates()):
    if temp in data_xtykc['kcmc'].values.tolist():  # 转换成列表
        # print('%s  使用' % temp, end='\n')
        # print(data_xtykc[data_xtykc['kcmc'] == temp]['ksxtcsmc'].values[0], end='\n')
        # print(zfdata_dq_zdkfx[temp], end='\n')
        res3['ksxtcsmc'].append(data_xtykc[data_xtykc['kcmc'] == temp]['ksxtcsmc'].values[0])
        res3['times'].append(zfdata_dq_zdkfx[temp])
    else:
        print('%s  没使用任何考试系统设备' % temp, end='\n')

xt_times = pd.DataFrame(res3) #字典转列表
xt_times.groupby('ksxtcsmc')['times'].agg([len,np.sum])
print(xt_times.groupby('ksxtcsmc')['times'].agg([len,np.sum]),end='\n')
# print(data_dq_zdkfx,'\n')

# 清洗：找出表格ZDKFX_LS中yjms字段中重点扣分项：与无扣分记录！间的扣分代码并存入列表。
for id, temp in enumerate(data_dq_zdkfx['yjms']):
    # print(id,temp,end='\n')
    # 利用正则表达式提取各考场无记录的重点扣分项，并对比考场性质进行数据清洗。
    pattern1 = re.compile(r'重点扣分项：', re.IGNORECASE)
    keyworld_zdkf = pattern1.search(temp)
    # print(keyworld_zdkf.span()[1])                #确定所在下标位置；match中有搜索到的词。或者用start()和end()
    pattern2 = re.compile(r'无扣分记录！', re.IGNORECASE)
    keyworld_wkfjl = pattern2.search(temp)
    # print(keyworld_wkfjl.span()[0])
    # print('输出%s行：' % id, temp[keyworld_zdkf.span()[1] + 1:keyworld_wkfjl.span()[0]], end='\n')
    kfx = (temp[keyworld_zdkf.span()[1] + 1:keyworld_wkfjl.span()[0]]).split(",")
    # print(kfx, end='\n')     #原扣分项目
    # print('\n')
    km2kfdm_res1 = []
    km2kfdm_res2 = []

    km3kfdm_res1 = []
    km3kfdm_res2 = []

    # zhkm2kfdm_xxc = list(map(str,km2kfdm_xxc))
    # print(zhkm2kfdm_xxc)
    if data_dq_zdkfx.loc[id, 'kskm'] == '科目二':
        if data_dq_zdkfx.loc[id, 'kcmc'] in km2dxc_kcmc:
            for temp_kfda in kfx:  # 过滤扣分代码
                if temp_kfda in list(map(str, km2kfdm)):
                    km2kfdm_res1.append(temp_kfda)
                else:
                    km2kfdm_res2.append(temp_kfda)

            print('该考场名称为:%s,过滤后的该考场扣分代码为：' % data_dq_zdkfx.loc[id, 'kcmc'], set(km2kfdm_res1), end='\n')
            print('该考场名称为:%s,没通过过滤的该考场扣分代码为：' % data_dq_zdkfx.loc[id, 'kcmc'], set(km2kfdm_res2), end='\n')
        else:
            for temp_kfda in kfx:  # 过滤扣分代码
                if temp_kfda in list(map(str, km2kfdm_xxc)):
                    km2kfdm_res1.append(temp_kfda)
                else:
                    km2kfdm_res2.append(temp_kfda)

            print('该考场名称为:%s,过滤后的该考场扣分代码为：' % data_dq_zdkfx.loc[id, 'kcmc'], set(km2kfdm_res1), end='\n')
            print('该考场名称为:%s,没通过过滤的该考场扣分代码为：' % data_dq_zdkfx.loc[id, 'kcmc'], set(km2kfdm_res2), end='\n')

    else:
        for temp_kfda in kfx:  # 过滤扣分代码
            if temp_kfda in list(map(str, km3kfdm)):
                km3kfdm_res1.append(temp_kfda)
            else:
                km3kfdm_res2.append(temp_kfda)

        print('该考场名称为:%s,过滤后的该考场扣分代码为：' % data_dq_zdkfx.loc[id, 'kcmc'], set(km3kfdm_res1), end='\n')
        print('该考场名称为:%s,没通过过滤的该考场扣分代码为：' % data_dq_zdkfx.loc[id, 'kcmc'], set(km3kfdm_res2), end='\n')

data_dq_zdkfx['ksrq'] = data_dq_zdkfx['ksrq'].astype('datetime64[D]')  # 直接更改列数值类型
# print(data_dq_zdkfx['ksrq'].dtypes)
data_dq_zdkfx.reset_index()  # 设置索引必须先复位再设置。
data_dq_zdkfx.set_index('ksrq')  # 重新索引后补重新回赋不改变原索引的dataframe
# print(data_dq_zdkfx.set_index('ksrq')[:'2020-01-10'], end='\n')  # 查询指定天数前的日期

print('无重点扣分项涉及日期共%s天。' % (data_dq_zdkfx[['ksrq']].drop_duplicates().shape[0]))
print('无重点扣分项涉及具体日期,如下表：')
print(data_dq_zdkfx.set_index('yjlx')['ksrq'].drop_duplicates())

# mm = data_dq_zdkfx[['ksrq']].drop_duplicates()
#
# dates = pd.to_datetime(pd.Series(mm['ksrq'].to_list()), format='%Y-%m-%d %H:%M:%S')
#
# print('返回日期值:\n', dates.dt.date)
# print('返回季度：\n', dates.dt.quarter)
# print('返回几点钟: \n', dates.dt.hour)
# print('返回年中的天: \n', dates.dt.dayofyear)
# print('返回年中的周：\n', dates.dt.weekofyear)
# print('返回星期几的名称：\n', dates.dt.weekday)
# print('返回月份的天数：\n',dates.dt.days_in_month)


# （2）、考试时间过短
# 考试时间过短需要解决如下问题：
#a.无备案的考车考场；b.每个考场考试预警次数统计；C.每个考场考试发生的项目统计（精确到哪个项目，如侧方1）；
#d.每个考试系统提供商预警次数统计；f.多少考生触发预警；g.每个考生触发预警次数；h.多少考车触发预警，每个考车触发次数。
#
sql_query_xmsjgd = "SELECT * from XMKSSJGD_LS t  WHERE to_char(t.scyf,'yyyy-MM-dd')" \
                 " like '2020-01-__'ORDER BY t.kccp ASC"  # 地区本月考试项目扣分表情况统计
data_dq_xmsjgd = pd.read_sql(sql_query_xmsjgd, engine1)  # Step1 : read csv
data_xmsjgd = data_dq_xmsjgd[['kcmc', 'kssb', 'kccp']]  # 取出有用的关系项
print(data_xmsjgd,end='\n')

print('触发考试过短预警信息无考车备案考场如下：')
print(data_xmsjgd.query('kccp == [None]')['kcmc'].drop_duplicates().values.tolist(),end='\n')



# （3）、考试时间过长
# （4）、设备重叠
# （5）、考试成绩不一致
# （6）、考试过程异常预警数据综合分析：

# 7、考试员合格率情况：

# 8、综合分析，重点发现问题考场：
