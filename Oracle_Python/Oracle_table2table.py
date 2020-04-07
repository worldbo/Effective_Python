#本程序实现对已存在表数据的建立备份表。不同数据库之间倒库。

import xlrd
import xlwt

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


#定义函数，自动输出DataFrme数据写入oracle的数类型字典表,配合to_sql方法使用(注意，其类型只能是SQLAlchemy type )
dtypedict = {'yjlx': sqlalchemy.types.NVARCHAR(length=1024),'lsh': sqlalchemy.types.NVARCHAR(length=255),
                'kskm': sqlalchemy.types.NVARCHAR(length=255),'ksrq': sqlalchemy.types.DATE(),
                'kcmc': sqlalchemy.types.NVARCHAR(length=255),'kssb': sqlalchemy.types.NVARCHAR(length=255),
                'kccp': sqlalchemy.types.NVARCHAR(length=255),'yjms': sqlalchemy.types.NVARCHAR(length=1024),
                'scyf': sqlalchemy.types.DATE()}

# dtypedict = {'yjlx': sqlalchemy.types.NVARCHAR(length=1024),'xm': sqlalchemy.types.NVARCHAR(length=1024),
#               'kskm': sqlalchemy.types.NVARCHAR(length=255),'ksrq': sqlalchemy.types.DATE(),
#               'kcmc': sqlalchemy.types.NVARCHAR(length=255),'yjms': sqlalchemy.types.NVARCHAR(length=255),
#              'scyf': sqlalchemy.types.DATE()}

engine1 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username1, password1, host_port1, database1),encoding='utf-8', echo=True)
engine2 = create_engine("oracle+cx_oracle://{}:{}@{}/{}".format(username2, password2, host_port2, database2),encoding='utf-8', echo=True)
                       #"//scott:tiger@localhost:1521/ORCL",encoding='utf-8', echo=True)

data = pd.read_sql("select * from KSXTSJYC t",engine1)

print(data.head())

data.to_sql('KSXTSJYC_LS',con=engine2,index=False,if_exists='append',dtype=dtypedict,chunksize=100)