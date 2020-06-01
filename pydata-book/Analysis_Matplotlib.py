# 接Analyse_report.py程序：
# 8、综合分析，重点发现问题考场：
# 本程序依据总队考试监管通报总队考试监管通报内容进行数据完善
# 清洗数据：a.读入数据；b.数据预览；c.检查NULL值；d.补全空值；e.特征工程；f.编码；g.再check；
# 数据分析与挖掘：数据探索（质量分析、特征分析）、数据预处理（清洗、集成、变换、规约）、挖掘建模
# （分类预测、聚类分析、关联规则、时序分析、离群点检测）

# 亲和性问题：数据集中不同变量之间的相关性。
# 分类问题：根据已知类别的数据集，经过训练得到分类模型，再用该模型对类别未知的数据集进行分类。
#
# 规则的优劣衡量最简单的方法：支持度（Support）和置信度（Confidence）
# 支持度是指数据集中规则应验的次数，比例。
# 置信度是指规则的准确率是多少。
# OneR算法：One Rule（一条规则简写）根据已有的数据中，具有相同特征值的个体最可能属于哪个类别
# 的进行分类，只选择选取特征中分类效果最好的一个用作分类依据。


from decimal import Decimal
from functools import reduce
from itertools import chain
import logging
import textwrap
from pprint import pprint
import math
import xlrd
import xlwt
import re
import nltk
from re import sub
import numpy as np
import pandas as pd
from sparklines import sparklines
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.dialects.oracle import \
    BFILE, BLOB, CHAR, CLOB, DATE, \
    DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
    NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
    VARCHAR2
import time
from datetime import datetime
from matplotlib import pyplot as plt
# !pip install brewer2mpl
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
import warnings

warnings.filterwarnings(action='once')

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['simhei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 定义sparklines函数用于展现数据分布
def sparkline_str(x):
    bins = np.histogram(x)[0]
    sl = ''.join(sparklines(bins))
    return sl


def color_negative_red(val):
    color = 'red' if val < 0 else 'black'
    return 'color:%s' % color


# 定义groupby之后的列名
sparkline_str.__name__ = "分布图"


def highlight_max(s):
    is_max = s == s.max()
    return ['background-color:yellow' if v else '' for v in is_max]


### exp.25 个常用 Matplotlib 图的 Python 代码
large = 22
med = 16
small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
# plt.style.use('seaborn-whitegrid')  #影响汉字显示
# sns.set_style("white")              #影响汉字显示
# % matplotlib inline
#
# Version
print(mpl.__version__)  # > 3.2.1
print(sns.__version__)  # >0.10.1

# dataset = load_iris()
# x = dataset.data
# y = dataset.target
# print(dataset.DESCR)
print(mpl.matplotlib_fname())  # 找到自己Matplotlib安装目录
x = np.linspace(0.05, 10, 1000)
y = np.cos(x)

plt.plot(x, y, ls='--', lw=2, label='plot figure-中文测试')  # 英文：plot figure-
plt.title('为图表加入\n图例、标题与标签')
plt.xlabel('x轴')
plt.ylabel('y轴')

plt.legend()  # 显示默认图例

plt.show()
