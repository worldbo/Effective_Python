# 月异常数据分析程序---DATE:20200101 version：1.0 ---author：bzy
import xlrd
import xlwt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import re
import os
import cx_Oracle

os.getcwd()  # 判断当前程序文件的路径

# 连接Oracle数据库，下面括号里内容根据自己实际情况填写
# conn = cx_Oracle.connect('用户名/密码@IP:端口号/SERVICE_NAME')
conn = cx_Oracle.connect('scott', 'tiger', 'localhost:1521/ORCL')
# conn1 = cx_Oracle.connect('scott/tiger@localhost:1521/ORCL')
dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'ORCL')
print(dsn_tns)
print(conn.version)  # 判断是否链接成功oracle

# 每月Excel表格数据清洗与导入Oracle：

# ===============定义表格参数==========================================================
EXcel_FilesPath = 'F:/2020年社会化考场违规情况汇总/一月份/通报数据/'
EXcel_Files = '吉林1月异常数据统计.xlsx'
Sheet_Names = ' 考试系统时间异常 '  # '项目考试时间过短 ','车速为零','重点扣分项目无记录',
# ' 考试成绩计算不一致 ','项目完成时间超长 '
# =====================================================================================

File_Data = pd.read_excel(EXcel_FilesPath + EXcel_Files, Sheet_Names)
# 获取最大行，最大列
nrows = File_Data.shape[0]
ncols = File_Data.columns.size
print("=========================================================================")
print('Max Rows:' + str(nrows))
print('Max Columns' + str(ncols))
print("=========================================================================")

File_Data['流水号'] = [' %i' % i for i in File_Data['流水号']]  # 解决科学技术法符号问题

File_Data1 = File_Data.sort_values(by=['考试日期', '预警描述'],
                                   ascending=[True, False])  # sort是以###为标准排序 ascending=True,升序排序
# data1.to_excel(string+'.xls',sheet_name='string', encoding='utf-8')
File_Data1.to_excel(EXcel_FilesPath + 'ls_out.xls', Sheet_Names, index=False, encoding='utf-8')  # 写入一个临时表
print('生成临时文件：' + EXcel_FilesPath + 'ls_out.xls' + '成功！！！')
print("================================ Finish ============================")

# 每月对导入数据的分析：

# 使用cursor()方法获取操作游标
cursor = conn.cursor()

# =====================导入===============================================


# ======================分析================================================

query = cursor.execute("select * from LS_KSXTSJYC t")

# 获取所有数据
all_data = cursor.fetchall()
# print(all_data)
for i, ROW_Data in enumerate(all_data):
    print('第 %s 列: %s：' % (i + 1, ROW_Data))
    for ROW_Item in ROW_Data:
        print(ROW_Item)

# 关闭光标与数据库
cursor.close()

# cursor1.close()
conn.close()
