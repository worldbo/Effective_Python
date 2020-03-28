import pymysql
import xlrd
import xlwt
# import XlsxWriter
import numpy as np
import pandas as pd
import sqlalchemy as sqla
import openpyxl as oxl
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from sqlalchemy import create_engine
import re
import os

csv_file_path = 'F:/1/'
csv_filename = '0226.xlsx'
database = 'csvdata'
sheetname = '辽源,从通化转入'
table_name = '0226'

db = sqla.create_engine('mysql+pymysql://root:world_bo@127.0.0.1:3306/sakila?charset=utf8')
print(pd.read_sql('select * from actor;', db))
df = pd.read_excel(csv_file_path + csv_filename)
print(df)
data = xlrd.open_workbook(csv_file_path + csv_filename)
sheet_1_data = data.sheet_by_name(sheetname)
print(sheet_1_data.row_values(0))

# 利用openpyxl库  金融大数据分析 page332

# file_1 = oxl.load_workbook(csv_file_path + csv_filename)
# data_1 = file_1.get_active_sheet()
# print(data_1)

# def excel_upload(request):
#     data = {"code": 0, "data": [], "msg": ''}
#     excel_obj = request.FILES.get('excel_save')
#     try:
#         excel_data = pd.read_excel(excel_obj)
#     except Exception as e:
#         print('excel_upload', str(e))
#         data["msg"] = '读取文件错误！'
#         return JsonResponse(data)
#     excel_data["data_time"] = excel_data["data_time"].map(lambda x: str(x).split("")[0])
#     print(excel_data)
#     db= sqla.create_engine('mysql+pymysql://root:你的数据库密码@你的服务器公网IP:数据库端口号/数据库名?charset=utf8')tf8')
# try:
#     excel_data.to_sql('score', con=mysql_engine, if_exists="append", index=False)
# except Exception as e:
#     print('pd2mysql', str(e))
# data['msg'] = '上传并保存成功'
# data["code"] = 1
# return JsonResponse(data)
#
