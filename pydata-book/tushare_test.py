# import math
# import xlrd
# import xlwt
# import re
# import nltk
# from re import sub
import numpy as np
import pandas as pd
import time
# from datetime import datetime
# from matplotlib import pyplot as plt
# import difflib
import tushare as ts
#
# # 查看pandas的文档，这个问题可以通过pandas内置的set_option()方法解决，
# # 从上面的属性设置中可以看到，与显示的行数列数有关的选项主要是【display】
# # 中的【max_columns,max_rows,max_colwidth,line_width】等这几项，只需要
# # 将这几项属性值设置得大一些就可以解决。
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)  # 设置打印宽度(**重要**)
pd.set_option('expand_frame_repr', False) #数据超过总宽度后，是否折叠显示
#
# # 存款利率等宏观经济数据
# # df_data1 = ts.get_deposit_rate()
# # print(df_data1, end='\n')  # 存款利率
# # print(ts.get_loan_rate(), end='\n')  # 贷款利率
# # print(ts.get_rrr(), end='\n') #存款准备金率
# # print(ts.get_money_supply(), end='\n') #货币供应量
#
# # 获取实时电影票房数据，30分钟更新一次票房数据，可随时调用。
# # df_data1 = ts.realtime_boxoffice()
# # print(df_data1, end='\n')  # 实时电影票房


# # df_data = ts.get_hist_data('600848',start='2020-05-20',end='2020-05-29')
# # ts.get_hist_data('600848', ktype='W') #获取周k线数据
# # ts.get_hist_data('600848', ktype='M') #获取月k线数据
# # ts.get_hist_data('600848', ktype='5') #获取5分钟k线数据
# # ts.get_hist_data('600848', ktype='15') #获取15分钟k线数据
# # ts.get_hist_data('600848', ktype='30') #获取30分钟k线数据
# # ts.get_hist_data('600848', ktype='60') #获取60分钟k线数据
# # ts.get_hist_data('sh'）#获取上证指数k线数据，其它参数与个股一致，下同
# # ts.get_hist_data('sz'）#获取深圳成指k线数据
# # ts.get_hist_data('hs300'）#获取沪深300指数k线数据
# # ts.get_hist_data('sz50'）#获取上证50指数k线数据
# # ts.get_hist_data('zxb'）#获取中小板指数k线数据
# # ts.get_hist_data('cyb'）#获取创业板指数k线数据
#
# # ts.get_h_data('002337') #前复权
# # ts.get_h_data('002337', autype='hfq') #后复权
# # ts.get_h_data('002337', autype=None) #不复权
# # ts.get_h_data('002337', start='2015-01-01', end='2015-03-16') #两个日期之间的前复权数据
# #
# # ts.get_h_data('399106', index=True) #深圳综合指数
# # ts.get_today_all() #一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
#
# # df = ts.get_tick_data('600848',date='2018-12-12',src='tt') #获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。
# # df.head(10)
# # df = ts.get_sina_dd('600848', date='2015-12-24') #获取大单交易数据，默认为大于等于400手，数据来源于新浪财经。
# # df = ts.get_sina_dd('600848', date='2015-12-24', vol=500)  #指定大于等于500手的数据
#
# # df_data = ts.get_index() #获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。
#
my_stocks = ['601577', '002297', '601390', '601989']
my_stocks_price = [7.803,5.486,5.015,4.162]

print('开始刷新实时数据**********************************************************************************************************',end='\n')
while True:
    for i, temp in enumerate(my_stocks):
        # df_data1 = ts.get_hist_data(temp, start='2020-05-29', end='2020-06-01')
        df = ts.get_realtime_quotes(temp)  # 获取实时分笔数据，可以实时取得股票当前报价和成交信息，
        my_price_difference = float(df['price'].iloc[0]) - my_stocks_price[i]
        df_stocks_name = df[['name']].iloc[0].values.tolist()[0]
        df_data = df[['code', 'name', 'high', 'low', 'price', 'bid', 'ask', 'volume', 'amount', 'date', 'time']].copy()
        df_data.rename(columns={'code': '代码','name': '名称','high':'最高', 'low':'最低','price': '现价','bid':'竞买','ask':'竞卖','volume':'成交量','amount':'成交金额','date':'日期','time':'时间'}, inplace=True)
        print('第%s支股票:%s，目前差价%.2f' % (i+1, df_stocks_name,my_price_difference), end='\n')
        print(df_data)
        print('——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————',end='\n')
    time.sleep(10)
    print('\n\n\n')

    print('继续刷新实时数据**********************************************************************************************************',end='\n')
    print('\n')