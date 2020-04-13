# 本程序实现对已存在月统计信息等表数据的建立备份表。不同数据库之间倒库。

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

username1 = 'scott'
password1 = 'tiger'
host_port1 = 'localhost:1521'
database1 = 'ORCL'
database1_Tables = ['JSRKSHGL','ksyhgl','jsrydkshgl','km2ccksnl','ksycqk','km2ycshzb','ksxmkf'] #total seven
database1_Tables = [item.upper() for item in database1_Tables] #对列表内容转换大小写['JSRKSHGL', 'KSYHGL', 'JSRYDKSHGL', 'KM2CCKSNL', 'KSYCQK', 'KSXMKF', 'KM2YCSHZB']


username2 = 'world'
password2 = '1'
host_port2 = 'localhost:1521'
database2 = 'ORCL'

engine1 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username1, password1, host_port1, database1),
                        encoding='utf-8', echo=True)
engine2 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username2, password2, host_port2, database2),
                        encoding='utf-8', echo=True)

for Table_Name in database1_Tables:
    if Table_Name == 'KM2YCSHZB':
        dtypedict = {'dq': sqlalchemy.types.NVARCHAR(length=255), 'ksrs': sqlalchemy.types.FLOAT,
                     'hgrs': sqlalchemy.types.FLOAT, 'hgl': sqlalchemy.types.FLOAT,
                     'kssjczsbcd': sqlalchemy.types.FLOAT, 'xmkssjgd': sqlalchemy.types.FLOAT,
                     'zdkfxwjl': sqlalchemy.types.FLOAT, 'kscjjsbyz': sqlalchemy.types.FLOAT,
                     'cgqtmck': sqlalchemy.types.FLOAT, 'xmwcsjcc': sqlalchemy.types.FLOAT,
                     'ycsjzj': sqlalchemy.types.FLOAT, 'zb': sqlalchemy.types.FLOAT,
                     'scyf': sqlalchemy.types.DATE()}
        print('是报表:%s' % Table_Name)
        data = pd.read_sql("select * from %s" % (Table_Name), engine1)
        print(data.head())
        data["hgl"] = data["hgl"].apply(lambda x: x.replace("%", "")).astype("float") / 100
        data["zb"] = data["zb"].apply(lambda x: x.replace("%", "")).astype("float") / 100

    elif Table_Name == 'KM2CCKSNL':
        dtypedict = {'dq': sqlalchemy.types.NVARCHAR(length=255), 'bykskcsl': sqlalchemy.types.FLOAT,
                     'ksrq': sqlalchemy.types.DATE(),'kcmc': sqlalchemy.types.NVARCHAR(length=255),
                     'yjsl': sqlalchemy.types.FLOAT,'yjzb': sqlalchemy.types.FLOAT, 'scyf': sqlalchemy.types.DATE()}
        print('是报表:%s' % Table_Name)
        data = pd.read_sql("select * from %s" % (Table_Name), engine1)
        print(data.head())
        data["yjzb"] = data["yjzb"].apply(lambda x: x.replace("%", "")).astype("float") / 100

    elif Table_Name == 'KSYCQK':
        dtypedict = {'dq': sqlalchemy.types.NVARCHAR(length=255),'ksrq': sqlalchemy.types.DATE(),
                     'kcmc': sqlalchemy.types.NVARCHAR(length=255),'kskm': sqlalchemy.types.NVARCHAR(length=255),
                     'ycqk': sqlalchemy.types.NVARCHAR(length=1024),'ksy': sqlalchemy.types.NVARCHAR(length=255),
                     'scyf': sqlalchemy.types.DATE()}
        print('是报表:%s' % Table_Name)
        data = pd.read_sql("select * from %s" % (Table_Name), engine1)
        print(data.head())

    elif Table_Name == 'KSXMKF':
        dtypedict = {'kcmc': sqlalchemy.types.NVARCHAR(length=255), 'ksxm': sqlalchemy.types.NVARCHAR(length=255),
             'qdqkscs': sqlalchemy.types.FLOAT, 'qdqkskfl': sqlalchemy.types.FLOAT,
             'kscs': sqlalchemy.types.FLOAT, 'kskfl': sqlalchemy.types.FLOAT,
             'scyf': sqlalchemy.types.DATE()}
        print('是报表:%s' % Table_Name)
        data = pd.read_sql("select * from %s" % (Table_Name), engine1)
        print(data.head())
        data["qdqkskfl"] = data["qdqkskfl"].apply(lambda x: x.replace("%", "")).astype("float") / 100
        data["kskfl"] = data["kskfl"].apply(lambda x: x.replace("%", "")).astype("float") / 100

    else:
        print('是报表:%s' % Table_Name)
        dtypedict = {'kskm': sqlalchemy.types.NVARCHAR(length=255), 'xm': sqlalchemy.types.NVARCHAR(length=255),
                     'ksrs': sqlalchemy.types.FLOAT, 'hgrs': sqlalchemy.types.FLOAT,
                     'hgl': sqlalchemy.types.FLOAT, 'scyf': sqlalchemy.types.DATE()}
        data = pd.read_sql("select * from %s" % (Table_Name), engine1)
        print(data.head())
        data["hgl"] = data["hgl"].apply(lambda x: x.replace("%", "")).astype("float") / 100


    data.to_sql('LS_' + Table_Name, con=engine2, index=False, if_exists='append', dtype=dtypedict, chunksize=100)

print("传输完成！！！")



def convert_currency(var):  # 函数可以将货币进行转化
    """
    convert the string number to a float
    _ 去除$
    - 去除逗号，
    - 转化为浮点数类型
    """
    new_value = var.replace(",", "").replace("$", "")
    return float(new_value)


# df["2016"].apply(lambda x: x.replace(",","").replace("$","")).astype("float64")
# 同样可以利用lambda表达式将PercentGrowth进行数据清理
# df["Percent Growth"].apply(lambda x: x.replace("%","")).astype("float")/100
# 最后一个自定义函数是利用np.where() function 将Active 列转化为布尔值。
# df["Active"] = np.where(df["Active"] == "Y", True, False)


# data = pd.read_sql("select * from %s" % (Table_Name), engine1)
# print(data.head())
# data['hgl'] = data['hgl'].astype('int') #强制转换
# 然后列带有特殊符号（%$）的object是不能直接通过astype("float")方法进行转化的，
# 这与python中的字符串转化为浮点数，都要求原始的字符都只能含有数字本身，不能含有其他的特殊字符
# 我们可以试着将将Active列转化为布尔值，看一下到底会发生什么,五个结果全是True，说明并没有起到什么作用
# data["hgl"] = data["hgl"].apply(lambda x: x.replace("%", "")).astype("float") / 100
# data.to_sql(Table_Name + '_LS', con=engine2, index=False, if_exists='append', dtype=dtypedict, chunksize=100)
# print("传输完成！！！")
