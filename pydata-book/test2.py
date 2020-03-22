import pandas as pd
import numpy as np
from openpyxl import load_workbook

writer = pd.ExcelWriter('F:/1/123.xlsx')
book = load_workbook('F:/1/123.xlsx')
writer.book = book
data3 = pd.DataFrame(np.random.randn(10, 5))
data3.to_excel(writer, sheet_name='345')
writer.save()
