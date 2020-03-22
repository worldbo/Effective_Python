# page44 第十九条

def remainder(number, divisor):
    return number % divisor


assert remainder(20, 7) == 6
assert remainder(20, 7) == remainder(20, divisor=7) == remainder(number=20, divisor=7) == remainder(divisor=7,
                                                                                                    number=20)


# remainder(number=20, 7) #位置参数在关键字参数之后，出错！！！
# remainder(20, number=7) #每个参数只能指定一次

# page45

def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff


weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print('%.3f kg per second' % flow)


# 增加估算流率
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period


flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
print('%.3f kg per second' % flow_per_second)
print('%.3f kg per hour' % flow_per_hour)

#可以扩充函数参数

def flow_rate(weight_diff, time_diff, period=1,units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period

pounds_per_hour = flow_rate(weight_diff, time_diff,
                          period=3600,units_per_kg=2.2)
print('%.3f kg per second' % pounds_per_hour)