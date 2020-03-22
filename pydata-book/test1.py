import pandas as pd
import numpy as np

writer = pd.ExcelWriter('F:/1/123.xlsx')
data1 = pd.DataFrame(np.arange(12).reshape((3, 4)))
print(data1)
data1.to_excel(writer,  sheet_name='123')

data2 = pd.DataFrame(np.random.randn(6, 6))
print(data2)
data2.to_excel(writer, sheet_name='234')
writer.save()
