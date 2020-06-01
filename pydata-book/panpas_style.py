import numpy as np
import pandas as pd
from sparklines import sparklines


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


pd.set_option('expand_frame_repr', False)  # True换行显示, False不允许换行
pd.set_option("display.max_columns", None)  # dataFrame的列, None显示完整的列, 数字表示显示最大列数
pd.set_option('display.max_rows', None)  # None显示完整的行, 数字表示显示最大行数
pd.set_option("display.width", 200)  # 横向最多显示多少个字符
pd.set_option("display.max_colwidth", 100)  # 列长度
pd.set_option('colheader_justify', 'left')  # 显示居中还是左边
pd.set_option('precision', 5)  # 显示小数点后的位数
pd.set_option('chop_threshold', 0.5)  # 绝对值小于0.5的显示0.0

# 列名对齐参数

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

np.random.seed(24)
df = pd.DataFrame({'A': np.linspace(1, 10, 10)})
df = pd.concat([df, pd.DataFrame(np.random.randn(10, 4), columns=list('BCDE'))],
               axis=1)
df.iloc[0, 2] = np.nan
s = df.style.applymap(color_negative_red)
print(df)
df.style.apply(highlight_max)
df.style.applymap(color_negative_red).apply(highlight_max)  # 对元素级别的操作  #对行或者column进行计算（聚合）
df.groupby('D')[['B', 'E']].agg(['mean', sparkline_str])
print(df.groupby('D')[['B', 'E', 'A']].agg(['mean', sparkline_str]))
