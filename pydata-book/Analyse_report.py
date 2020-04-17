# 本程序依据总队考试监管通报总队考试监管通报内容进行数据完善

from decimal import Decimal
from functools import reduce
from itertools import chain
import math
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
# print(zfdata_dq_ycqctj[i][0], end=',')  # 打印列表不换行！！！end='，'分隔

print('\n')
# #利用list（）和tuple（）配合.index与.columns以及.values取出相应值。
pd.set_option('max_colwidth', 512)
print('地区本月产生考试异常情况所涉及场次日期如下表：')
bgdata_dq_ycqctj = data_dq_ycqctj.pivot(index='kcmc', columns='ksrq', values='ycqk')
# print(tuple(bgdata_dq_ycqctj.index))
res1 = []
res2 = []
for i, temp in enumerate(tuple(bgdata_dq_ycqctj.columns)):
    if temp != None:
        print(temp, end='：')  # 打印列表不换行！！！end='，'分隔
        res1.append(temp)
        for i, temp1 in enumerate(bgdata_dq_ycqctj[temp].fillna('Null').values):  # 对字符串向对nan先填入特征值'Null'
            # if math.isnan(temp1):     #对纯数值有效，在之前不用去除。
            if temp1 != 'Null':  # 对特征值'Null'去除。
                print(temp1, end='\n')
                res2.append(temp1)

# 统计ycqk中的无%音视频%；没有车辆备案；监管中无三类等所涉及的考场名称：
print(res2,end='\n')
print(dict(zip(res1,res2)))


# 6、考试过程异常预警方面情况：
# （1）、重点扣分项
# （2）、考试时间过短
# （3）、考试时间过长
# （4）、设备重叠
# （5）、考试成绩不一致
# （6）、考试过程异常预警数据综合分析：


# 7、考试员合格率情况：


# 8、考试员合格率情况：


# 9、综合分析，重点发现问题考场：
