This is a demo programs. data:2020-03-02
Version 1.0
#第一条：确认版本号
#improt sys
#print(sys.version_info)
#pring(sys.version)

#第二条：遵循PEP8风格
#《Python Enhancement Proposal #8》（8号Python增强提案）PEP8。
一、空白（whitespace）：
1、使用space（空格）来表示缩进，不要用Tab（制表符）
2、和语法相关的每一层缩进都用4个空格表示。
3、每行字符不超过79个
4、对于占据多行的长表达式，除首行外，其余各行都应该在通常的缩进级别上在加4个空格。
5、同一个类中，各方法之间应用两个空行隔开。
6、在使用下标来获取列表元素、调用函数或给关键参数赋值时，不要在两旁加空格。
7、为变量赋值时，赋值符号的左侧和右侧应该各自写上一个空格，而且只写一个就好。

二、命名：
1、函数、变量以及属性应该用小写字母来拼写，各单词之间以下划线相连接，例如：lowercase_underscore
2、受保护的实例属性，应该以单个下划线开头，例如：_leading_underscore
3、私有的实例属性，应该以两个下划线开头，例如：__double_leading_underscore
4、类与异常，应该以每个单词首字母均应大写的形式来命名，例如：CapitalizedWord
5、模块级别的常量，应该全部采用大写字母来拼写，各单词之间以下划线相连，例如：ALL_CAPS
6、类中的实例方法（instance method）,应该把首个参数命名为self，以表示该对象自身。
7、类方法（class method）的首个参数，应该命名为cls，以表示该类的自身。

三、表达式和语句：
1、采用内联形式的否定词，而不要把否定词放在整个表达式的前面，
   例如，应该写“if a is not b”而不是“if no a is b”
2、不要通过检测长度的方法（如 if len(somelist) == 0）来判断somelist 
   是否为[]或''等空值，而应采用“if not somlist”这种写法来判定。空值自动Flase
3、检测somelist是否为[1]或'hi'等非空值时，也应如上。空值自动True。
4、不要编写单行的if语句、for循环、while循环以及except复合语句，应分成多行，以示清晰。
5、import语句应该总放在文件开头处。
6、引入模块时，总应使用绝对名称，而不应根据当前模块的路径来使用相对名称。例如：引入
   bar包中的foo模块时，应该完整的写出“from bar import foo”而不应简写成“import foo”
7、如果一定要使用相对名称来编写import语句，应采用明确的“from.import foo”
8、文件中的import语句应按顺序分成三个部分，分别表示标准库模块、第三方模块以及自用模块。
   在每个部分中，各import语句应按模块字母顺序排列。
9、当编写Python代码时，总应遵循pep8风格指南。

#第三条：bytes、Unicode与Unicode区别（Python3只有bytes和str）
1、bytes的实例包含原始的8位值（就是原始字节，每个字节有8个二进制位）
   str的实例包含Unicode字符。
2、str的Unicode字符转换成二进制数，必须使用encode方法；二进制转换Unicode，使用decode方法。
3、编写Python时，必须把编解码操作放到界面最外面；程序核心部分必须使用Unicode字符类型。
4、输出文本信息只采用UTF-8编码形式。
5、如果通过内置的open函数获取文件的句柄，该句柄默认会采用UTF-8编码格式来操作文件。
   如向文件中写二进制数必须采用二进制的写入模式（'wb'）来开启操作的文件。
   即：open（'xx.bin','wb'）,不能采用字符写入模式'w';读文件用'rb',不能用'r'.
   否则会产生：TypeError：must be str,no bytes.


#第四条：用辅助函数取代复杂的表达式


#第五条：切割序列的方法（page10）
1、切割的基本写法是：somelist[start:end],其中start（起始索引）所指的元素包含在切割后的
   范围内（切割后序列中有它），end（结束索引）所指的元素不包含在求切割后结果内（没有它）。
2、切割列表时，即便start或end索引越界也不会出错。但访问单个列表时，下标不能越界。
3、切割后，不会改变原列表。
4、如对左侧的切割的列表进行赋值操作，则该原列表的对应制定的对象元素会改变成相应的赋值。
   该赋值的个数不一定与分割的数相同，其会根据新的个数适当的扩张或收缩。切割范围前后值不变。

#第六条：单次切片操作，不要同时指定start、end和stride
1、除基本切割操作外，Python提供了somelist[start:end:stride]形式写法，实现步进切割。
2、stride值为-1时，对字符串和ASCII字符可以反转过来，但对已经编码的UTF-8的Unicode无效。
3、不要把start、end和stride写一起，并且stride尽量用正值，同时省略tart、end值。
4、如一定要配合tart、end的化，可先赋值给一个变量后再进行二次切割。
5、如时间或内存要求严格，就用内置的itertools模块中的islide方法，其不允许负值。


#第七条：用列表推导取代map和filter（page15）
1、一种Python精炼的写法：根据一份列表制作另一份的表达式-list comprehensio（列表推导）
2、例如：x**2 for x in a 其比map函数更清晰。
3、如用map需要lambda函数，如x = map（lambda x:x**2，a）
4、如有过滤条件，直接在循环后加条件表达式即可。
   例如：x**2 for x in a if x % 2 == 0
5、如用flite函数与map结合，就比较麻烦。
   例如：alt = map(lambda x: x**2,filter(lambda x: x % 2 == 0, a))
6、字典（dict）与集（set），也有和列表类似的推导机制。



