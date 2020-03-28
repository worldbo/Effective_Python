import xlrd
import xlwt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import re
import os

# os.getcwd()

# 依次读取多个相同结果的excel文件并创建DataFrame

dfs = []

# 根据需要的excel文件数调整数字5
# for i in range(1, 5):
# 先利用dos命令len批量改excel文件名为调查问卷i
# 前面加r表示原始字符串，不然在路径\U下会报错，程序误以为八进制,注意名称的空格
# CCYD_Data = r"F:\1\0226.xls"
# data = pd.read_excel(CCYD_Data)
# dfs.append(data.iloc[2:6,1:4])
# data.iloc方法，第一个参数指定行，第二个参数指定列，类似于python中的数组切片操作
# 例如：data.iloc[2:6,0:9]
# 将多个DataFrame合并为一个

# df = pd.concat(dfs)

# 写入Excel文件，index = False不包含索引数据，暂理解成表头
# 保存在自己桌面)
# 如果不加r,可以写成df.to_excel（C:\\User\TQF\Desktop\pythonsy\汇总.xlsx', index = False)
# 只要去掉\U变八进制的影响就好
# df.to_excel(r'F:\1\out.xls', index=False)

# import pandas as pd
#
# file1 = 'C:/Users/Administrator/Desktop/00/1.xlsx'
# file2 = 'C:/Users/Administrator/Desktop/00/3.xlsx'
# file3 = 'C:/Users/Administrator/Desktop/00/21.xlsx'
# file = [file1, file2, file3]
# li = []
# for i in file:
#     li.append(pd.read_excel(i))
# writer = pd.ExcelWriter('C:/Users/Administrator/Desktop/00/output.xlsx')
# pd.concat(li).to_excel(writer, 'Sheet1', index=False)
#
# writer.save()
#
########################################
# input_file = open("F:/1/0226.xls", mode='r', encoding='utf-8')
# output_file = open("F:/1/out.xls","w")
#
# table = []
# header = input_file.readline() #读取并弹出第一行
# for line in input_file:
#     col = line.split(',') #每行分隔为列表，好处理列格式
#     col[3] = float(col[3][1:-1])
#     col[4] = int(col[4][1:-2]) #各行没有先strip 末位是\n
#     table.append(col) #嵌套列表table[[8,8][*,*],...]
#
# table_sorted = sorted(table, key=itemgetter(3, 4))#先后按列索引3,4排序
#
# output_file.write(header + '\t')
# for row in table_sorted:                    #遍历读取排序后的嵌套列表
#     row = [str(x) for x in row]             #转换为字符串格式，好写入文本
#     output_file.write("\t".join(row) + '\n')
#
# input_file.close()
# output_file.close()

########################################################
CCYD_Data = r"F:\1\0227.xlsx"
sheet_name = '长春二道科目三'
file_data = pd.read_excel(CCYD_Data,sheet_name)
# 获取最大行，最大列
nrows = file_data.shape[0]
ncols = file_data.columns.size
print("=========================================================================")
print('Max Rows:' + str(nrows))
print('Max Columns' + str(ncols))
print("=========================================================================")
# file_data['流水号'] = [' %i' % i for i in file_data['流水号']]
# file_data['管理部门'] = [' %i' % i for i in file_data['管理部门']]
# file_data['变更前流水号'] = [' %i' % i for i in file_data['变更前流水号']]  # 解决科学技术法符号问题
file_data1 = file_data.sort_values(by=['身份证明号码', '考试时间', '考场名称'],
                                   ascending=[False, True, False])  # sort是以###为标准排序 ascending=True,升序排序
# data1.to_excel(string+'.xls',sheet_name='string', encoding='utf-8')
file_data1.to_excel(r'F:\1\out.xls', sheet_name, index=False, encoding='utf-8')
print("================================ Finish ============================")
