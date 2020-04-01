# page47
import os
import datetime
import time
import json


def log(message, when=datetime.datetime.now()):  # 用datetime的中的方法，原文有错，印成datetime.now()！！！
    print('%s:%s' % (when, message))


log('Hi there!')
time.sleep(12)
log('Hi again!!')
print("两个值相同，错误！！！判断函数只调用一次")


##
def log1(message, when=None):
    """Log a messge with a timestamo

    Args:
        message:Message to print
        when:datatime of when the message occurred
            Defaults to the present time."""

    when = datetime.datetime.now() if when is None else when  # 用datetime的中的方法，原文有错，印成datetime.now()！！！
    print('%s:%s' % (when, message))


log1('Hi there!')
time.sleep(12)
log1('Hi again!!')


# page48
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
print("两个值相同，错误！！！判断函数只调用一次")


def decode1(data, default=None):
    """Log Json data from a string

       Args:
           data:Json data to decode
           default:Value to return if decoding fails.
               Defaults to an empty dictionary."""

    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode1('bad data')
foo['stuff'] = 5
bar = decode1('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
