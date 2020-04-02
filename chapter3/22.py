# page53
class SimpleGragebook(object):
    def __init__(self):
        self.__grades = {}

    def add_student(self, name):
        self.__grades[name] = []    # 一个学生对应一个成绩列表

    def report_grade(self, name, score):
        self.__grades[name].append(score)

    def average_grade(self, name):
        grades = self.__grades[name]
        return sum(grades) / len(grades)    ## 计算一个学生的平均成绩

    def sum_grade(self, name):
        grades = self.__grades[name]
        return sum(grades)    ## 计算一个学生的总成绩


book = SimpleGragebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)
book.add_student('ss')
book.report_grade('ss', 90)
book.report_grade('ss', 100)
book.report_grade('ss', 100)
book.add_student('aa')
book.report_grade('aa', 70)
book.report_grade('aa', 67)
# ...
print(book.average_grade('Isaac Newton'))
print(book.sum_grade('Isaac Newton'))
print(book.average_grade('ss'))
print(book.sum_grade('ss'))
print(book.average_grade('aa'))
print(book.sum_grade('aa'))
print(book._SimpleGragebook__grades)

##page55 增加科目需求

class SimpleGradebook():
    def __init__(self):
        self.__grades = {}

    def add_student(self, name):
        self.__grades[name] = {}    # 一个学生的成绩加入科目分类，所以用字典存储

    def report_grade(self, name, subject, score):
        by_subject = self.__grades[name]
        grade_list = by_subject.setdefault(subject, [])     # 存在该科目则返回已有列表，不存在则返回一个空列表
        grade_list.append(score)

    def average_grade(self, name):
        by_subject = self.__grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count


book = SimpleGradebook()
book.add_student('ss')
book.report_grade('ss', 'Math', 90)
book.report_grade('ss', 'Math', 100)
print(book.average_grade('ss'))


###page56 增加考试权重
from collections import namedtuple, defaultdict

Grade = namedtuple('Grade', ('score', 'weight'))    # 具名元组


class Subject:
    # 科目的类，包含成绩和权重
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    # 学生的类，包含各项课程
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class Gradebook:
    # 所有学生成绩的容器类，以学生的名字为键
    def __init__(self):
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]


book = Gradebook()
# albert = book.get_student('ss')
# math = albert.get_subject('Math')
# math.report_grade(75, 0.05)
# math.report_grade(65, 0.15)
# math.report_grade(70, 0.80)
# gym = albert.get_subject('Gym')
# gym.report_grade(100, 0.40)
# gym.report_grade(85, 0.60)
albert = book.get_student('Albert Einstein')
math = albert.get_subject('Math')
math.report_grade(80, 0.10)
print(albert.average_grade())


