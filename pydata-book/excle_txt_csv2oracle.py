#使用python批量导入csv、excel、txt格式文件到oracle数据库（python3x）
#1、相对较小的文件，使用python open该文件，再逐条取出数据，导入到数据库，简单粗暴，以这三种格式的文件举几个超简单的例子：

#e.g.1 excel2oracle
# -*- coding: utf-8 -*-
import cx_Oracle
import xlrd


conn = cx_Oracle.connect('scott/tiger@localhost:1521/ORCL')     #('xxx/xxx@ip/orcl')
cursor=conn.cursor()
file_name="商超.xlsx"
insert_line=0
workbook = xlrd.open_workbook(file_name)
booksheet = workbook.sheet_by_index(0)
nrows = booksheet.nrows #行数
ncols = booksheet.ncols #列数
for i in range(0,nrows):
    row_data = booksheet.row_values(i)
    #print(row_data)
    if row_data:
        sql_insert="insert into id_shangchao values ('%s')"%row_data[0].strip()
        cursor.execute(sql_insert)
        insert_line+=1
conn.commit()
cursor.close()
conn.close()
print(insert_line)


#e.g.2 csv2oracle

# -*- coding: utf-8 -*-
import cx_Oracle
import csv
conn = cx_Oracle.connect('')
cursor=conn.cursor()
file_name="TOP商户id.csv"
insert_line=0
#, encoding='gbk'
f=open(file_name)
csv_reader = csv.reader(f)
for row_data in csv_reader:
    if row_data:
        value=tuple(row_data)
        #print(value[0])
        sql_insert="insert into id_TOP_OB values ('%s','%s')"%(value[0].strip(),value[1].strip())
        cursor.execute(sql_insert)
        insert_line+=1
f.close()
conn.commit()
cursor.close()
conn.close()
print(insert_line)

#e.g.txt2oracle
# -*- coding: utf-8 -*-
#CREATE TABLE DR_TEMP2018081000 (ob_id char(15));
import cx_Oracle
conn = cx_Oracle.connect('')
mcursor = conn.cursor()
file_name="OB_CODE.txt"
insert_line=0
f=open(file_name,encoding='utf-8')
for row_data in f.readlines():
    account=row_data.strip()
    #print(account)
    if row_data:
        sqlexe="insert into DR_TEMP2018073104 values('%s')"%account
        mcursor.execute(sqlexe)
        insert_line+=1
f.close()
conn.commit()
mcursor.close()
conn.close()
print(insert_line)


###2、当单个文件很大的时候，再调用open，对系统可能内存占用可能就很大，或者压根打不开，
# 这个时候可以使用oracle的sqlldr命令，使用oracle服务器的功能，把数据以极快的速度导入到
# 数据库中，速度比1中简单粗暴的办法快了上百倍！！！
#不过要注意
# 1、sqlldr导入的文件必须以.dat为后缀，并且需要控制文件来说明导入文件的格式，
# 2、SQLLDR是一个命令工具，并非一个API，不能从PL/SQL调用。
# sqlldr特点：
# 可以从不同文件类型的多个输入数据文件中加载数据；
# 输入记录可以是定长的或变长的记录；
# 可以在同一次运行中加载多个表，还可以逻辑地将选定的记录载入到每个表中；
# 在输入数据载入表之前，可以对其使用SQL函数；
# 多个物理记录可以被编译成一个逻辑记录，同样，SQL可以提取一条物理记录并把它作为多个逻辑记录加载；
# 支持嵌套、嵌套表、VARRAYS和LOBS（包括BLOGCLOBNLOBBFILE）。

#e.g.sqlldr
table_name=table_list[i//10]
  #CHARACTERSET ZHS16GBK
  #edit ctl files according to table_name
  lines=open(contol_file,'r').readlines()
  for k in range(len(lines)):
      if 'INTO TABLE' in lines[k]:
          lines[k]='INTO TABLE %s\n'%table_name
  f=open(contol_file,'w')
  f.writelines(lines)
  f.close()

  newname=file_name+".dat"
  try:
      os.remove(newname)
  except:
      pass

  os.rename(file_name,newname)

#import
cmd_str="sqlldr cups_user/Hb20021209@172.16.121.190/orcl control=%s data=%s "%(contol_file,newname)
cmd_str+=" bad=%s\\bad_files\\%s.bad log=%s\\log_files\\%s.log direct=true"%(basedir,file_name,basedir,file_name)
#print(cmd_str)
os.system(cmd_str)
