import os
import re
import datetime
import time
import xlrd
import xlwt
import numpy as np
import pandas as pd

EXcel_FilesPath = 'F:/2020年社会化考场违规情况汇总/一月份/通报数据/'
EXcel_Files = '吉林1月异常数据统计1.xlsx'
Sheet_Names = ' 考试系统时间异常 '

#去除读取Excel文件中数据（字符串前）的空格

def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text

def make_int(text):
    return int(text.strip('" '))

def make_date(text):
    return make_date(text.strip('" '))



File_Data = pd.read_excel(EXcel_FilesPath + EXcel_Files, Sheet_Names)
print(File_Data)
temp = File_Data.replace('\s+','',regex=True,inplace=True)  ###
# table = pd.read_table("data.csv", sep=r',',
#                       names=["Year", "Make", "Model", "Description"],
#                       converters = {'Description' : strip,
#                                     'Model' : strip,
#                                     'Make' : strip,
#                                     'Year' : make_int})
# print(table)
# names=['预警类型', '流水号', '考试科目', '考试日期',
#                        '考场名称', '考试设备', '考车号牌', '预警描述','生成月份'],
#                       converters = {'预警类型' : strip,
#                                     '流水号' : strip,
#                                     '考试科目' : strip,
#                                     '考试日期': strip,
#                                     '考场名称': strip,
#                                     '考试设备' : strip,
#                                     '考车号牌' : strip,
#                                     '预警描述': strip,
#                                     '生成月份': strip}))
print(File_Data)
print(temp)