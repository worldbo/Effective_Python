# page41 定义log函数，把调试信息打印出来

def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print('%s: %s ' % (message, values_str))


log('My numbers are', [1, 2, 3, 4, 5, 6])
log('Hi there', [])


# 上述例子log('Hi there', [])第二个参数因其必须传入，存在视觉杂讯，改造之

def log(message, *values):  # The only different
    if not values:
        print(message)
    else:
        values_str = ','.join(str(x) for x in values)
        print('%s: %s ' % (message, values_str))


log('My numbers are', [4, 5, 6])
log('Hi there')

favorites = [7, 33, 99]
log('Favorite colors', *favorites)


# page42 传递为元组，再迭代，易崩溃。
def my_generator():
    for i in range(10):
        yield i


def my_func(*args):
    print(args)


it = my_generator()
my_func(*it)


# page43 调用变长参数第二产生问题
def log(sequence, message, *values):  # The only different
    if not values:
        print('%s: %s ' % (sequence, message))
    else:
        values_str = ','.join(str(x) for x in values)
        print('%s: %s: %s ' % (sequence, message, values_str))


log(1, 'Favorites', 7, 33)  # New usage is OK
log('Favorites numbers', 7, 33)  # Old usage breaks


