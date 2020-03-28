# page28

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


x, y = 0, 5
result = divide(x, y)
if result is None:
    print('Invalid inputs')  # This is wrong!


def divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


success, result = divide(x, y)
if not success:
    print('Invalid inputs')


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e


x, y = 5, 2
try:

    result = divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    # print('Result is {result}'.format(result=result)) #如果是元组的化！！！
    print('Result is %.1f' % result)


# page30
def sort_priority(values, group):
    def helper(x):  # 闭包函数,x是numbers中各个元素
        if x in group:
            return (0, x)
        return (1, x)

    values.sort(key=helper)  # 闭包函数传给key参数


numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)


def sort_priority2(numbers, group):
    found = False  # Scope：'sort_priority2_

    def helper(x):
        if x in group:
            found = True  # seem simple#Scope：'helper'-----Bad!
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found


found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)


# page33
def sort_priority3(numbers, group):
    found = False  # Scope：'sort_priority2_

    def helper(x):
        nonlocal found
        if x in group:
            found = True  # seem simple#Scope：'helper'-----Bad!
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found


# page34
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)


sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True


# page35
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':  #
            result.append(index + 1)
    return result


address = 'Four score and seven years age .....'
result = index_words(address)
print(result[:3])


# page36 采用生成器
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':  #
            yield index + 1


address = 'Four score and seven years age .....'
result = list(index_words_iter(address))
print(result[:3])

# page36-2
from itertools import islice


def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


with open('F:/python/Effective_Python/chapter2/2.txt') as f:
    it = index_file(f)
    results = islice(it, 0, 3)  # slice() 函数实现切片对象，主要用在切片操作函数里的参数传递。
    print(list(results))


# page37
def normalize(numbers):  # 标准化函数
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)


def fun():
    li = [15, 35, 80]
    for i in li:
        yield i


print(normalize(fun()))


# files 方式 生成器
# def read_visits(data_path):
#     with open(data_path) as f:
#         for line in f:
#             yield int(line)


# it = read_visits('F:/python/Effective_Python/chapter2/2.txt')
# print((list))
# percentages = normalize(it)
# print(percentages)  # Already exhaustes

# page38
# def normalize_copy(numbers):
#     numbers = list(numbers)  # Copy the iterator
#     total = sum(numbers)
#     result = []
#     for value in numbers:
#         percent = 100 * value / total
#         result.append(percent)
#     return result


# it = read_visits('F:/python/Effective_Python/chapter2/2.txt')
# print(it)
# percentages = normalize_copy(it)
# print(list(it))  # Already exhaustes


class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


path = 'F:/python/Effective_Python/chapter2/2.txt'
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)


