# 首先导入PyMySQL库
#import pymysql

# 连接数据库，创建连接对象connection
# 连接对象作用是：连接数据库、发送数据库信息、处理回滚操作（查询中断时，数据库回到最初状态）、创建新的光标对象
# connection = pymysql.connect(host = 'localhost' #host属性
# user = 'root' #用户名
# password = '******'  #此处填登录数据库的密码
# db = 'mysql' #数据库名
# )

# 创建光标对象，一个连接可以有很多光标，一个光标跟踪一种数据状态。
# 光标对象作用是：、创建、删除、写入、查询等等
# cur = connection.cursor()
# 查看有哪些数据库，通过cur.fetchall()获取查询所有结果
#cur.execute('SHOW DATABASES') 执行sql语句
# print(cur.fetchall())

# 在test数据库里创建表:
# 使用数据库test
# cur.execute('USE test')
# 在test数据库里创建表student，有name列和age列
# cur.execute('CREATE TABLE student(name VARCHAR(20),age TINYINT(3))')
#
# sql = 'INSERT INTO student (name,age) VALUES (%s,%s)'
# cur.execute(sql,('XiaoMing',23))

# 向数据表student中插入一条数据：
# sql = 'INSERT INTO student (name,age) VALUES (%s,%s)'
# cur.execute(sql,('XiaoMing',23))

# 查看数据表student内容：
# cur.execute('SELECT * FROM student')
# print(cur.fetchone())

# 要记得关闭光标和连接：

# 关闭连接对象，否则会导致连接泄漏，消耗数据库资源
# connection.close()
# 关闭光标
# cur.close()


#LOAD DATA LOCAL INFILE 'csv_file_path' INTO TABLE table_name FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES
# csv_file_path 指文件绝对路径
# table_name指表名称
# FIELDS TERMINATED BY ','指以逗号分隔
# LINES TERMINATED BY '\\r\\n'指换行
# IGNORE 1 LINES指跳过第一行，因为第一行是表的字段名


# 导入pymysql方法
import pymysql

# 连接数据库
config = {'host': 'localhost',
          'port': 3306,
          'user': 'root',
          'passwd': 'world_bo',
          'charset': 'utf8mb4',
          'local_infile': 1
          }
conn = pymysql.connect(**config)
cur = conn.cursor()


# load_csv函数，参数分别为csv文件路径，表名称，数据库名称
def load_csv(csv_file_path, table_name, database='evdata'):
    # 打开csv文件
    file = open(csv_file_path, 'r', encoding='utf-8')
    # 读取csv文件第一行字段名，创建表
    reader = file.readline()
    b = reader.split(',')
    colum = ''
    for a in b:
        colum = colum + a + ' varchar(255),'
    colum = colum[:-1]
    # 编写sql，create_sql负责创建表，data_sql负责导入数据
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'
    data_sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES" % (
        csv_filename, table_name)

    # 使用数据库
    cur.execute('use %s' % database)
    # 设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 执行create_sql，创建表
    cur.execute(create_sql)
    # 执行data_sql，导入数据
    cur.execute(data_sql)
    conn.commit()
    # 关闭连接
    conn.close()
    cur.close()
