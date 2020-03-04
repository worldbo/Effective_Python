# Helper_Function,Python3只有bytes和str
# 编写接受str和bytes，返回str的方法

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        # Python3的isinstance() 函数是Python3内置函数，isinstance()函数
        # 来判断一个对象是否是一个已知的类型,类似 type()
        value = bytes_or_str.decode('utf-8')  # 二进制转换Unicode，使用decode方法。
    else:
        value = bytes_or_str
    return value  # Instance of str


# 编写接受str和bytes，总返回bytes的方法。
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')  # Unicode字符转换成二进制数，必须使用encode方法
    else:
        value = bytes_or_str
    return value  # Instance of bytes


# 用辅助函数取代复杂的表达式
from urllib.parse import parse_qs

my_valuse = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
print(repr(my_valuse))
print('Red:', my_valuse.get('red'))
print('Green:', my_valuse.get('green'))
print('Opacity:', my_valuse.get('opacity'))

# For query string 'red=5&blue=0&green='
red = my_valuse.get('red', [''])[0] or 0
green = my_valuse.get('green', [''])[0] or 0
opacity = my_valuse.get('opacity', [''])[0] or 0
print('Red:    %r' % red)
print('Green:  %r' % green)
print('Opacity:%r' % opacity)


# 上述写法不易读，应改成if/else形式，并写成辅助函数。
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found


# page10
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('First four:', a[:4])
print('Last four:', a[-4:])
print('Middle tow:', a[3:-3])
print('First four:', a[1:4])
first_twenty_items = a[:20]
last_twenty_items = a[-20:]

# page13
a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = a[::2]  # 取奇数
evens = a[1::2]  # 取偶数
print(odds)
print(evens)
x = b'mongoose'
y = x[::-1]
print(y)

w = '您好'
y = w[::-1]
print(y)
# x = w.encode('utf-8')
# y = x[::-1]
# z = y.decode('utf-8')

# page15
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x ** 2 for x in a]
print(squares)

even_squares = [x ** 2 for x in a if x % 2 == 0]
print(even_squares)

alt = map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)  # assert断言语句

chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}
chile_len_set = {len(name) for name in rank_dict.values()}
print(rank_dict)
print(chile_len_set)

#page16
matrix = [[1,2,3],[4,5,6],[7,8,9]]
flat = [x**2 for row in matrix for x in row]# from left(or row in matrix)to right(for x in row).
print(flat)

#page16
squared = [[x**2 for x in row] for row in matrix]
print(squared)

my_lists = [
    [[1,2,3],[4,5,6]],
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]
print(flat)

flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
print(flat)

a = [1,2,3,4,5,6,7,8,9,10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]
assert c == b  # assert断言语句
print(b)

#page17(尽量不要用这种方式)
matrix = [[1,2,3],[4,5,6],[7,8,9]]
filtered = [[x for x in row if x % 3 ==0]
            for row in matrix if sum(row) >= 10]
print(filtered)

