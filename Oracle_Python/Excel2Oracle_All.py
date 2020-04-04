import os
import re
import datetime
import time
import threading
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


def log(message, when=None):
    """Log a messge with a timestamo

    Args:
        message:Message to print
        when:datatime of when the message occurred
            Defaults to the present time."""

    when = datetime.datetime.now() if when is None else when
    print('%s:%s' % (when, message))


# 建立方法将pandas.DataFrame中列名和预指定的类型映射
def mapping_df_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: NVARCHAR(length=255)})
        if "float" in str(j):
            dtypedict.update({i: FLOAT(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtypedict.update({i: DOUBLE_PRECISION()})
    return dtypedict


# 对DataFrame的列标签进行修改
def named_df_Columns(df):
    df.rename(columns={'预警类型': 'yjlx', '流水号': 'lsh', '考试科目': 'kskm', '考试日期': 'ksrq',
                       '考场名称': 'kcmc', '考试设备': 'kssb', '考车号牌': 'kccp', '预警描述': 'yjms',
                       '生成月份': 'cyf'}, inplace=True)


# 定义函数，自动输出DataFrme数据写入oracle的数类型字典表,配合to_sql方法使用(注意，其类型只能是SQLAlchemy type )
# dtypedict = {'yjlx': sqlalchemy.types.NVARCHAR(length=255),'lsh': sqlalchemy.types.NVARCHAR(length=255),
#                 'kskm': sqlalchemy.types.NVARCHAR(length=255),'ksrq': sqlalchemy.types.DATE(),
#                 'kcmc': sqlalchemy.types.NVARCHAR(length=255),'kssb': sqlalchemy.types.NVARCHAR(length=255),
#                 'kccp': sqlalchemy.types.NVARCHAR(length=255),'yjms': sqlalchemy.types.NVARCHAR(length=255),
#                 'scyf': sqlalchemy.types.DATE()}

# 连接Oracle
engine = create_engine("oracle+cx_oracle://scott:tiger@localhost:1521/ORCL", encoding='utf-8', echo=True)

os.getcwd()  # 判断当前程序文件的路径

# 每月Excel表格数据清洗与导入Oracle：
# ===============定义表格参数==========================================================
EXcel_FilesPath = 'F:/2020年社会化考场违规情况汇总/一月份/通报数据/'
EXcel_Files = '吉林1月异常数据统计.xlsx'
Sheet_Names = ' 考试系统时间异常 '  # '项目考试时间过短 ','车速为零','重点扣分项目无记录',
# ' 考试成绩计算不一致 ','项目完成时间超长 '#也可直接赋值或指定sheet_name = [0, '车速为零', 'Sheet4']，
# ================读取表格中的数据=========================================================
File_Data = pd.read_excel(EXcel_FilesPath + EXcel_Files, Sheet_Names)
named_Columns = named_df_Columns(File_Data)
print(File_Data)
print(File_Data.dtypes)
# 获取最大行，最大列
nrows = File_Data.shape[0]
# nrows = File_Data.index.size
ncols = File_Data.shape[1]
# ncols = File_Data.columns.size
print("=========================================================================")
print('Max Rows:' + str(nrows))
print('Max Columns' + str(ncols))
print("=========================================================================")
log('正在导入，请耐心等待！！！!')
try:
    # 解析sql语句
    dtypedict = mapping_df_types(File_Data)  # 调列名和预指定的类型映射方法
    File_Data.to_sql('LS_KSXTSJYC2', con=engine, index=False, if_exists='append', dtype=dtypedict, chunksize=100)
    # 捕获SQL异常
    time.sleep(0.1)
    log('导入完成!!')
except Exception as e:
    print(e)
    log('导入出错!!')
