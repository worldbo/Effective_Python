# coding=utf-8
# 文件功能：弹出式闹钟，没有控制台，没有装饰，响应时间为30S
# 导入包
import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# 创建QApplication对象，每个PyQtGui程序必须有一个QApplication对象，该对象提供访问全局信息的能力。
app = QApplication(sys.argv)  # 传递命令行参数
try:
    due = QTime.currentTime()  # due变量设置为现在的时间点，并给出一个默认消息：Alert！
    message = "Alert!"
    if len(sys.argv) < 2:
        raise ValueError  # 如果用户没有给定命令行参数值，就会raise一个ValueError异常。
    '''
    如果第一个参数不含冒号，那么在尝试调用split()将两个元素解包时，就将触发一个ValueError异常。
    如果小时数和分钟数不是有效数字，那么int()将会触发一个ValueError异常；
    如果小时数和分钟数超限，导致成无效的QTime，那么需要自己来触发一个ValueError异常。
    '''
    hours, mins = sys.argv[1].split(":")
    due = QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
    '''如果该time有效，那么就把这条消息与其他命令行参数用空格分隔开；如果没有其他参数，就用开头设置的默认信息“Alert”来代替之'''
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
except ValueError:
    message = "Usage:alert.pyw HH:MM [optional message]"  # 24hr clock
    while QTime.currentTime() < due:
        time.sleep(20)  # 20seconds

label = QLabel("<font color=red size=72><b>" + message + "</b></font>")
label.setWindowFlags(Qt.SplashScreen)
label.show()
QTimer.singleShot(30000, app.quit)
app.exec_()

