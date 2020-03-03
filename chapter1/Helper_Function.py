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

#page10
a = ['a','b','c','d','e','f','g','h']
print('First four:',a[:4])
print('Last four:',a[-4:])
print('Middle tow:',a[3:-3])
print('First four:',a[1:4])
first_twenty_items = a[:20]
last_twenty_items = a[-20:]
