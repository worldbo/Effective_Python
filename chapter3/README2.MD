#第三章 类与继承

#第二十二条：尽量用辅助类来维护程序状态，而不要用字典和元组。
1、不要使用包含其他字典的字典，也不要使用过长的元组。
2、利用collections模块中的namedtuple（具名元组）类型，解决元组元素超出2项的问题。
3、实际应用中如处理数据，最好还是用数据库，写类很繁琐的。
4、如果容器中包含简单而又不可变的数据，优先用具名元组。
5、保存内部状态的字典如果变的复杂，应把其拆分为多个辅助类。
6、定义一个实例，其他辅助类依赖这个实例，这样逐层引用解决问题。


#第二十三条：简单的接口应该接受函数，而不是类的实例
1、