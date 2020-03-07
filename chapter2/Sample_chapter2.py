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

#page30
def sort_priority(values,group):
    def helper(x): #闭包函数,x是numbers中各个元素
        if x in group:
            return (0,x)
        return (1,x)
    values.sort(key=helper)#闭包函数传给key参数

numbers = [8,3,1,2,5,4,7,6]
group = {2,3,5,7}
sort_priority(numbers,group)
print(numbers)


def sort_priority2(numbers,group):
    found = False#Scope：'sort_priority2_
    def helper(x):
        if x in group:
            found = True #seem simple#Scope：'helper'-----Bad!
            return (0,x)
        return (1,x)
    numbers.sort(key=helper)
    return found

found = sort_priority2(numbers,group)
print('Found:',found)
print(numbers)


#page33
def sort_priority3(numbers,group):
    found = False#Scope：'sort_priority2_
    def helper(x):
        nonlocal found
        if x in group:
            found = True #seem simple#Scope：'helper'-----Bad!
            return (0,x)
        return (1,x)
    numbers.sort(key=helper)
    return found

#page34
class Sorter(object):
    def __init__(self,group):
        self.group = group
        self.found = False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0,x)
        return (1,x)


sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True
