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
