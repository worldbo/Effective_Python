import xlrd
import xlwt
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import openpyxl
import xlwings as xw

########################################################
CCYD_Data = r"F:\1\0227.xlsx"
sheet_all = ['长春二道科目三','不足10人次']
writer = pd.ExcelWriter(r'F:/1/out.xls')
for sheet_name in sheet_all:
    book = load_workbook('F:/1/123.xlsx')
    writer.book = book
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
    file_data1.to_excel(writer, sheet_name)

    #file_data1.to_excel(writer, sheet_name, index=0)
    writer.save()
writer.close()
    #file_data1.to_excel(r'F:\1\out.xls', sheet_name, index=False, encoding='utf-8')
print("================================ Finish ============================")