import xlrd
import xlwt
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

def To_Numbers(strTargetField):
    numResult = "TO_NUMBER(decode(decode(lower(nvl(replace(translate(" + strTargetField + \
    ", '$%', ' '),' ',''),0)),upper(nvl(replace(translate(" + strTargetField + \
    ", '$%', ' '), ' ', ''), 0)), 1, 0), 1,nvl(replace(translate(" + strTargetField + \
    ", '$%', ' '),' ',''),0),0))"
    return (numResult)

print(To_Numbers('hgl'))

engine1 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username1, password1, host_port1, database1),
                        encoding='utf-8', echo=True)

###查询相关表格并进行简单分析
sql_query = "select * from KM2YCSHZB t WHERE %s > 61.6 ORDER BY to_number(ksrs) DESC" % (To_Numbers('hgl'))
data = pd.read_sql(sql_query, engine1)  # Step1 : read csv
print(data.head())

data.info()
print(data.describe(include='all'))  # Step2 : preview data

data1 = data.copy(deep=True)  # Step3: check null value for every column
print(data1)
print(data1.isnull().sum())
