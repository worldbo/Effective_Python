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
cursor1 = conn.cursor()

# 使用execute方法执行SQL语句
result = cursor.execute('select * from DEPT t')
result1 = cursor1.execute('select * from EMP t')

# 使用fetchone()方法获取一条数据
# data=cursor.fetchone()


# 获取所有数据
all_data = cursor.fetchall()
all_data1 = cursor1.fetchall()
print(all_data)
print(all_data1)
# 获取部分数据，8条
# many_data=cursor.fetchmany(8)

# 关闭光标与数据库
cursor.close()
cursor1.close()
db.close()
