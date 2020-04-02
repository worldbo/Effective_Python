# python操作oracle完整教程
import cx_Oracle

# 连接数据库，下面括号里内容根据自己实际情况填写
# conn = cx_Oracle.connect('用户名/密码@IP:端口号/SERVICE_NAME')
db = cx_Oracle.connect('scott', 'tiger', 'localhost:1521/ORCL')
db1 = cx_Oracle.connect('scott/tiger@localhost:1521/ORCL')
dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'ORCL')
print(dsn_tns)
print(db.version)  # python操作oracle完整教程
import cx_Oracle

# 连接数据库，下面括号里内容根据自己实际情况填写
# conn = cx_Oracle.connect('用户名/密码@IP:端口号/SERVICE_NAME')
conn = cx_Oracle.connect('scott', 'tiger', 'localhost:1521/ORCL')
conn1 = cx_Oracle.connect('scott/tiger@localhost:1521/ORCL')
dsn_tns = cx_Oracle.makedsn('localhost', 1521, 'ORCL')
print(dsn_tns)
print(db.version)

# 使用cursor()方法获取操作游标
cursor = conn.cursor()
# cursor1 = conn.cursor()
# cursor2 = conn.cursor()

# 使用execute方法执行SQL语句
# cx_Oracle.Cursor.executemany(statement,parameters)

# 特别有用的批量插入，避免一次只能插入一条；
# result = cursor.execute('select * from DEPT t')
# result1 = cursor1.execute('select * from EMP t')

# 绑定变量查询可以提高效率，避免不必要的编译；参数可以是名称参数或位置参数，尽量使用名称绑定。
# named_params = {'dept_id': 30, 'sal': 1000}
# query1 = cursor.execute('SELECT * FROM  EMP WHERE deptno=:dept_id AND SAl>:sal', named_params)
# query2 = cursor.execute('SELECT * FROM employees WHERE department_id=:dept_id AND salary>:sal', dept_id=50, sal=1000)

# 使用fetchone()方法获取一条数据
# data=cursor.fetchone()

# query1 = cursor.execute("SELECT * FROM  SP2CC  WHERE 变更前流水号 = '2190117986126'")
query1 = cursor.execute("select distinct b.kcmc from "
                        "(select a.kssb,a.kcmc from "
                        "(select DISTINCT t.kssb,kcmc,ksrq from "
                        "KSXTSJYC t where t.kssb like '%SL%')a "
                        "where a.kssb like '%qx%' or  a.kssb like '%QX%' "
                        "order by a.kcmc desc)b")
# 获取所有数据
all_data = cursor.fetchall()
# all_data1 = cursor1.fetchall()
# all_data2 = cursor2.fetchall()
print(all_data)
# print(all_data1)
# 获取部分数据，8条
# many_data=cursor.fetchmany(8)

# 关闭光标与数据库
cursor.close()
# cursor1.close()
db.close()
