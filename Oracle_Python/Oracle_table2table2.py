#本程序实现对已存在月统计信息等表数据的建立备份表。不同数据库之间倒库。

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
database1_Tables = 'jsrkshgl'
# ['jsrkshgl','ksyhgl','jsrydkshgl','km2ccksnl','ksycqk','ksxmkf','km2ycshzb'] #total seven


username2 = 'world'
password2 = '1'
host_port2 = 'localhost:1521'
database2 = 'ORCL'


engine1 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username1, password1, host_port1, database1),encoding='utf-8', echo=True)
engine2 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username2, password2, host_port2, database2),encoding='utf-8', echo=True)



dtypedict = {'kskm': sqlalchemy.types.NVARCHAR(length=255), 'xm': sqlalchemy.types.NVARCHAR(length=255),
                     'ksrs': sqlalchemy.types.INTERVAL, 'hgrs': sqlalchemy.types.INTERVAL,
                     'hgl': sqlalchemy.types.INTERVAL, 'scyf': sqlalchemy.types.DATE()}

    data = pd.read_sql("select * from %s" % (Table_Name), engine1)
    print(data.head())
    data.to_sql(Table_Name+'_LS', con=engine2, index=False, if_exists='append', dtype=dtypedict, chunksize=100)
print("全部表传输完成！！！")