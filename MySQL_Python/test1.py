# 导入pymysql方法
import pymysql
import xlrd
import xlwt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import re
import os

many = True
csv_file_path = 'F:/1/0226.xls'
csv_filename = '0226.xls'
database = 'evdata'
table_name = ''

# 连接数据库
config = {'host': 'localhost',
          'port': 3306,
          'user': 'root',
          'password': 'world_bo',
          'charset': 'utf8mb4',
          'local_infile': 1
          }
conn = pymysql.connect(**config)
cur = conn.cursor()
cur.execute('SHOW DATABASES')
print(cur.fetchall())
dab = cur.execute('USE test')
cur.execute('SHOW TABLES')
print(cur.fetchall())
table_number = cur.execute('SELECT * FROM `sp2cc` WHERE sp2cc.`流水号` = 2190718273142;')
if many:
    result = cur.fetchall()
    print('多条', result)
else:
    result = cur.fetchone()  # {''}
    print('单条', result)
cur.close()
conn.close()




def load_csv(csv_file_path, table_name, database='evdata'):
    # 打开csv文件
    file = open(csv_file_path, 'r', encoding='utf-8')
    # 读取csv文件第一行字段名，创建表
    reader = file.readline()
    b = reader.split(',')
    colum = ''
    for a in b:
        colum = colum + a + ' varchar(255),'
    colum = colum[:-1]
    # 编写sql，create_sql负责创建表，data_sql负责导入数据
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'
    data_sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES" % (
        csv_filename, table_name)

    # 使用数据库
    cur.execute('use %s' % database)
    # 设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 执行create_sql，创建表
    cur.execute(create_sql)
    # 执行data_sql，导入数据
    cur.execute(data_sql)
    conn.commit()
    # 关闭连接
    conn.close()
    cur.close()
