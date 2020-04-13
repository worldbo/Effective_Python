#本程序实现对已存在表数据的建立备份表。不同数据库之间倒库。

iimport xlrd
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
database1_Tables = ['KSXTSJYC','CSWL','XMKSSJGD','ZDKFX','KSCJBYZ','XMWCSJCC']

username2 = 'world'
password2 = '1'
host_port2 = 'localhost:1521'
database2 = 'ORCL'


engine1 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username1, password1, host_port1, database1),encoding='utf-8', echo=True)
engine2 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username2, password2, host_port2, database2),encoding='utf-8', echo=True)
                       #"//scott:tiger@localhost:1521/ORCL",encoding='utf-8', echo=True)

#向sql语句中传递参数，第一种方法：
# for Table_Name in database1_Tables:
#     print(Table_Name)
#     sql_select = "select * from {}"
#     sql_select1 = sql_select.format(Table_Name)
#     print(sql_select1)
#     data = pd.read_sql(sql_select1, engine1)  # Step1 : read csv
#     print(data.head())

#向sql语句中传递参数，第二种方法：使用的是正则法，也就是利用 re.sub 这个方法将需要的SQL内容替换掉，
# 这样的好处就是可以替换任意内容，缺点就是必须每次使用的时候 import re.sub。
for Table_Name in database1_Tables:
    if Table_Name != 'XMWCSJCC':
        dtypedict = {'yjlx': sqlalchemy.types.NVARCHAR(length=1024), 'lsh': sqlalchemy.types.NVARCHAR(length=255),
                     'kskm': sqlalchemy.types.NVARCHAR(length=255), 'ksrq': sqlalchemy.types.DATE(),
                     'kcmc': sqlalchemy.types.NVARCHAR(length=255), 'kssb': sqlalchemy.types.NVARCHAR(length=255),
                     'kccp': sqlalchemy.types.NVARCHAR(length=255), 'yjms': sqlalchemy.types.NVARCHAR(length=1024),
                     'scyf': sqlalchemy.types.DATE()}
        print('不是XMWCSJCC')
    else:
        dtypedict = {'yjlx': sqlalchemy.types.NVARCHAR(length=1024), 'xm': sqlalchemy.types.NVARCHAR(length=1024),
                      'kskm': sqlalchemy.types.NVARCHAR(length=255),'ksrq': sqlalchemy.types.DATE(),
                      'kcmc': sqlalchemy.types.NVARCHAR(length=255),'yjms': sqlalchemy.types.NVARCHAR(length=255),
                      'scyf': sqlalchemy.types.DATE()}
        print('是XMWCSJCC')
    print(Table_Name)
    data = pd.read_sql("select * from %s" % (Table_Name), engine1)
    print(data.head())
    data.to_sql(Table_Name+'_LS', con=engine2, index=False, if_exists='append', dtype=dtypedict, chunksize=100)
print("全部表传输完成！！！")