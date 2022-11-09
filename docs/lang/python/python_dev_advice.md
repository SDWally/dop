# 改善 Python 程序的 91 个建议之务必版

引用自heavysheep 博客素材，由Wally删减

第 1 章 引论
建议 1：理解 Pythonic 概念
Pythonic 
当你输入 import this 就会显示 zen of python

美丽胜于丑陋。 
显式优于隐式。 
简单比复杂好。 
复合胜于复杂。 
平面比嵌套好。 
稀疏比密集好。 
可读性是重要的。 
特殊情况不足以打破规则。 
虽然实用性胜过纯粹。 
除了显示错误，错误永远不应该沉默。

代码风格 
充分体现python动态语言的特色，类似于

# 变量交换
a, b = b, a
# 上下文管理
with open(path, 'r') as f:
    do_sth_with(f)
# 不应当过分地追求奇技淫巧
a = [1, 2, 3, 4]
a[::-1] # 不推荐。好吧，自从学了切片我一直用的这个
list(reversed(a))   # 推荐
然后表扬了 Flask 框架，提到了 generator 之类的特性尤为 Pythonic，有个包和模块的约束： 
* 包和模块的命名采用小写、单数形式，而且短小 
* 包通常仅作为命名空间，如只含空的init.py文件

建议 2：编写 Pythonic 代码
避免劣化代码

避免只用大小写区分不同的对象
避免使用容易引起混淆的名称
不要害怕过长的变量名
深入认识python有助于编写pythonic代码

全面掌握 python 提供的特性，包括语言和库
随着时间推移，要不断更新知识
深入学习业界公认的 pythonic 代码
编写符合 pep8 的代码规范（就是让你使用pycharm）
建议 3：理解 Python 与 C 语言的不同之处
Python 使用代码缩进的方式来分割代码块，不要混用 Tab 键和空格
Python 中单、双引号的效果相同（个人建议使用单引号，在面对其他语言的双引号源码时不必再转义）
三元操作符：x if bool else y（原因是作者认为应该用可读性更好的方式表达）
用其他方法替代 switch-case
建议 4：在代码中适当添加注释
块和行注释仅仅注释复杂的操作、算法等
注释和代码隔开一段距离
给外部可访问的函数和方法添加文档注释
推荐在文件头中包含 copyright 申明、模块描述等
另外，编写代码应该朝代码即文档的方向进行，但仍应该注重注释的使用

建议 5：通过适当添加空行使代码布局更为优雅、合理
表达完一个完整思路后，应该用空白行间隔，尽量不要在一段代码中说明几件事。
尽量保持上下文的易理解性，比如调用者在上，被调用者在下
避免过长的代码行，超过80个字符应该使用行连接换行（还是让你使用pycharm）
水平对齐毫无意义，不要用多余空格保持对齐
空格的使用要能够在需要使用时强调警示读者（符合PEP8规范）
建议 6：编写函数的 4 个原则
函数设计要尽量短小，嵌套层次不宜过深
函数申明应该做到合理、简单、易于使用
函数参数设计应该考虑向下兼容
一个函数只做一件事，尽量保证函数语句粒度的一致性
Python 中函数设计的好习惯还包括：不要在函数中定义可变对象作为默认值，使用异常替换返回错误，保证通过单元测试等。

# 关于函数设计的向下兼容
def readfile(filename):         # 第一版本
    pass
def readfile(filename, log):    # 第二版本
    pass
def readfile(filename, logger=logger.info):     # 合理的设计
    pass

建议 7：将常量集中到一个文件
在Python中应当如何使用常量：

常量名全部大写
将存放常量的文件命名为constant.py
示例为：

class _const:
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass
    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't change const.%s" % name
        if not name.isupper():
            raise self.ConstCaseError, \
                    'const name "%s" is not all uppercase' % name
        self.__dict__[name] = value
import sys
sys.modules[__name__] = _const()
import const
const.MY_CONSTANT = 1
const.MY_SECOND_CONSTANT = 2
const.MY_THIRD_CONSTANT = 'a'
const.MY_FORTH_CONSTANT = 'b'
其他模块中引用这些常量时，按照如下方式进行即可：

from constant import const
print(const.MY_CONSTANT)

第 2 章 编程惯用法
建议 8：利用 assert 语句来发现问题
断言的判断会对性能有所影响，因此要分清断言的使用场合：

断言应使用在正常逻辑无法到达的地方或总是为真的场合
python本身异常处理能解决的问题不需要用断言
不要使用断言检查用户输入，而使用条件判断
在函数调用后，当需要确认返回值是否合理时使用断言
当条件是业务的先决条件时可以使用断言
代码示例：

>>> y = 2
>>> assert x == y, "not equals"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError: not equals
>>> x = 1
>>> y = 2
# 以上代码相当于
>>> if __debug__ and not x == y:
...     raise AssertionError("not equals")
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
AssertionError: not equals
运行是加入-O参数可以禁用断言。

建议 9：数据交换的时候不推荐使用中间变量
>>> Timer('temp = x; x = y; y = temp;', 'x = 2; y = 3').timeit()
0.059251302998745814
>>> Timer('x, y = y, x', 'x = 2; y = 3').timeit()
0.05007316499904846
对于表达式x, y = y, x，在内存中执行的顺序如下： 
1. 先计算右边的表达式y, x，因此先在内存中创建元组(y, x)，其标识符和值分别为y, x及其对应的值，其中y和x是在初始化已经存在于内存中的对象 
2. 计算表达式左边的值并进行赋值，元组被依次分配给左边的标识符，通过解压缩，元组第一标识符y分配给左边第一个元素x，元组第二标识符x分配给左边第一个元素y，从而达到交换的目的

（简单来说，直接交换符合pythonic且性能最佳，这么做就对了）

建议 10：充分利用 Lazy evaluation 的特性
（就是生成器） 
Lazy evaluation常被译为延迟计算，体现在用 yield 替换 return 使函数成为生成器，好处主要有两方面：

避免不必要的计算，带来性能提升
节省空间，使无限循环的数据结构成为可能
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

建议 12：不推荐使用 type 来进行类型检查
使用 isinstance 来进行类型检查（注意上下包含关系就行）

建议 13：尽量转换为浮点类型后再做除法
py2.x:转换浮点类型后再做除法

建议 14：警惕 eval() 的安全漏洞
eval具有安全漏洞，建议使用安全性更好的ast.literal_eval。

建议 15：使用 enumerate() 获取序列迭代的索引和值
>>> li = ['a', 'b', 'c', 'd', 'e']
>>> for i, e in enumerate(li):
...     print('index: ', i, 'element: ', e)
... 
index:  0 element:  a
index:  1 element:  b
index:  2 element:  c
index:  3 element:  d
index:  4 element:  e
# enumerate(squence, start=0) 内部实现
def enumerate(squence, start=0):
    n = start
    for elem in sequence:
        yield n, elem   # 666
        n += 1
# 明白了原理我们自己也来实现一个反序的
def reversed_enumerate(squence):
    n = -1
    for elem in reversed(sequence):
        yield len(sequence) + n, elem
        n -= 1
（此方式相比从列表里放索引取值更加优雅）

建议 16：分清 == 与 is 的适用场景
比较有趣的：

>>> s1 = 'hello world'
>>> s2 = 'hello world'
>>> s1 == s2
True
>>> s1 is s2
False
>>> s1.__eq__(s2)
True
>>> a = 'Hi'
>>> b = 'Hi'
>>> a == b
True
>>> a is b
True
为了提高系统性能，对于较小的字符串会保留其值的一个副本，当创建新的字符串时直接指向该副本，所以a和b的 id 值是一样的，同样对于小整数[-5, 257)也是如此：

注意is不相当于 ==， is 是对 id 方法做的 == 。

建议 17：考虑兼容性，尽可能使用 Unicode
python2.x 这是无敌深坑，需要刻苦学习掌握（python3偶尔也会碰到这种问题，但避免了大多数这种可能）

建议 18：构建合理的包层次来管理 module
（__init__是对包的头文件定制） 
本质上每一个 Python 文件都是一个模块，使用模块可以增强代码的可维护性和可重用性，在较大的项目中，我们需要合理地组织项目层次来管理模块，这就是包(Package)的作用。

一句话说包：一个包含__init__.py 文件的目录。包中的模块可以通过.进行访问，即包名.模块名。那么这\个init.py文件有什么用呢？最明显的作用就是它区分了包和普通目录，在该文件中申明模块级别的 import 语句从而变成了包级别可见，另外在该文件中定义__all__变量，可以控制需要导入的子包或模块。

这里给出一个较为合理的包组织方式，是FlaskWeb 开发：基于Python的Web应用开发实战一书中推荐而来的：

|-flasky
    |-app/                      # Flask 程序
        |-templates/            # 存放模板
        |-static/               # 静态文件资源
        |-main/
            |-__init__.py
            |-errors.py         # 蓝本中的错误处理程序
            |-forms.py          # 表单对象
            |-views.py          # 蓝本中定义的程序路由
        |-__init__.py
        |-email.py              # 电子邮件支持
        |-models.py             # 数据库模型
    |-migrations/               # 数据库迁移脚本
    |-tests/                    # 单元测试
        |-__init__.py
        |-test*.py
    |-venv/                     # 虚拟环境
    |-requirements/
        |-dev.txt               # 开发过程中的依赖包
        |-prod.txt              # 生产过程中的依赖包
    |-config.py                 # 储存程序配置
    |-manage.py                 # 启动程序以及其他的程序任务
第 3 章：基础语法
建议 19：有节制地使用 from...import 语句
Python 提供三种方式来引入外部模块：import语句、from...import语句以及__import__函数，其中__import__函数显式地将模块的名称作为字符串传递并赋值给命名空间的变量。

使用import需要注意以下几点：

优先使用import a的形式
有节制地使用from a import A
尽量避免使用from a import *
为什么呢？我们来看看 Python 的 import 机制，Python 在初始化运行环境的时候会预先加载一批内建模块到内存中，同时将相关信息存放在sys.modules中，我们可以通过 sys.modules.items() 查看预加载的模块信息，当加载一个模块时，解释器实际上完成了如下动作：

在 sys.modules 中搜索该模块是否存在，如果存在就导入到当前局部命名空间，如果不存在就为其创建一个字典对象，插入到 sys.modules 中
加载前确认是否需要对模块对应的文件进行编译，如果需要则先进行编译
执行动态加载，在当前命名空间中执行编译后的字节码，并将其中所有的对象放入模块对应的字典中
>>> dir()
['__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__']
>>> import test
testing module import
>>> dir()
['__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'test']
>>> import sys
>>> 'test' in sys.modules.keys()
True
>>> id(test)
140367239464744
>>> id(sys.modules['test'])
140367239464744
>>> dir(test)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'b']
>>> sys.modules['test'].__dict__.keys()
dict_keys(['__file__', '__builtins__', '__doc__', '__loader__', '__package__', '__spec__', '__name__', 'b', 'a', '__cached__'])
从上可以看出，对于用户自定义的模块，import 机制会创建一个新的 module 将其加入当前的局部命名空间中，同时在 sys.modules 也加入该模块的信息，但本质上是在引用同一个对象，通过test.py所在的目录会多一个字节码文件。

（这节说的是，盲目使用from...import...会带来：

命名空间冲突
循环嵌套导入）
建议 20：优先使用 absolute import 来导入模块
（py3 中 relative import方法已被移除，不用操心）

建议 21： i+=1 不等于 ++i
++i 合法，但是无效

建议 22：使用 with 自动关闭资源
对于打开的资源我们记得关闭它，如文件、数据库连接等，Python 提供了一种简单优雅的解决方案：with。

with的实现得益于一个称为上下文管理器(context manager)的东西，它定义程序运行时需要建立的上下文，处理程序的进入和退出，实现了上下文管理协议，即对象中定义了enter()和exit()，任何实现了上下文协议的对象都可以称为一个上下文管理器：

enter()：返回运行时上下文相关的对象
exit(exception_type, exception_value, traceback)：退出运行时的上下文，处理异常、清理现场等
包含with语句的代码块执行过程如下：

>>> with open('test.txt', 'w') as f:
...     f.write('test')
... 
4
>>> f.__enter__
<built-in method __enter__ of _io.TextIOWrapper object at 0x7f1b967aaa68>
>>> f.__exit__
<built-in method __exit__ of _io.TextIOWrapper object at 0x7f1b967aaa68>
计算表达式的值，返回一个上下文管理器对象
加载上下文管理器对象的exit()以备后用
调用上下文管理器对象的enter()
将enter()的返回值赋给目标对象
执行代码块，正常结束调用exit()，其返回值直接忽略，如果发生异常，会调用exit()并将异常类型、值及 traceback 作为参数传递给exit()，exit()返回值为 false 异常将会重新抛出，返回值为 true 异常将被挂起，程序继续执行
Python 还提供 contextlib 模块，通过 Generator 实现，其中的 contextmanager 作为装饰器来提供一种针对函数级别上的上下文管理器，可以直接作用于函数/对象而不必关心enter()和exit()的实现。

推荐文章

建议 23：使用 else 子句简化循环（异常处理）
python 的 else 子句在循环正常结束和循环条件不成立时被执行，由 break 语句中断时不执行，同样，我们可以利用这颗语法糖作用在 while 和 try...except 中。

建议 24：遵循异常处理的几点基本原则
异常处理的几点原则： 
1. 注意异常的粒度，不推荐在 try 中放入过多的代码 
2. 谨慎使用单独的 except 语句处理所有异常，最好能定位具体的异常 
3. 注意异常捕获的顺序，在适合的层次处理异常，Python 是按内建异常类的继承结构处理异常的，所以推荐的做法是将继承结构中子类异常在前抛出，父类异常在后抛出 
4. 使用更为友好的异常信息，遵守异常参数的规范

建议 25：避免 finally 中可能发生的陷阱
当 finally 执行完毕时，之前临时保存的异常将会再次被抛出，但如果 finally 语句中产生了新的异常或执行了 return 或 break 语句，那么临时保存的异常将会被丢失，从而异常被屏蔽。 
在实际开发中不推荐 finally 中使用 return 语句进行返回。

建议 26：深入理解 None，正确判断对象是否为空
（None被判断为False，但是空集不等于None） 
类型FalseTrue布尔False （与0等价）True （与1等价）字符串""（ 空字符串）非空字符串，例如 " ", "blog"数值0, 0.0非0的数值，例如：1, 0.1, -1, 2容器[], (), {}, set()至少有一个元素的容器对象，例如：[0], (None,), ['']NoneNone非None对象

>>> id(None)
10743840
>>> a = None
>>> id(a)
10743840
>>> l = []
>>> if l is not None:       # 判断逻辑 l 不为空
...     print('l is {}'.format(l))
... else:
...     print('l is empty')
... 
l is []
>>> if l:   # #3 正确的判断形式
...     print('Do something...')
... else:
...     print('Do other thing...')
... 
Do other thing...
执行中会调用nonzero()来判断自身对象是否为空并返回0/1或True/False，如果没有定义该方法，Python 将调用len()进行判断，返回 0 表示为空。如果一个类既没有定义len()又没有定义nonzero()，该类实例用 if 判断为True。

建议 27：连接字符串优先使用 join 而不是 +
连接字符串使用join将使程序性能更佳，原因是使用每次使用 + 都需要格外分一块内存去存储结果。

建议 28：格式化字符串时尽量使用 .format 而不是 %
format方法总结 
使用 format 格式化字符串有以下好处：

format更为灵活，参数顺序和格式不必完全相同
format更为方便的作为参数传递（例如支持列表的索引操作）
%最终会被format取代
%容易抛出异常，而format则不会（未尝是好事）
建议 29：区别对待可变对象和不可变对象
Python 中一切皆对象，每个对象都有一个唯一的标识符（id）、类型（type）和值。数字、字符串、元组属于不可变对象，字典、列表、字节数组属于可变对象。

默认参数在初始化时仅仅被评估一次，以后直接使用第一次评估的结果，course 指向的是 list 的地址，每次操作的实际上是 list 所指向的具体列表，所以对于可变对象的更改会直接影响原对象。

最好的方法是传入None作为默认参数，在创建对象的时候动态生成列表。

>>> list1 = ['a', 'b', 'c']
>>> list2 = list1
>>> list1.append('d')
>>> list2
['a', 'b', 'c', 'd']
>>> list3 = list1[:]    # 可变对象的切片操作相当于浅拷贝
>>> list3.remove('a')
>>> list3
['b', 'c', 'd']
>>> list1
['a', 'b', 'c', 'd']
建议 30：[]、() 和 {} 一致的容器初始化形式
使用列表解析、字典解析、元组解析等替代for循环 
解析式有以下好处：

代码更清晰、简洁
效率更高、速度更快
（代码更加pythonic）
建议 31：记住函数传参既不是传值也不是传引用
正确的说法是传对象（call by object）或传对象的引用（call-by-object-reference），函数参数在传递过程中将整个对象传入，对可变对象的修改在函数外部以及内部都可见，对不可变对象的”修改“往往是通过生成一个新对象然是赋值实现的。

建议 32：警惕默认参数潜在的问题
其中就是默认参数如果是可变对象，在调用者和被调用者之间是共享的。 
所以默认值使用可以使用数字、字符串、元组 
不可以使用字典、列表、字节数组

import time
# 对当前系统时间进行处理
def report(when=time.time): # 而不是when=time.time()
    pass
建议 33：慎用变长参数
原因如下： 
1. 使用过于灵活，导致函数签名不够清晰，存在多种调用方式 
2. 使用*args和**kw简化函数定义就意味着函数可以有更好的实现方法

使用场景： 
1. 为函数添加一个装饰器 
2. 参数数目不确定 
3. 实现函数的多态或子类需要调用父类的某些方法时

建议 34：深入理解 str() 和repr() 的区别
（str方法面向用户更为友好，repr解释更加清晰） 
总结几点：

str()面向用户，返回用户友好和可读性强的字符串类型；repr()面向 Python 解释器或开发人员，返回 Python 解释器内部的含义
解释器中输入a默认调用repr()，而print(a)默认调用str()
repr()返回值一般可以用eval()还原对象：obj == eval(repr(obj))
以上两个方法分别调用内建的str()和repr()，一般来说类中都应该定义repr()，但当可读性比准确性更为重要时应该考虑str()，用户实现repr()方法的时候最好保证其返回值可以用eval()是对象还原
建议 35：分清 staticmethod 和 classmethod 的适用场景
（需要返回类的实例时，或需要动态生成对应类的类变量，使用classmethod，方法不跟实例与类相关（不适用self和cls），定义为静态方法（工具方法））

调用类方法装饰器的修饰器的方法，会隐式地传入该对象所对应的类，可以动态生成对应的类的类变量，同时如果我们期望根据不同的类型返回对应的类的实例，类方法才是正确的解决方案。

反观静态方法，当我们所定义的方法既不跟特定的实例相关也不跟特定的类相关，可以将其定义为静态方法，这样使我们的代码能够有效地组织起来，提高可维护性。

当然，也可以考虑定义一个模块，将一组的方法放入其中，通过模块来访问。

第 4 章 库
建议 36：掌握字符串的基本用法
# 小技巧：Python 遇到未闭合的小括号会自动将多行代码拼接为一行
>>> s = ('SELECT * '
...      'FROM table '
...      'WHERE field="value"')
>>> s
'SELECT * FROM table WHERE field="value"'
# Python2 中使用 basestring 正确判断一个变量是否是字符串
# 性质判断
isalnum() isalpha() isdigit() islower() isupper() isspace() istitle()
# 查找替换
startswith(prefix[, start[, end]]) endswith(suffix[, start[, end]]) # prefix参数可以接收 tuple 类型的实参
count(sub[, start[, end]]) find(sub[, start[, end]]) index(sub[, start[, end]])
rfind(sub[, start[, end]]) rindex(sub[, start[, end]]) replace(old, new[, count])   # count是指的替换次数，不指定就全部替换
# 切分
partition(sep) rpartition(sep) splitlines([keepends]) split([sep, [, maxsplit]]) rsplit([sep[, maxsplit]])  # partition 返回一个3个元素的元组对象
# 变形
lower() upper() capitalize() swapcase() title()
# 删减填充
strip([chars]) lstrip([chars]) rstrip([chars]) # 没有提供chars默认是空白符，由string.whitespace 常量定义
center(width[, fillchar]) ljuct(width[, fillchar]) rjust(width[, fillchar])
zfill(width) expandtabs([tabszie])
下面来介绍一些易混淆的地方：

>>> '  hello world'.split()
['hello', 'world']
>>> '  hello world'.split(' ')
['', '', 'hello', 'world']
>>> 'hello wORld'.title()
'Hello World'
>>> import string
>>> string.capwords(' hello world!')
'Hello World!'
>>> string.whitespace
' \t\n\r\x0b\x0c'
建议 37：按需选择 sort() 或者 sorted()
（sort方法是原地操作，sorted是复制操作，不需要保留源列表用sort）

# 函数原型
sorted(iterable[, cmp[, key[, reverse]]])   # 返回一个排序后的列表
s.sort([cmp[, key[, reverse]]])             # 直接修改原列表，返回为None
>>> persons = [{'name': 'Jon', 'age': 32}, {'name': 'Alan', 'age': 50}, {'name': 'Bob', 'age': 23}]
>>> sorted(persons, key=lambda x: (x['name'], -x['age']))
[{'name': 'Alan', 'age': 50}, {'name': 'Bob', 'age': 23}, {'name': 'Jon', 'age': 32}]
>>> a = (1, 2, 4, 2, 3)
>>> sorted(a)
[1, 2, 2, 3, 4]
所以如果实际过程中需要保留原有列表，可以使用sorted()。sort()不需要复制原有列表，消耗内存较小，效率较高。同时传入参数key比传入参数cmp效率要高，cmp传入的函数在整个排序过程中会调用多次，而key针对每个元素仅作一次处理。

建议 38：使用 copy 模块深拷贝对象
（对可变对象需要真正意义上的复制时使用copy.deepcopy，这种需求情况还是比较少见）

浅拷贝（shallow copy）：构造一个新的复合对象并将从原对象中发现的引用插入该对象中。工厂函数、切片操作、copy 模块中的 copy 操作都是浅拷贝

深拷贝（deep copy）：针对引用所指向的对象继续执行拷贝，因此产生的对象不受其它引用对象操作的影响。深拷贝需要依赖 copy 模块的 deepcopy() 操作

在 python 中，标识一个对象唯一身份的是：对象的id(内存地址)，对象类型，对象值，而浅拷贝就是创建一个具有相同类型，相同值但不同id的新对象。因此使用浅拷贝的典型使用场景是：对象自身发生改变的同时需要保持对象中的值完全相同，比如 list 排序：

def sorted_list(olist, key=None):
    copied_list = copy.copy(olist)
    copied_list.sort(key=key)
    return copied_list
a = [3, 2, 1]       # [3, 2, 1]
b = sorted_list(a)  # [1, 2, 3]
深拷贝不仅仅拷贝了原始对象自身，也对其包含的值进行拷贝，它会递归的查找对象中包含的其他对象的引用，来完成更深层次拷贝。因此，深拷贝产生的副本可以随意修改而不需要担心会引起原始值的改变：

>>> a = [1, 2]
>>> b = [a, a]
>>> b
[[1, 2], [1, 2]]
>>> from copy import deepcopy
>>> c = deepcopy(b)
>>> id(b[0]) == id(c[0])
False
>>> id(b[0]) == id(b[1])
True
>>> c
[[1, 2], [1, 2]]
>>> c[0].append(3)
>>> c
[[1, 2, 3], [1, 2, 3]]
使用 copy 和 deepcopy 可以完成对一个对象拷贝的定制。

参考博文

建议 39： 使用 Counter 进行计数统计
（需要计数统计时，使用Counter） 
常见的计数统计可以使用dict、defaultdict、set和list，不过 Python 提供了一个更优雅的方式：

>>> from collections import Counter
>>> some_data = {'a', '2', 2, 3, 5, 'c', '7', 4, 5, 'd', 'b'}
>>> Counter(some_data)
Counter({'7'，: 1, 2: 1, 3: 1, 4: 1, 5: 1, '2': 1, 'b': 1, 'a': 1, 'd': 1, 'c': 1})
Counter 类属于字典类的子类，是一个容器对象，用来统计散列对象，支持+、-、&、|，其中&和|分别返回两个 Counter 对象各元素的最小值和最大值。

# 初始化
Counter('success')
Counter(s=3, c=2, e=1, u=1)
Counter({'s': 3, 'c': 2, 'u': 1, 'e': 1})
# 常用方法
list(Counter(some_data).elements())     # 获取 key 值
Counter(some_data).most_common(2)       # 前 N 个出现频率最高的元素以及对应的次数
(Counter(some_data))['y']               # 访问不存在的元素返回 0
c = Counter('success')
c.update('successfully')                # 更新统计值
c.subtract('successfully')              # 统计数相减，允许为0或为负
建议 40：深入掌握 ConfigParser
（啥程序都需要配置，要搞懂配置库） 
几乎所有的应用程序都会读取配置文件，ini是一种比较常见的文件格式：

[section1]
option1=0
Python 提供标准库 ConfigParser 来支持它：

import ConfigParser
conf = ConfigParser.ConfigParser()
conf.read('example.conf')
print(conf.get('section1', 'in_default'))
再来看个SQLAlchemy配置文件的例子：

[DEFAULT]
conn_str = %(dbn)s://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s
dbn = mysql
user = root
host = localhost
port = 3306
[db1]
user = aaa
pw = ppp
db = example
[db2]
host = 192.168.0.110
pw = www
db = example
import ConfigParser
conf = ConfigParser.ConfigParser()
conf.read('format.conf')
print(conf.get('db1', 'conn_str'))
print(conf.get('db2', 'conn_str'))
建议 41：使用argparse处理命令行参数
处理命令行参数可以使用argsparse，也推荐更方便更高级的docopt进行处理 
docopt是根据常见的帮助信息定义了一套领域特定语言（DSL），并通过这个DSL Parser参数生成处理命令行参数的代码。

建议 42：使用pandas处理大型CSV文件
pandas作为python三大科学运算库之一的使用。

建议 43：一般情况下使用ElementTree解析xml格式文件
使用Beautifulsoup更好

建议 44：理解模块pickle优劣
序列化，简单来说就是把内存中的数据结构在不丢失其身份和类型信息的情况下转成对象的文本或二进制表示的过程。同类支持序列化的模块有pickle，json，marshal和shelve。

pickle是最通用的序列化模块，我们应该优先使用c语言实现的cPickle，速度比pickle快1000倍，区别是cPickle不能被继承。

pickle主要通过dump和load两种方法序列化与反序列化（存储与读取）

import cPickle as pickle
# 序列化
my_data= {"name":"Python","type":"Language"}
fp = open("picklefile.dat","wb")
pickle.dump(my_data, fp)
fp.close
# 反序列化
fp = open("picklefile.dat", "rb")
out = pickle.load(fp)
pickle模块的优点： 
1. 接口简单，容易使用 
2. 存储格式有平台通用型，在Linux和Windouws都可以使用，兼容性好。 
3. 支持数据类型广泛，除了常规项，还包含能通过类的__dict__或__getstate__()方法返回的对象。 
4. pickle是可扩展的，对于不可序列化的对象，也可以通过特殊方法来返回示例在被pickle时的状态。 
5. 能够自动维护对象间的引用

pickle模块的限制： 
* pickle不能保证操作的原子性。当错误发生时，可能部分数据已经被保存；如果对象处于深递归状态，那么可能超过python的最大递归深度，可以通过sys.setrecursionlimit()进行扩展 
* pickle存在安全性问题，为乳清提供了可能 
* pickle协议是python特定的，不同语言之间数据内容可能难以保障。

简单来说，对于需要存储的对象，使用pickle，另外很重要的一点，dat文件用pickle模块来读。

建议 45：序列化的另一个不错的选择 -- JSON
cJson比python自身的json要快250倍 
JSON的优势： 
1. 使用简单，支持多种数据类型（集合、列表、字典、关联数组等等） 
2. 存储格式可读性更友好，易于修改 
3. 支持跨平台跨语言操作，所占空间更小 
4. 具有较强扩展性

json的速度比pickle略慢 
json不支持序列化dateime

建议 46：使用 traceback 获取栈信息
当发生异常，开发人员往往需要看到现场信息，trackback 模块可以满足这个需求，先列几个常用的：

traceback.print_exc()   # 打印错误类型、值和具体的trace信息
traceback.print_exception(type, value, traceback[, limit[, file]])  # 前三个参数的值可以从sys.exc_info()
raceback.print_exc([limit[, file]])         # 同上，不需要传入那么多参数
traceback.format_exc([limit])               # 同 print_exc()，返回的是字符串
traceback.extract_stack([file, [, limit]])  # 从当前栈中提取 trace 信息
traceback 模块获取异常相关的数据是通过sys.exc_info()得到的，该函数返回异常类型type、异常value、调用和堆栈信息traceback组成的元组。

同时 inspect 模块也提供了获取 traceback 对象的接口。

建议 47：使用 logging 记录日志信息
仅仅将信息输出到控制台是远远不够的，更为常见的是使用日志保存程序运行过程中的相关信息，如运行时间、描述信息以及错误或者异常发生时候的特定上下文信息。Python 提供 logging 模块提供了日志功能。

常规日志设置:

logging.basicConfig(
            filename='%s.log' % self.table_name,
            level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S')
logging是线程安全的，不支持多进程写入同一个子文件，对多个进程需要配置不同的日志文件。

建议 48：使用 threading 模块编写多线程程序
（python3中，使用threadpool线程池模块比较省心） 
由于 GIL 的存在，让 Python 多线程编程在多核处理器中无法发挥优势，但在一些使用场景下使用多线程仍然比较好，如等待外部资源返回，或建立反应灵活的用户界面，或多用户程序等。

Python3 提供了两个模块：_thread和threading。_thread提供了底层的多线程支持，使用比较复杂，下面我们重点说说threading。

Python 多线程支持用两种方式来创建线程：一种通过继承 Thread 类，重写它的run()方法；另一种是创建一个 threading.Thread 对象，在它的初始化函数init()中将可调用对象作为参数传入。

threading模块中不仅有 Lock 指令锁，RLock 可重入指令锁，还支持条件变量 Condition、信号量 Semaphore、BoundedSemaphore 以及 Event 事件等。

下面有一个比较经典的例子来理解多线程：

import threading
from time import ctime,sleep
def music(func):
    for i in range(2):
        print("I was listening to %s. %s" % (func,ctime()))
        sleep(1)    # 程序休眠 1 秒
def move(func):
    for i in range(2):
        print("I was at the %s! %s" % (func,ctime()))
        sleep(5)
threads = []
t1 = threading.Thread(target=music,args=('爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=move,args=('阿凡达',))
threads.append(t2)
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)   # 声明线程为守护线程
        t.start()
    #3
    print("all over %s" % ctime())
以下是运行结果：

I was listening to 爱情买卖. Tue Apr  4 17:57:02 2017
I was at the 阿凡达! Tue Apr  4 17:57:02 2017
all over Tue Apr  4 17:57:02 2017
分析：threading 模块支持线程守护，我们可以通过setDaemon()来设置线程的daemon属性，当其属性为True时，表明主线程的退出可以不用等待子线程完成，反之，daemon属性为False时所有的非守护线程结束后主线程才会结束，那运行结果为：

I was listening to 爱情买卖. Tue Apr  4 18:05:26 2017
I was at the 阿凡达! Tue Apr  4 18:05:26 2017
all over Tue Apr  4 18:05:26 2017
I was listening to 爱情买卖. Tue Apr  4 18:05:27 2017
I was at the 阿凡达! Tue Apr  4 18:05:31 2017
继续修改代码，当我们在#3处加入t.join()，此方法能够阻塞当前上下文环境，直到调用该方法的线程终止或到达指定的 timeout，此时在运行程序：

I was listening to 爱情买卖. Tue Apr  4 18:08:15 2017
I was at the 阿凡达! Tue Apr  4 18:08:15 2017
I was listening to 爱情买卖. Tue Apr  4 18:08:16 2017
I was at the 阿凡达! Tue Apr  4 18:08:20 2017
all over Tue Apr  4 18:08:25 2017
当我们把music函数的休眠时间改为 4 秒，再次运行程序：

I was listening to 爱情买卖. Tue Apr  4 18:11:16 2017
I was at the 阿凡达! Tue Apr  4 18:11:16 2017
I was listening to 爱情买卖. Tue Apr  4 18:11:20 2017
I was at the 阿凡达! Tue Apr  4 18:11:21 2017
all over Tue Apr  4 18:11:26 2017
此时我们就可以发现多线程的威力了，music虽然增加了 3 秒，然而总的运行时间仍然为 10 秒。

建议 49：使用 Queue 使多线程编程更加安全
（同47，使用threadingpool） 
线程间的同步和互斥，线程间数据的共享等这些都是涉及线程安全要考虑的问题。纵然 Python 中提供了众多的同步和互斥机制，如 mutex、condition、event 等，但同步和互斥本身就不是一个容易的话题，稍有不慎就会陷入死锁状态或者威胁线程安全。

如何保证线程安全呢？我们先来看看 Python 中的 Queue 模块：

Queue.Queue(maxsize)：先进先出，maxsize 为队列大小，其值为非正数的时候为无限循环队列

Queue.LifoQueue(maxsize)：后进先出，相当于栈

Queue.PriorityQueue(maxsize)：优先级队列

以上队列所支持的方法：

Queue.qsize()：返回近似的队列大小。当该值 > 0 的时候并不保证并发执行的时候 get() 方法不被阻塞，同样，对于 put() 方法有效。

Queue.empty()：队列为空的时候返回 True，否则返回 False

Queue.full()：当设定了队列大小的情况下，如果队列满则返回 True，否则返回 False

Queue.put(item[, block[, timeout]])：往队列中添加元素 item，block 设置为 False 的时候，如果队列满则抛出 Full 异常。如果 block 设置为 True，timeout 为 None 的时候则会一直等待直到有空位置，否则会根据 timeout 的设定超时后抛出 Full 异常

Queue.put_nowait(item)：等于 put(item, False).block 设置为 False 的时候，如果队列空则抛出 Empty 异常。如果 block 设置为 True、timeout 为 None 的时候则会一直等到有元素可用，否则会根据 timeout 的设定超时后抛出 Empty 异常

Queue.get([block[, timeout]])：从队列中删除元素并返回该元素的值

Queue.get_nowait()：等价于 get(False)

Queue.task_done()：发送信号表明入列任务已经完成，经常在消费者线程中用到

Queue.join()：阻塞直至队列中所有的元素处理完毕

首先 Queue 中的队列和 collections.deque 所表示的队列并不一样，前者用于不同线程之间的通信，内部实现了线程的锁机制，后者是数据结构上的概念，支持 in 方法。

Queue 模块实现了多个生产者多个消费者的队列，当多线程之间需要信息安全的交换的时候特别有用，因此这个模块实现了所需要的锁原语，为 Python 多线程编程提供了有力的支持，它是线程安全的。

先来看一个简单的例子：

import os
import Queue
import threading
import urllib2
class DownloadThread(threading.Thead):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            url = self.queue.get()
            print('{0} begin download {1}...'.format(self.name, url))
            self.download_file(url)
            self.queque.task_done()
            print('{0} download completed!!!'.format(self.name))
    def download_file(self, url):
        urlhandler = urllib2.urlopen(url)
        fname = os.path.basename(url) + '.html'
        with open(fname, 'wb') as f:
            while True:
                chunk = urlhandler.read(1024)
                if not chunk: break
                f.write(chunk)
if __name__ == '__main__':
    urls = ['http://wiki.python.org/moin/WebProgramming',
            'https://www.createspace.com/3611970',
            'http://wiki.python.org/moin/Documentation'
    ]
    queue = Queue.Queue()
    for i range(5):
        t = DownloadThread(queue)
        t.setDaemon(True)
        t.start()
    for url in urls:
        queue.put(url)
    queue.join()
第 5 章 设计模式
建议 50：利用模块实现单例模式
单例模式可以保证徐彤中一个类只有一个实例且该实例易被外界访问，常用来使用XxxManager之类的功能。

满足单例模式的 3 个需求：

只能有一个实例
必须自行创建这个实例
必须自行向整个系统提供这个实例
模块采用的其实是天然的单例的实现方式，在入口文件导入： 
* 所有的变量都会绑定到模块 
* 模块只初始化一次 
* import 机制是线程安全的，保证了在并发状态下模块也只是一个实例

# World.py
import Sun
def run():
    while True:
        Sun.rise()
        Sun.set()
# main.py
import World
World.run()
此外，Borg模式可以创造任意数量实例，并保证状态共享。

建议 51：用 mixin 模式让程序更加灵活
模板方法模式就是在一个方法中定义一个算法的骨架，并将一些实现步骤延迟到子类中。模板方法可以使子类在不改变算法结构的情况下，重新定义算法中的某些步骤。

class UseSimpleTeapot(object):
    def get_teapot(self):
        return SimpleTeapot()
class UseKungfuTeapot(object):
    def get_teapot(self):
        return KungfuTeapot()
class OfficePeople(People, UseSimpleTeapot): pass
class HomePeople(People, UseSimpleTeapot): pass
class Boss(People, UseKungfuTeapot): pass
def simple_tea_people():
    people = People()
    people.__base__ += (UseSimpleTeapot,)
    return people
def coffee_people():
    people = People()
    people.__base__ += (UseCoffeepot,)
def tea_and_coffee_people():
    people = People()
    people.__base__ += (UseSimpleTeapot, UserCoffeepot,)
    return people
def boss():
    people = People()
    people.__base__ += (KungfuTeapot, UseCoffeepot, )
    return people
代码的原理在于每个类都有一个bases属性，它是一个元组，用来存放所有的基类，作为动态语言，Python 中的基类可以在运行中可以动态改变。所以当我们向其中增加新的基类时，这个类就拥有了新的方法，这就是混入mixin。

利用这个技术我们可以在不修改代码的情况下就可以完成需求：

import mixins   # 把员工需求定义在 Mixin 中放在 mixins 模块
def staff():
    people = People()
    bases = []
    for i in config.checked():
        bases.append(getattr(maxins, i))
    people.__base__ += tuple(bases)
    return people
建议 52：用发布订阅模式实现松耦合
发布订阅模式是一种编程模式，消息的发送者不会发送其消息给特定的接收者，而是将发布的消息分为不同的类别直接发布，并不关注订阅者是谁。而订阅者可以对一个或多个类别感兴趣，且只接收感兴趣的消息，并且不关注是哪个发布者发布的消息。要实现这个模式，就需要一个中间代理人. Broker，它维护着发布者和订阅者的关系，订阅者把感兴趣的主题告诉它，而发布者的信息也通过它路由到各个订阅者处。

from collections import defaultdict
route_table = defaultdict(list)
def sub(topic, callback):
    if callback in route_table[topic]:
        return
    route_table[topic].append(callback)
def pub(topic, *args, **kw):
    for func in route_table[topic]:
        func(*args, **kw)
将以上代码放在 Broker.py 的模块，省去了各种参数检测、优先处理、取消订阅的需求，只向我们展示发布订阅模式的基础实现：

import Broker
def greeting(name):
    print('Hello, {}'.format(name))
Broker.sub('greet', greeting)
Broker.pub('greet', 'LaiYonghao')
因为python-message的消息订阅默认是全局性的，所以有可能产生名字冲突。

建议 53：用状态模式美化代码
所谓状态模式，就是当一个对象的内在状态改变时允许改变其行为，但这个对象看起来像是改变了其类。

简单的状态模式有其缺点：

查询对象的当前状态很麻烦
状态切换时需要对原状态做一些清扫工作，而对新状态做初始化工作，因每个状态需要做的事情不同，全部写在切换状态的代码中必然重复
这时候我们可以使用 Python-state 来解决。

from state import curr, switch, stateful, State, behavior
@stateful
class People(object):
    class Workday(State):
        default = True
        @behavior   # 相当于staticmethod
        def day(self):  # 这里的self并不是Python的关键字，而是有助于我们理解状态类的宿主是People的实例
            print('work hard')
    class Weekend(State):
        @behavior
        def day(self):
            print('play harder')
people = People()
while True:
    for i in range(1, 8):
        if i == 6:
            switch(people, People.Weekend)
        if i == 1:
            switch(people, People.Workday)
        people.day()
@statefule装饰器重载了被修饰的类的getattr()从而使得 People 的实例能够调用当前状态类的方法，同时被修饰的类的实例是带有状态的，能够使用curr()查询当前状态，也可以使用switch()进行状态切换，默认的状态是通过类定义的 default 属性标识，default = True的类成为默认状态。

状态类 Workday 和 Weekend 继承自 State 类，从其派生的子类可以使用begin和end_状态转换协议，自定义进入和离开当前状态时对宿主的初始化和清理工作。

下面是一个真实业务的例子：

@stateful
class User(object):
    class NeedSignin(State):
        default = True
        @behavior
        def signin(self, user, pwd):
            ...
            switch(self, Player.Signin)
    class Signin(State):
        @behavior
        def move(self, dst): ...
        @behavior
        def atk(self, other): ...
第 6 章 内部机制
建议 54：理解 built-in objects
Python 中一切皆对象，在新式类中，object 是所有内建类型的基类，用户自定义的类可以继承自 object 也可继承自内建类型。

In [1]: class TestNewClass:
   ...:     __metaclass__ = type
   ...:     
In [2]: type(TestNewClass)
Out[2]: type
In [3]: TestNewClass.__bases__
Out[3]: (object,)
In [4]: a = TestNewClass()
In [5]: type(a)
Out[5]: __main__.TestNewClass
In [6]: a.__class__
Out[6]: __main__.TestNewClass
新式类支持 property 和描述符特性，作为新式类的祖先，Object 类还定义了一些特殊方法：new()、init()、delattr()、getattribute()、setattr()、hash()、repr()、str()等。

建议 55：init()不是构造方法
class A(object):
    def __new__(cls, *args, **kw):
        print(cls)
        print(args)
        print(kw)
        print('----------')
        instance = object.__new__(cls, *args, **kw)
        print(instance)
    def __init__(self, a, b):
        print('init gets called')
        print('self is {}'.format(self))
        self.a, self.b = a, b
a1 = A(1, 2)
print(a1.a)
print(a1.b)
运行结果：

<class '__main__.A'>
(1, 2)
{}
----------
Traceback (most recent call last):
  File "test.py", line 19, in <module>
    a1 = A(1, 2)
  File "test.py", line 13, in __new__
    instance = object.__new__(cls, *args, **kw)
TypeError: object() takes no parameters
从结果中我们可以看出，程序输出了new()调用所产生的输出，并抛出了异常。于是我们知道，原来new()才是真正创建实例，是类的构造方法，而init()是在类的对象创建好之后进行变量的初始化。上面程序抛出异常是因为在new()中没有显式返回对象，a1此时为None，当去访问实例属性时就抛出了异常。

根据官方文档，我们可以总结以下几点：

object.new(cls[, args...])：其中 cls 代表类，args 为参数列表，为静态方法

object.init(self[, args...])：其中 self 代表实例对象，args 为参数列表，为实例方法

控制实例创建的时候可使用 new() ，而控制实例初始化的时候使用 init()

new()需要返回类的对象，当返回类的对象时将会自动调用init()进行初始化，没有对象返回，则init()不会被调用。init() 方法不需要显示返回，默认为 None，否则会在运行时抛出 TypeError

但当子类继承自不可变类型，如 str、int、unicode 或者 tuple 的时候，往往需要覆盖new()

覆盖 new() 和 init() 的时候这两个方法的参数必须保持一致，如果不一致将导致异常

下面我们来总结需要覆盖new()的几种特殊情况：

当类继承不可变类型且默认的 new() 方法不能满足需求的时候

用来实现工厂模式或者单例模式或者进行元类编程，使用new()来控制对象创建

作为用来初始化的 init() 方法在多继承的情况下，子类的 init()方法如果不显式调用父类的 init() 方法，则父类的 init() 方法不会被调用；通过super(子类， self).init()显式调用父类的初始化方法；对于多继承的情况，我们可以通过迭代子类的 bases 属性中的内容来逐一调用父类的初始化方法

分别来看例子加深理解：

# 创建一个集合能够将任何以空格隔开的字符串变为集合中的元素
class UserSet(frozenset):
    def __new__(cls, *args):
        if args and isinstance(args[0], str):
            args = (args[0].split(), ) + args[1:]
        return super(UserSet, cls).__new__(cls, *args)
# 一个工厂类根据传入的参量决定创建出哪一种产品类的实例
class Shape(object):
    def __init__(object):
        pass
    def draw(self):
        pass
class Triangle(Shape):
    def __init__(self):
        print("I am a triangle")
    def draw(self):
        print("I am drawing triangle")
class Rectangle(Shape):
    def __init__(self):
        print("I am a rectangle")
    def draw(self):
        print("I am drawing triangle")
class Trapezoid(Shape):
    def __init__(self):
        print("I am a trapezoid")
    def draw(self):
        print("I am drawing triangle")
class Diamond(Shape):
    def __init__(self):
        print("I am a diamond")
    def draw(self):
        print("I am drawing triangle")
class ShapeFactory(object):
    shapes = {'triangle': Triangle, 'rectangle': Rectangle, 'trapzoid': Trapezoid, 'diamond': Diamond}
    def __new__(cls, name):
        if name in ShapeFactory.shapes.keys():
            print('creating a new shape {}'.format(name))
            return ShapeFactory.shapes[name]()
        else:
            print('creating a new shape {}'.format(name))
            return Shape()
建议 56：理解名字查找机制
在 Python 中所谓的变量其实都是名字，这些名字指向一个或多个 Python 对象。这些名字都存在于一个表中（命名空间），我们称之为局部变量，调用locals()可以查看：

>>> locals()
{'__package__': None, '__spec__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__doc__': None, '__name__': '__main__', '__builtins__': <module 'builtins' (built-in)>}
>>> globals()
{'__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__builtins__': <module 'builtins' (built-in)>, '__package__': None, '__doc__': None, '__spec__': None, '__name__': '__main__'}
Python 中的作用域分为：

局部作用域: 一般来说函数的每次调用都会创建一个新的本地作用域, 拥有新的命名空间

全局作用域: 定义在 Python 模块文件中的变量名拥有全局作用域, 即在一个文件的顶层的变量名仅在这个文件内可见

嵌套作用域: 多重函数嵌套时才会考虑, 即使使用 global 进行申明也不能达到目的, 其结果最终是在嵌套的函数所在的命名空间中创建了一个新的变量

内置作用域: 通过标准库中的builtin实现的

当访问一个变量的时候，其查找顺序遵循变量解析机制 LEGB 法则，即依次搜索 4 个作用域：局部作用域、嵌套作用域、全局作用域以及内置作用域，并在第一个找到的地方停止搜寻，如果没有搜到，则会抛出异常。

Python 3 中引入了 nonlocal 关键字:

def foo(x):
    a = x
    def bar():
        nonlocal a
        b = a * 2
        a = b + 1
        print(a)
    return bar
建议 57: 为什么需要 self 参数
在类中当定义实例方法的时候需要将第一个参数显式声明为self, 而调用时不需要传入该参数, 我们通过self.x访问实例变量, self.m()访问实例方法:

class SelfTest(object):
    def __init__(self.name):
        self.name = name
    def showself(self):
        print('self here is {}'.format(self))
    def display(self):
        self.showself()
        print('The name is: {}'.format(self.name))
st = SelfTest('instance self')
st.display()
print('{}'.format(st))
运行结果:

self here is <__main__.SelfTest object at 0x7f440c53ba58>
The name is: instance self
<__main__.SelfTest object at 0x7f440c53ba58>
从中可以发现, self 表示实例对象本身, 即 SelfTest 类的对象在内存中的地址. self 是对对象 st 本身的引用, 我们在调用实例方法时也可以直接传入实例对象: SelfTest.display(st). 同时 self 或 cls 并不是 Python 的关键字, 可以替换成其它的名称.

Python 中为什么需要 self 呢:

借鉴了其他语言的特征

Python 语言本身的动态性决定了使用 self 能够带来一定便利

在存在同名的局部变量以及实例变量的情况下使用 self 使得实例变量更容易被区分

Python 属于一级对象语言, 我们有好几种方法可以引用类方法:

A.__dict__["m"]
A.m.__func__
Python 的哲学是：显示优于隐式（Explicit is better than implicit）.

建议 58: 理解 MRO 与多继承
古典类与新式类所采取的 MRO (Method Resolution Order, 方法解析顺序) 的实现方式存在差异.

古典类是按照多继承申明的顺序形成继承树结构, 自顶向下采用深度优先的搜索顺序. 而新式类采用的是 C3 MRO 搜索方法, 在新式类通过mro得到 MRO 的搜索顺序, C3 MRO 的算法描述如下:

假定，C1C2...CN 表示类 C1 到 CN 的序列，其中序列头部元素（head）=C1，序列尾部（tail）定义 = C2...CN；

C 继承的基类自左向右分别表示为 B1，B2...BN

L[C] 表示 C 的线性继承关系，其中 L[object] = object。

算法具体过程如下：

L[C(B1...BN)] = C + merge(L[B1] ... L[BN], B1 ... BN)

其中 merge 方法的计算规则如下：在 L[B1]...L[BN]，B1...BN 中，取 L[B1] 的 head，如果该元素不在 L[B2]...L[BN]，B1...BN 的尾部序列中，则添加该元素到 C 的线性继承序列中，同时将该元素从所有列表中删除（该头元素也叫 good head），否则取 L[B2] 的 head。继续相同的判断，直到整个列表为空或者没有办法找到任何符合要求的头元素（此时，将引发一个异常）。

菱形继承是我们在多继承设计的时候需要尽量避免的一个问题.

建议 59: 理解描述符机制
In [1]: class MyClass(object):
   ...:     class_attr = 1
   ...:     
# 每一个类都有一个__dict__属性, 包含它的所有属性
In [2]: MyClass.__dict__
Out[2]:
mappingproxy({'__dict__': <attribute '__dict__' of 'MyClass' objects>,
              '__doc__': None,
              '__module__': '__main__',
              '__weakref__': <attribute '__weakref__' of 'MyClass' objects>,
              'class_attr': 1})
In [3]: my_instance = MyClass()
# 每一个实例也相应有一个实例属性, 我们通过实例访问一个属性时,
# 它首先会尝试在实例属性中查找, 找不到会到类属性中查找
In [4]: my_instance.__dict__
Out[4]: {}
# 实例访问类属性
In [5]: my_instance.class_attr
Out[5]: 1
# 如果通过实例增加一个属性,只能改变此实例的属性
In [6]: my_instance.inst_attr = 'china'
In [7]: my_instance.__dict__
Out[7]: {'inst_attr': 'china'}
# 对于类属性而言并没有丝毫变化
In [8]: MyClass.__dict__
Out[8]:
mappingproxy({'__dict__': <attribute '__dict__' of 'MyClass' objects>,
              '__doc__': None,
              '__module__': '__main__',
              '__weakref__': <attribute '__weakref__' of 'MyClass' objects>,
              'class_attr': 1})
# 我们可以动态地给类增加一个属性
In [9]: MyClass.class_attr2 = 100
In [10]: my_instance.class_attr2
Out[10]: 100
# 但Python的内置类型并不能随意地为它增加属性或方法
.操作符封装了对实例属性和类属性两种不同属性进行查找的细节。

但是如果是访问方法呢:

In [1]: class MyClass(object):
   ...:     def my_method(self):
   ...:         print('my_method')
   ...:         
In [2]: MyClass.__dict__['my_method']
Out[2]: <function __main__.MyClass.my_method>
In [3]: MyClass.my_method
Out[3]: <function __main__.MyClass.my_method>
In [4]: type(MyClass.my_method)
Out[4]: function
In [5]: type(MyClass.__dict__['my_method'])
Out[5]: function
根据通过实例访问属性和根据类访问属性的不同，有以下两种情况：

一种是通过实例访问，比如代码 obj.x，如果 x 是一个描述符，那么 getattribute() 会返回 type(obj).dict['x'].get(obj, type(obj)) 结果，即：type(obj) 获取 obj 的类型；type(obj).dict['x'] 返回的是一个描述符，这里有一个试探和判断的过程；最后调用这个描述符的 get() 方法。

另一个是通过类访问的情况，比如代码 cls.x，则会被 getattribute()转换为 cls.dict['x'].get(None, cls)。

描述符协议是一个 Duck Typing 的协议，而每一个函数都有 get 方法，也就是说其他每一个函数都是描述符。所有对属性, 方法进行修饰的方案往往都用到了描述符, 如classmethod, staticmethod, property等, 以下是property的参考实现:

class Property(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError, "unreadable attribute"
        return self.fget(obj)
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError, "can't set attribute"
        self.fset(obj, value)
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError, "can't delete attribute"
        self.fdel(obj)
建议 60：区别getattr()和getattribute()方法
以上两种方法可以对实例属性进行获取和拦截：

getattr(self, name)：适用于属性在实例中以及对应的类的基类以及祖先类中都不存在；

getattribute(self, name)：对于所有属性的访问都会调用该方法

但访问不存在的实例属性时，会由内部方法getattribute()抛出一个 AttributeError 异常，也就是说只要涉及实例属性的访问就会调用该方法，它要么返回实际的值，要么抛出异常。详情请参考。

那么getattr()在什么时候调用呢：

属性不在实例的dict中；

属性不在其基类以及祖先类的dict中；

触发AttributeError异常时（注意，不仅仅是getattribute()方法的AttributeError异常，property 中定义的get()方法抛出异常的时候也会调用该方法）。

当这两个方法同时被定义的时候，要么在getattribute()中显式调用，要么触发AttributeError异常，否则getattr()永远不会被调用。

我们知道 property 也能控制属性的访问，如果一个类中如果定义了 property、getattribute()以及getattr()来对属性进行访问控制，会最先搜索getattribute()方法，由于 property 对象并不存在于 dict 中，因此并不能返回该方法，此时会搜索 property 中的get()方法；当 property 中的set()方法对属性进行修改并再次访问 property 的get()方法会抛出异常，这时会触发getattr()的调用。

getattribute()总会被调用，而getattr()只有在getattribute()中引发异常的情况下调用。

第 6 章 内部机制
建议 61：使用更加安全的 property
property 实际上是一种实现了 get() 、 set() 方法的类，用户也可以根据自己的需要定义个性化的 property，其实质是一种特殊的数据描述符（数据描述符：如果一个对象同时定义了 get() 和 set() 方法，则称为数据描述符，如果仅定义了get() 方法，则称为非数据描述符）。它和普通描述符的区别在于：普通描述符提供的是一种较为低级的控制属性访问的机制，而 property 是它的高级应用，它以标准库的形式提供描述符的实现，其签名形式为：

property(fget=None, fset=None, fdel=None, doc=None) -> property attribute
property 有两种常用的形式：

1、第一种形式

class Some_Class(object):
    def __init__(self):
        self._somevalue = 0
    def get_value(self):
        print('calling get method to return value')
        return self._somevalue
    def set_value(self, value):
        print('calling set method to set value')
        self._somevalue = value
    def def_attr(self):
        print('calling delete method to delete value')
        def self._somevalue
    x = property(get_value, set_value, del_attr, "I'm the 'x' property.")
obj = Some_Class()
obj.x = 10
print(obj.x + 2)
del obj.x
obj.x
2、第二种形式

class Some_Class(self):
    _x = None
    def __init__(self):
        self._x = None
    @property
    def x(self):
        print('calling get method to return value')
        return self._x
    @x.setter
    def x(self, value):
        print('calling set method to set value')
        self._x = value
    @x.deleter
    def x(self):
        print('calling delete method to delete value')
        del self._x
以上我们可以总结出 property 的优势：

1、代码更简洁，可读性更强

2、更好的管理属性的访问。property 将对属性的访问直接转换为对对应的 get、set 等相关函数的调用，属性能够更好地被控制和管理，常见的应用场景如设置校验（如检查电子邮件地址是否合法）、检查赋值的范围（某个变量的赋值范围必须在 0 到 10 之间）以及对某个属性进行二次计算之后再返回给用户（将 RGB 形式表示的颜色转换为#**）或者计算某个依赖于其他属性的属性。

class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    def get_date(self):
        return self.year + '-' + self.month + '-' + self.day
    def set_date(self, date_as_string):
        year, month, day = date_as_string.split('-')
        if not (2000 <= year <= 2017 and 0 <= month <= 12 and 0 <= day <= 31):
            print('year should be in [2000:2017]')
            print('month should be in [0:12]')
            print('day should be in [0, 31]')
            raise AssertionError
        self.year = year
        self.month = month
        self.day = day
    date = property(get_date, set_date)
创建一个 property 实际上就是将其属性的访问与特定的函数关联起来，相对于标准属性的访问，property 的作用相当于一个分发器，对某个属性的访问并不直接操作具体的对象，而对标准属性的访问没有中间这一层，直接访问存储属性的对象：

3、代码可维护性更好。property 对属性进行再包装，以类似于接口的形式呈现给用户，以统一的语法来访问属性，当具体实现需要改变的时候，访问的方式仍然可以保持一致。

4、控制属性访问权限，提高数据安全性。如果用户想设置某个属性为只读，来看看 property 是如何实现的。

class PropertyTest(object):
    def __init__(self):
        self.__var1 = 20
    @property
    def x(self):
        return self.__var1
pt = PropertyTest()
print(pt.x)
pt.x = 12
注意这样使用 property 并不能真正意义达到属性只读的目的，正如以双下划线命令的变量并不是真正的私有变量一样，我们还是可以通过pt._PropertyTest__var1 = 30来修改属性。稍后我们会讨论如何实现真正意义上的只读和私有变量。

既然 property 本质是特殊类，那么就可以被继承，我们就可以自定义 property：

def update_meta(self, other):
    self.__name__ = other.__name__
    self.__doc__ = other.__doc__
    self.__dict__.update(other.__dict__)
    return self
class UserProperty(property):
    def __new__(cls, fget=None, fset=None, fdel=None, doc=None):
        if fget is not None:
            def __get__(obj, objtype=None, name=fget.__name__):
                fegt = getattr(obj, name)
                return fget()
            fget = update_meta(__get__, fget)
        if fset is not None:
            def __set__(obj, value, name=fset.__name__):
                fset = getattr(obj, name)
                return fset(value)
            fset = update_meta(__set__, fset)
        if fdel is not None:
            def __delete__(obj, name=fdel.__name__):
                fdel = getattr(obj, name)
                return fdel()
            fdel = update_meta(__delete__, fdel)
        return property(fget, fset, fdel, doc)
class C(object):
    def get(self):
        return self._x
    def set(self, x):
        self._x = x
    def delete(self):
        del self._x
    x = UserProperty(get, set, delete)
c = C()
c.x = 1
print(c.x)
def c.x
UserProperty 继承自 property，其构造函数 new(cls, fget=None, fset=None, fdel=None, doc=None) 中重新定义了 fget() 、 fset() 以及 fdel() 方法以满足用户特定的需要，最后返回的对象实际还是 property 的实例，因此用户能够像使用 property 一样使用 UserProperty。

使用 property 并不能真正完全达到属性只读的目的，用户仍然可以绕过阻碍来修改变量。我们来看看一个可行的实现：

def ro_property(obj, name, value):
    setattr(obj.__class__, name, property(lambda obj: obj.__dict__["__" + name]))
    setattr(obj, "__" + name, value)
class ROClass(object):
    def __init__(self, name, available):
        ro_property(self, "name", name)
        self.available = available
a = ROClass("read only", True)
print(a.name)
a._Article__name = "modify"
print(a.__dict__)
print(ROClass.__dict__)
print(a.name)
建议 62：掌握 metaclass
关于元类这知识点，推荐stackoverflow上Jerub的回答

这里有中文翻译

建议 63：熟悉 Python 对象协议
因为 Python 是一门动态语言，Duck Typing 的概念遍布其中，所以其中的 Concept 并不以类型的约束为载体，而另外使用称为协议的概念。

In [1]: class Object(object):
   ...:     def __str__(self):
   ...:         print('calling __str__')
   ...:         return super(Object, self).__str__()
   ...:     
In [2]: o = Object()
In [3]: print('%s' % o)
calling __str__
<__main__.Object object at 0x7f133ff20160>
比如在字符串格式化中，如果有占位符 %s，那么按照字符串转换的协议，Python 会自动地调用相应对象的 str() 方法。

总结一下 Python 中的协议：

1、类型转换协议：str() 、repr()、init()、long()、float()、nonzero() 等。

2、比较大小的协议：cmp()，当两者相等时，返回 0，当 self < other 时返回负值，反之返回正值。同时 Python 又有 eq()、ne()、lt()、gt() 等方法来实现相等、不等、小于和大于的判定。这也就是 Python 对 ==、!=、< 和 > 等操作符的进行重载的支撑机制。

3、数值相关的协议：



其中有个 Python 中特有的概念：反运算。以something + other为例，调用的是something的add()，若没有定义add()，这时候 Python 有一个反运算的协议，查看other有没有radd()，如果有，则以something为参数调用。

4、容器类型协议：容器的协议是非常浅显的，既然为容器，那么必然要有协议查询内含多少对象，在 Python 中，就是要支持内置函数 len()，通过 len() 来完成，一目了然。而 getitem()、setitem()、delitem() 则对应读、写和删除，也很好理解。iter() 实现了迭代器协议，而 reversed() 则提供对内置函数 reversed() 的支持。容器类型中最有特色的是对成员关系的判断符 in 和 not in 的支持，这个方法叫 contains()，只要支持这个函数就能够使用 in 和 not in 运算符了。

5、可调用对象协议：所谓可调用对象，即类似函数对象，能够让类实例表现得像函数一样，这样就可以让每一个函数调用都有所不同。

In [1]: class Functor(object):
   ...:     def __init__(self, context):
   ...:         self._context = context
   ...:     def __call__(self):
   ...:         print('do something with %s' % self._context)
   ...:         
In [2]: lai_functor = Functor('lai')
In [3]: yong_functor = Functor('yong')
In [4]: lai_functor()
do something with lai
In [5]: yong_functor()
do something with yong
6、还有一个可哈希对象，它是通过 hash() 方法来支持 hash() 这个内置函数的，这在创建自己的类型时非常有用，因为只有支持可哈希协议的类型才能作为 dict 的键类型（不过只要继承自 object 的新式类就默认支持了）。

7、上下文管理器协议：也就是对with语句的支持，该协议通过enter()和exit()两个方法来实现对资源的清理，确保资源无论在什么情况下都会正常清理：

class Closer:
    def __init__(self):
        self.obj = obj
    def __enter__(self):
        return self.obj
    def __exit__(self, exception_type, exception_val, trace):
        try:
            self.obj.close()
        except AttributeError:
            print('Not closeable.')
            return True
这里 Closer 类似的类已经在标准库中存在，就是 contextlib 里的 closing。

以上就是常用的对象协议，灵活地用这些协议，我们可以写出更为 Pythonic 的代码，它更像是声明，没有语言上的约束，需要大家共同遵守。

建议 64：利用操作符重载实现中缀语法
熟悉 Shell 脚本编程应该熟悉|管道符号，用以连接两个程序的输入输出。如按字母表反序遍历当前目录的文件与子目录：

$ ls | sort -r
Videos/
Templates/
Public/
Pictures/
Music/
examples.desktop
Dropbox/
Downloads/
Documents/
Desktop/
管道的处理非常清晰，因为它是中缀语法。而我们常用的 Python 是前缀语法，比如类似的 Python 代码应该是 sort(ls(), reverse=True)。

Julien Palard 开发了一个 pipe 库，利用|来简化代码，也就是重载了 ror() 方法：

class Pipe:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return self.function(other)
    def __call__(self, *args, **kwargs):
        return Pipe(lambda x: self.function(x, *args, **kwargs))
这个 Pipe 类可以当成函数的 decorator 来使用。比如在列表中筛选数据：

@Pipe
def where(iterable, predicate):
    return (x for x in iterable if (predicate(x)))
pipe 库内置了一堆这样的处理函数，比如 sum、select、where 等函数尽在其中，请看以下代码：

fib() | take_while(lambda x: x < 1000000) \
      | where(lambda x: x % 2) \
      | select(lambda x: x * x) \
      | sum()
这样写的代码，意义是不是一目了然呢？就是找出小于 1000000 的斐波那契数，并计算其中的偶数的平方之和。

我们可以使用pip3 install pipe安装，安装完后测试：

In [1]: from pipe import *
In [2]: [1, 2, 3, 4, 5] | where(lambda x: x % 2) | tail(2) | select(lambda x: x * x) | add
Out[2]: 34
此外，pipe 是惰性求值的，所以我们完全可以弄一个无穷生成器而不用担心内存被用完：

In [3]: def fib():
   ...:     a, b = 0, 1
   ...:     while True:
   ...:         yield a
   ...:         a, b = b, a + b
   ...:         
In [4]: euler2 = fib() | where(lambda x: x % 2 ==0) | take_while(lambda x: x < 400000) | add
In [5]: euler2
Out[5]: 257114
读取文件，统计文件中每个单词出现的次数，然后按照次数从高到低对单词排序：

from __future__ import print_function
from re import split
from pipe import *
with open("test_descriptor.py") as f:
    print(f.read()
          | Pipe(lambda x: split("/W+", x))
          | Pipe(lambda x:(i for i in x if i.strip()))
          | groupby(lambda x:x)
          | select(lambda x:(x[0], (x[1] | count)))
          | sort(key=lambda x: x[1], reverse=True)
          )
建议 65：熟悉 Python 的迭代器协议
首先介绍一下 iter() 函数，iter() 可以输入两个实参，为了简化，第二个可选参数可以忽略。iter() 函数返回一个迭代器对象，接受的参数是一个实现了 iter() 方法的容器或迭代器（精确来说，还支持仅有 getitem() 方法的容器）。对于容器而言，iter() 方法返回一个迭代器对象，而对迭代器而言，它的 iter() 方法返回其自身。

所谓协议，是一种松散的约定，并没有相应的接口定义，所以把协议简单归纳如下：

实现 iter() 方法，返回一个迭代器

实现 next() 方法，返回当前的元素，并指向下一个元素的位置，如果当前位置已无元素，则抛出 StopIteration 异常

没错，其实 for 语句就是对获取容器的迭代器、调用迭代器的 next() 方法以及对 StopIteration 进行处理等流程进行封装的语法糖（类似的语法糖还有 in/not in 语句）。

迭代器最大的好处是定义了统一的访问容器（或集合）的统一接口，所以程序员可以随时定义自己的迭代器，只要实现了迭代器协议即可。除此之外，迭代器还有惰性求值的特性，它仅可以在迭代至当前元素时才计算（或读取）该元素的值，在此之前可以不存在，在此之后也可以销毁，也就是说不需要在遍历之前实现准备好整个迭代过程中的所有元素，所以非常适合遍历无穷个元素的集合或或巨大的事物（斐波那契数列、文件）：

class Fib(object):
    def __init__(self):
        self._a, self._b = 0, 1
    def __iter__(self):
        return self
    def next(self):
        self._a, self._b = self._b, self._a + self._b
        return self._a
for i, f in enumerate(Fib()):
    print(f)
    if i > 10:
        break
下面来看看与迭代有关的标准库 itertools。

itertools 的目标是提供一系列计算快速、内存高效的函数，这些函数可以单独使用，也可以进行组合，这个模块受到了 Haskell 等函数式编程语言的启发，所以大量使用 itertools 模块中的函数的代码，看起来有点像函数式编程语言。比如 sum(imap(operator.mul, vector1, vector2)) 能够用来运行两个向量的对应元素乘积之和。

itertools 提供了以下几个有用的函数：chain() 用以同时连续地迭代多个序列；compress()、dropwhile() 和 takewhile() 能用遴选序列元素；tee() 就像同名的 UNIX 应用程序，对序列作 n 次迭代；而 groupby 的效果类似 SQL 中相同拼写的关键字所带的效果。

[k for k, g in groupby("AAAABBBCCDAABB")] --> A B C D A B
[list(g) for k, g in groupby("AAAABBBCCD")] --> AAAA BBB CC D
除了这些针对有限元素的迭代帮助函数之外，还有 count()、cycle()、repeat() 等函数产生无穷序列，这 3 个函数就分别可以产生算术递增数列、无限重复实参的序列和重复产生同一个值的序列。

组合函数意义product()计算 m 个序列的 n 次笛卡尔积permutations()产生全排列combinations()产生无重复元素的组合combinations_with_replacement()产生有重复元素的组合

In [1]: from itertools import *
In [2]: list(product('ABCD', repeat=2))
Out[2]: 
[('A', 'A'),
 ('A', 'B'),
 ('A', 'C'),
 ('A', 'D'),
 ('B', 'A'),
 ('B', 'B'),
 ('B', 'C'),
 ('B', 'D'),
 ('C', 'A'),
 ('C', 'B'),
 ('C', 'C'),
 ('C', 'D'),
 ('D', 'A'),
 ('D', 'B'),
 ('D', 'C'),
 ('D', 'D')]
# 其中 product() 可以接受多个序列
In [5]: for i in product('ABC', '123', repeat=2):
   ...:     print(''.join(i))
   ...:     
A1A1
A1A2
A1A3
A1B1
A1B2
A1B3
A1C1
A1C2
...
建议 66：熟悉 Python 的生成器
生成器，顾名思义，就是按一定的算法生成一个序列。

迭代器虽然在某些场景表现得像生成器，但它绝非生成器；反而是生成器实现了迭代器协议的，可以在一定程度上看作迭代器。

如果一个函数，使用了 yield 关键字，那么它就是一个生成器函数。当调用生成器函数时，它返回一个迭代器，不过这个迭代器是以生成器对象的形式出现的：

In [1]: def fib(n):
   ...:     a, b = 0, 1
   ...:     while a < n:
   ...:         yield a
   ...:         a, b = b, a + b
   ...: for i, f in enumerate(fib(10)):
   ...:     print(f)
   ...:     
0
1
1
2
3
5
8
In [2]: f = fib(10)
In [3]: type(f)
Out[3]: generator
In [4]: dir(f)
Out[4]: 
['__class__',
 '__del__',
 '__delattr__',
 '__dir__',
 '__doc__',
 '__eq__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__gt__',
 '__hash__',
 '__init__',
 '__iter__',
 '__le__',
 '__lt__',
 '__name__',
 '__ne__',
 '__new__',
 '__next__',
 '__qualname__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 'close',
 'gi_code',
 'gi_frame',
 'gi_running',
 'gi_yieldfrom',
 'send',
 'throw']
可以看到它返回的是一个 generator 类型的对象，这个对象带有iter()和next()方法，可见确实是一个迭代器。

分析：

每一个生成器函数调用之后，它的函数并不执行，而是到第一次调用 next() 的时候才开始执行；

yield 表达式的默认返回值为 None，当第一次调用 next() 方法时，生成器函数开始执行，执行到 yield 表达式为止；

再次调用next()方法，函数将在上次停止的地方继续执行。

send() 是全功能版本的 next()，或者说 next() 是 send()的快捷方式，相当于 send(None)。还记得 yield 表达式有一个返回值吗？send() 方法的作用就是控制这个返回值，使得 yield 表达式的返回值是它的实参。

除了能 yield 表达式的“返回值”之外，也可以让它抛出异常，这就是 throw() 方法的能力。

对于常规业务逻辑的代码来说，对特定的异常有很好的处理（比如将异常信息写入日志后优雅的返回），从而实现从外部影响生成器内部的控制流。

当调用 close() 方法时，yield 表达式就抛出 GeneratorExit 异常，生成器对象会自行处理这个异常。当调用 close() 方法，再次调用 next()、send() 会使生成器对象抛出 StopIteration 异常。换言之，这个生成器对象已经不再可用。当生成器对象被 GC 回收时，会自动调用 close()。

生成器还有两个很棒的用处：

实现 with 语句的上下文管理协议，利用的是调用生成器函数时函数体并不执行，当第一次调用 next() 方法时才开始执行，并执行到 yield 表达式后中止，直到下一次调用 next() 方法这个特性；

实现协程，利用的是 send()、throw()、close() 等特性。

第二个用处在下一个小节讲解，先看第一个：

In [1]: with open('/tmp/test.txt', 'w') as f:
   ...:     f.write('Hello, context manager.')
   ...:     
In [2]: from contextlib import contextmanager
In [3]: @contextmanager
   ...: def tag(name):
   ...:     print('<%s>' % name)
   ...:     yield
   ...:     print('<%s>' % name)
   ...:     
In [4]: with tag('h1'):
   ...:     print('foo')
   ...:     
<h1>
foo
<h1>
这是 Python 文档中的例子。通过 contextmanager 对 next()、throw()、close() 的封装，yield 大大简化了上下文管理器的编程复杂度，对提高代码可维护性有着极大的意义。除此之外，yield 和 contextmanager 也可以用以“池”模式中对资源的管理和回收，具体的实现留给大家去思考。

建议 67：基于生成器的协程及 greenlet
先介绍一下协程的概念：

协程，又称微线程和纤程等，据说源于 Simula 和 Modula-2 语言，现代编程语言基本上都支持这个特性，比如 Lua 和 ruby 都有类似的概念。

协程往往实现在语言的运行时库或虚拟机中，操作系统对其存在一无所知，所以又被称为用户空间线程或绿色线程。又因为大部分协程的实现是协作式而非抢占式的，需要用户自己去调度，所以通常无法利用多核，但用来执行协作式多任务非常合适。用协程来做的东西，用线程或进程通常也是一样可以做的，但往往多了许多加锁和通信的操作。

基于生产着消费者模型，比较抢占式多线程编程实现和协程编程实现。线程实现至少有两点硬伤：

对队列的操作需要有显式/隐式（使用线程安全的队列）的加锁操作。

消费者线程还要通过 sleep 把 CPU 资源适时地“谦让”给生产者线程使用，其中的适时是多久，基本上只能静态地使用经验，效果往往不尽如人意。

下面来看看协程的解决方案，代码来自廖雪峰 Python3 教程：

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'
def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()
c = consumer()
produce(c)
执行结果：

[PRODUCER] Producing 1...
[CONSUMER] Consuming 1...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 2...
[CONSUMER] Consuming 2...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 3...
[CONSUMER] Consuming 3...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 4...
[CONSUMER] Consuming 4...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 5...
[CONSUMER] Consuming 5...
[PRODUCER] Consumer return: 200 OK
注意到consumer函数是一个generator，把一个consumer传入produce后：

首先调用c.send(None)启动生成器；

然后，一旦生产了东西，通过c.send(n)切换到consumer执行；

consumer通过yield拿到消息，处理，又通过yield把结果传回；

produce拿到consumer处理的结果，继续生产下一条消息；

produce决定不生产了，通过c.close()关闭consumer，整个过程结束。

整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。

最后套用Donald Knuth的一句话总结协程的特点：

“子程序就是协程的一种特例。”

greenlet 是一个 C 语言编写的程序库，它与 yield 关键字没有密切的关系。greenlet 这个库里最为关键的一个类型就是 PyGreenlet 对象，它是一个 C 结构体，每一个 PyGreenlet 都可以看到一个调用栈，从它的入口函数开始，所有的代码都在这个调用栈上运行。它能够随时记录代码运行现场，并随时中止，以及恢复。它跟 yield 所能够做到的相似，但更好的是它提供从一个 PyGreenlet 切换到另一个 PyGreenlet 的机制。

from greenlet import greenlet
def test1():
    print(12)
    gr2.switch()
    print(34)
def test2():
    print(56)
    gr1.switch()
    print(78)
gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
协程虽然不能充分利用多核，但它跟异步 I/O 结合起来以后编写 I/O 密集型应用非常容易，能够在同步的代码表面下实现异步的执行，其中的代表当属将 greenlet 与 libevent/libev 结合起来的 gevent 程序库，它是 Python 网络编程库。最后，以 gevent 并发查询 DNS 的例子为例，使用它进行并发查询 n 个域名，能够获得几乎 n 倍的性能提升：

In [1]: import gevent
In [2]: from gevent import socket
In [3]: urls = ['www.baidu.com', 'www.python.org', 'www.qq.com']
In [4]: jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
In [5]: gevent.joinall(jobs, timeout=2)
Out[5]: 
[<Greenlet at 0x7f37e439c508>,
 <Greenlet at 0x7f37e439c5a0>,
 <Greenlet at 0x7f37e439c340>]
In [6]: [job.value for job in jobs]
Out[6]: ['115.239.211.112', '151.101.24.223', '182.254.34.74']
建议 68：理解 GIL 的局限性
多线程 Python 程序运行的速度比只有一个线程的时候还要慢，除了程序本身的并行性之外，很大程度上与 GIL 有关。由于 GIL 的存在，多线程编程在 Python 中并不理想。GIL 被称为全局解释器锁（Global Interpreter Lock），是 Python 虚拟机上用作互斥线程的一种机制，它的作用是保证任何情况下虚拟机中只会有一个线程被运行，而其他线程都处于等待 GIL 锁被释放的状态。不管是在单核系统还是多核系统中，始终只有一个获得了 GIL 锁的线程在运行，每次遇到 I/O 操作便会进行 GIL 锁的释放。

但如果是纯计算的程序，没有I/O操作，解释器则会根据sys.setcheckinterval的设置来自动进行线程间的切换，默认是每隔100个内部时钟就会释放GIL锁从而轮换到其他线程：

在单核 CPU 中，GIL 对多线程的执行并没有太大影响，因为单核上的多线程本质上就是顺序执行的。但对于多核 CPU，多线程并不能真正发挥优势带来效率上明显的提升，甚至在频繁 I/O 操作的情况下由于存在需要多次释放和申请 GIL 的情形，效率反而会下降。

那么 Python 解释器为什么要引入 GIL 呢？

我们知道 Python 中对象的管理与引用计数器密切相关，当计数器变为 0 的时候，该对象便会被垃圾回收器回收。当撤销一个对象的引用时，Python 解释器对对象以及其计数器的管理分为以下两步：

使引用计数值减1

判断该计数值是否为 0，如果为0，则销毁该对象

鉴于此，Python 引入了 GIL，以保证对虚拟机内部共享资源访问的互斥性。

GIL 的引入确实使得多线程不能再多核系统中发挥优势，但它也带来了一些好处：大大简化了 Python 线程中共享资源的管理，在单核 CPU 上，由于其本质是顺序执行的，一般情况下多线程能够获得较好的性能。此外，对于扩展的 C 程序的外部调用，即使其不是线程安全的，但由于 GIL 的存在，线程会阻塞直到外部调用函数返回，线程安全不再是一个问题。

在 Python3.2 中重新实现了 GIL，其实现机制主要集中在两个方面：一方面是使用固定的时间而不是固定数量的操作指令来进行线程的强制切换；另一个方面是在线程释放 GIL 后，开始等待，直到某个其他线程获取 GIL 后，再开始尝试去获取 GIL，这样虽然可以避免此前获得 GIL 的线程，不会立即再次获取 GIL，但仍然无法保证优先级高的线程优先获取 GIL。这种方式只能解决部分问题，并未改变 GIL 的本质。

Python 提供了其他方式可以绕过 GIL 的局限，比如使用多进程 multiprocess 模块或者采用 C 语言扩展的方式，以及通过 ctypes 和 C 动态库来充分利用物理内核的计算能力。

建议 69：对象的管理与垃圾回收
class Leak(object):
    def __init__(self):
        print('object with id %d was born' % id(self))
while(True):
    A = Leak()
    B = Leak()
    A.b = B
    B.a = A
    A = None
    B = None
运行上述程序，我们会发现 Python 占用的内存消耗一直在持续增长，直到最后内存耗光。

先简单谈谈 Python 中的内存管理的方式：

Python 使用引用计数器（Reference counting）的方法来管理内存中的对象，即针对每一个对象维护一个引用计数值来表示该对象当前有多少个引用。

当其他对象引用该对象时，其引用计数会增加 1，而删除一个队当前对象的引用，其引用计数会减 1。只有当引用计数的值为 0 时的时候该对象才会被垃圾收集器回收，因为它表示这个对象不再被其他对象引用，是个不可达对象。引用计数算法最明显的缺点是无法解决循环引用的问题，即两个对象相互引用。如同上述代码中A、B对象之间相互循环引用造成了内存泄露，因为两个对象的引用计数都不为 0，该对象也不会被垃圾回收器回收，而无限循环导致一直在申请内存而没有释放。

循环引用常常会在列表、元组、字典、实例以及函数使用时出现。对于由循环引用而导致的内存泄漏的情况，可以使用 Python 自带的一个 gc 模块，它可以用来跟踪对象的“入引用（incoming reference）“和”出引用（outgoing reference）”，并找出复杂数据结构之间的循环引用，同时回收内存垃圾。有两种方式可以触发垃圾回收：一种是通过显式地调用 gc.collect() 进行垃圾回收；还有一种是在创建新的对象为其分配内存的时候，检查 threshold 阈值，当对象的数量超过 threshold 的时候便自动进行垃圾回收。默认情况下阈值设为（700，10，10），并且 gc 的自动回收功能是开启的，这些可以通过 gc.isenabled() 查看：

In [1]: import gc
In [2]: print(gc.isenabled())
True
In [3]: gc.isenabled()
Out[3]: True
In [4]: gc.get_threshold()
Out[4]: (700, 10, 10)
所以修改之前的代码：

def main():
    collected = gc.collect()
    print("Garbage collector before running: collected {} objects.".format(collected))
    print("Creating reference cycles...")
    A = Leak()
    B = Leak()
    A.b = B
    B.a = A
    A = None
    B = None
    collected = gc.collect()
    print(gc.garbage)
    print("Garbage collector after running: collected {} objects".format(collected))
if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
gc.garbage 返回的是由于循环引用而产生的不可达的垃圾对象的列表，输出为空表示内存中此时不存在垃圾对象。gc.collect() 显示所有收集和销毁的对象的数目，此处为 4（2 个对象 A、B，以及其实例属性 dict）。

我们再来考虑一个问题：如果在类 Leak 中添加析构方法 del()，会发现 gc.garbage 的输出不再为空，而是对象 A、B 的内存地址，也就是说这两个对象在内存中仍然以“垃圾”的形式存在。

这是什么原因呢？实际上当存在循环引用并且当这个环中存在多个析构方法时，垃圾回收器不能确定对象析构的顺序，所以为了安全起见仍然保持这些对象不被销毁。而当环被打破时，gc 在回收对象的时候便会再次自动调用 del() 方法。

gc 模块同时支持 DEBUG 模式，当设置 DEBUG 模式之后，对于循环引用造成的内存泄漏，gc 并不释放内存，而是输出更为详细的诊断信息为发现内存泄漏提供便利，从而方便程序员进行修复。更多 gc 模块可以参考文档 。

第 7 章 使用工具辅助项目开发
Python 项目的开发过程，其实就是一个或多个包的开发过程，而这个开发过程又由包的安装、管理、测试和发布等多个节点构成，所以这是一个复杂的过程，使用工具进行辅助开发有利于减少流程损耗，提升生产力。本章将介绍几个常用的、先进的工具，比如 setuptools、pip、paster、nose 和 Flask-PyPI-Proxy 等。

建议 70：从 PyPI 安装包
PyPI 全称 Python Package Index，直译过来就是“Python 包索引”，它是 Python 编程语言的软件仓库，类似 Perl 的 CPAN 或 Ruby 的 Gems。

$ tar zxvf requests-1.2.3.tar.gz
$ cd requests-1.2.3
$ python setup.py install
$ sudo aptitude install python-setuptools   # 自动安装包
建议 71：使用 pip 和 yolk 安装、管理包
pip 常用命令：

$ pip install package_name
$ pip uninstall package_name
$ pip show package_name
$ pip freeze
建议 72：做 paster 创建包
distutils 标准库，至少提供了以下几方面的内容：

支持包的构建、安装、发布（打包）

支持 PyPI 的登记、上传

定义了扩展命令的协议，包括 distutils.cmd.Command 基类、distutils.commands 和 distutils.key_words 等入口点，为 setuptools 和 pip 等提供了基础设施。

要使用 distutils，按习惯需要编写一个 setup.py 文件，作为后续操作的入口点。在arithmetic.py同层目录下建立一个setup.py文件，内容如下：

from distutils.core import setup
setup(name="arithmetic",
     version='1.0',
     py_modules=["your_script_name"],
     )
setup.py 文件的意义是执行时调用 distutils.core.setup() 函数，而实参是通过命名参数指定的。name 参数指定的是包名；version 指定的是版本；而 py_modules 参数是一个序列类型，里面包含需要安装的 Python 文件。

编写好 setup.py 文件以后，就可以使用 python setup.py install 进行安装了。

distutils 还带有其他命令，可以通过 python setup.py --help-commands 进行查询。

实际上若要把包提交到 PyPI，还要遵循 PEP241，给出足够多的元数据才行，比如对包的简短描述、详细描述、作者、作者邮箱、主页和授权方式等：

setup(
    name='requests',￼
    version=requests.__version__,￼
    description='Python HTTP for Humans.',￼
    long_description=open('README.rst').read() + '\n\n' +￼
                    open('HISTORY.rst').read(),￼
    author='Kenneth Reitz',￼
    author_email='me@kennethreitz.com',￼
    url='http://python-requests.org',￼
    packages=packages,￼
    package_data={'': ['LICENSE', 'NOTICE'], 'requests': ['*.pem']},￼
    package_dir={'requests': 'requests'},￼
    include_package_data=True,￼
    install_requires=requires,￼
    license=open('LICENSE').read(),￼
    zip_safe=False,￼
    classifiers=(￼
        'Development Status :: 5 - Production/Stable',￼
        'Intended Audience :: Developers',￼
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',￼
        'Programming Language :: Python',￼
        'Programming Language :: Python :: 2.6',￼
        'Programming Language :: Python :: 2.7',￼
        'Programming Language :: Python :: 3',￼
        'Programming Language :: Python :: 3.3',￼
        ),￼
)
包含太多内容了，如果每一个项目都手写很困难，最好找一个工具可以自动创建项目的 setup.py 文件以及相关的配置、目录等。Python 中做这种事的工具有好几个，做得最好的是 pastescript。pastescript 是一个有着良好插件机制的命令行工具，安装以后就可以使用 paster 命令，创建适用于 setuptools 的包文件结构。

安装好 pastescript 以后可以看到它注册了一个命令行入口 paster：

$ paster create --list-template     # 查询目录安装的模板
$ paster create -o arithmethc-2 -t basic_package atithmetic     # 为了 atithmetic 生成项目包
简单地填写几个问题以后，paster 就在 arithmetic-2 目录生成了名为 arithmetic 的包项目。

用上 --config 参数，它是一个类似 ini 文件格式的配置文件，可以在里面填好各个模板变量的值（查询模板有哪些变量用 --list-variables参数），然后就可以使用了。

[pastescript]
description = corp-prj
license_name = 
keywords = Python
long_description = corp-prj
author = xxx corp
author_email = xxx@example.com
url = http://example.com
version = 0.0.1
以上配置文件使用paster create -t basic_package --config="corp-prj-setup.cfg" arithmetic

建议 73：理解单元测试概念
单元测试用来验证程序单元的正确性，一般由开发人员完成，是测试过程的第一个环节，以确保缩写的代码符合软件需求和遵循开发目标。好的单元测试有以下好处：

减少了潜在 bug，提高了代码的质量。

大大缩减软件修复的成本

为集成测试提供基本保障

有效的单元测试应该从以下几个方面考虑：

测试先行，遵循单元测试步骤：

创建测试计划（Test Plan）

编写测试用例，准备测试数据

编写测试脚本

编写被测代码，在代码完成之后执行测试脚本

修正代码缺陷，重新测试直到代码可接受为止

遵循单元测试基本原则：

一致性：避免currenttime = time.localtime()这种不确定执行结果的语句

原子性：执行结果只有 True 或 False 两种

单一职责：测试应该基于情景（scenario）和行为，而不是方法。如果一个方法对应着多种行为，应该有多个测试用例；而一个行为即使对应多个方法也只能有一个测试用例

隔离性：不能依赖于具体的环境设置，如数据库的访问、环境变量的设置、系统的时间等；也不能依赖于其他的测试用例以及测试执行的顺序，并且无条件逻辑依赖。单元测试的所有输入应该是确定的，方法的行为和结构应是可以预测的。

使用单元测试框架，在单元测试方面常见的测试框架有 PyUnit 等，它是 JUnit 的 Python 版本，在 Python2.1 之前需要单独安装，在 Python2.1 之后它成为了一个标准库，名为 unittest。它支持单元测试自动化，可以共享地进行测试环境的设置和清理，支持测试用例的聚集以及独立的测试报告框架。unittest 相关的概念主要有以下 4 个：

测试固件（test fixtures）：测试相关的准备工作和清理工作，基于类 TestCase 创建测试固件的时候通常需要重新实现 setUp() 和 tearDown() 方法。当定义了这些方法的时候，测试运行器会在运行测试之前和之后分别调用这两个方法

测试用例（test case）：最小的测试单元，通常基于 TestCase 构建

测试用例集（test suite）：测试用例的集合，使用 TestSuite 类来实现，除了可以包含 TestCase 外，也可以包含 TestSuite

测试运行器（test runner）：控制和驱动整个单元测试过程，一般使用 TestRunner 类作为测试用例的基本执行环境，常用的运行器为 TextTestRunner，它是 TestRunner 的子类，以文字方式运行测试并报告结果。

# 测试以下类
class MyCal(object):
    def add(self, a, b):
        return a + b
    def sub(self, a, b):
        return a - b
# 测试
class MyCalTest(unittest.TestCase):
    def setUp(self):
        print('running set up')
    def tearDown(self):
        print('running teardown')
        self.mycal = None
    def testAdd(self):
        self.assertEqual(self.mycal.add(-1, 7), 6)
    def testSub(self):
        self.assertEqual(self.mycal.sub(10, 2), 8)
suite = unittest.TestSuite()
suite.addTest(MyCalTest("testAdd"))
suite.addTest(MyCalTest("testSub"))
runner = unittest.TextTestRunner()
runner.run(suite)
运行 python3 -m unittest -v MyCalTest 得到测试结果。

建议 74：为包编写单元测试
直接上一个实例：

__author__ = 'Windrivder'
import unittest
from app import create_app, db
from flask import current_app
class BasicsTestCase(unittest.TestCase):
    def setUp(self):    # 测试前运行
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # 创建全新的数据库
    def tearDown(self):  # 测试后运行
        db.session.remove()
        db.drop_all()   # 删除数据库
        self.app_context.pop()
    # 测试程序实例是否存在
    def test_app_exists(self):
        self.assertFalse(current_app is None)
    # 测试程序能在测试配置中运行
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
__author__ = 'Windrivder'
import time
import unittest
from datetime import datetime
from app import create_app, db
from app.models import AnonymousUser, Follow, Permission, Role, User
class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='Cat')
        self.assertTrue(u.password_hash is not None)
    def test_no_password_getter(self):
        u = User(password='Cat')
        with self.assertRaises(AttributeError):
            u.password
    def test_password_verifycation(self):
        u = User(password='Cat')
        self.assertTrue(u.verify_password('Cat'))
        self.assertFalse(u.verify_password('Dog'))
    def test_password_salts_are_random(self):
        u = User(password='Cat')
        u2 = User(password='Cat')
        self.assertTrue(u.password_hash != u2.password_hash)
    def test_roles_and_permission(self):
        Role.insert_roles()
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))
    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
    def test_timestamps(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.member_since).total_seconds() < 3)
        self.assertTrue(
            (datetime.utcnow() - u.last_seen).total_seconds() < 3)
    def test_ping(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)
建议 75：利用测试驱动开发提高代码的可测性
测试驱动开发（Test Driven Development，TDD）是敏捷开发中一个非常重要的理念，它提倡在真正开始编码之前测试先行，先编写测试代码，再在其基础上通过基本迭代完成编码，并不断完善。一般来说，遵循以下过程：

编写部分测试用例，并运行测试

如果测试通过，则回到测试用例编写的步骤，继续添加新的测试用例

如果测试失败，则修改代码直到通过测试

当所有测试用例编写完成并通过测试之后，再来考虑对代码进行重构

关于测试驱动开发和提高代码可测性方面有几点需要说明：

TDD 只是手段而不是目的，因此在实践中尽量只验证正确的事情，并且每次仅仅验证一件事。当遇到问题时不要局限于 TDD 本身所涉及的一些概念，而应该回头想想采用 TDD 原本的出发点和目的是什么

测试驱动开发本身就是一门学问

代码的不可测性可以从以下几个方面考量：实践 TDD 困难；外部依赖太多；需要写很多模拟代码才能完成测试；职责太多导致功能模糊；内部状态过多且没有办法去操作和维护这些状态；函数没有明显返回或者参数过多；低内聚高耦合等等。

建议 76：使用 Pylint 检查代码风格
如果团队遵循 PEP8 编码风格，Pylint 是个不错的选择（还有其他选择，比如 pychecker、pep8 等）。Pylint 始于 2003 年，是一个代码分析工具，用于检查 Python 代码中的错误，查找不符合代码编码规范以及潜在的问题。支持不同的 OS 平台，如 Windows、Linux、OSX 等，特性如下：

代码风格审查。它以 Guido van Rossum 的 PEP8 为标准，能够检查代码的行长度，不符合规范的变量名以及不恰当的模块导入等不符合编码规范的代码

代码错误检查。如未被实现的接口，方法缺少对应参数，访问模块中未定义的变量等

发现重复以及设计不合理的代码，帮助重构。

高度的可配置化和可定制化，通过 pylintrc 文件的修改可以定义自己适合的规范。

支持各种 IDE 和编辑器集成。如 Emacs、Eclipse、WingIDE、VIM、Spyder 等

**能够基于 Python 代码生成 UML 图。**Pylint0.15 中就集成了 Pyreverse，能够轻易生成 UML 图形

能够与 Hudson、Jenkins 等持续集成工具相结合支持自动代码审查。

使用 Pylint 分析代码，输出分为两部分：一部分为源代码分析结果，第二部分为统计报告。报告部分主要是一些统计信息，总体来说有以下6 类：

Statistics by type：检查的模块、函数、类等数量，以及它们中存在文档注释以及不良命名的比例

Raw metrics：代码、注释、文档、空行等占模块代码量的百分比统计

Duplication：重复代码的统计百分比

Messages by category：按照消息类别分类统计的信息以及和上一次运行结果的对比

Messages：具体的消息 ID 以及它们出现的次数

Global evaluation：根据公式计算出的分数统计：10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)

我们来重点讨论一下源代码分析主要以消息的形式显示代码中存在的问题，消息以 MESSAGE_TYPE:LINE_NUM:[OBJECT:]MESSAGE 的形式输出，主要分为以下 5 类：

（C）惯例，违反了编码风格标准

（R）重构，写得非常糟糕的代码

（W）警告，某些 Python 特定的问题

（E）错误，很可能是代码中的 bug

（F）致命错误，阻止 Pylint 进一步运行的错误

比如如果信息输出 trailing-whitespace 信息，可以使用命令 pylint --help-msg="trailing-whitespace" 来查看，这里提示是行尾存在空格。

如果不希望对这类代码风格进行检查，可以使用命令行过滤掉这些类别的信息，比如 pylint -d C0303,W0312 BalancePoint.py。

Pylint 支持可配置化，如果在项目中希望使用统一的代码规范而不是默认的风格来进行代码检查，可以指定 --generate-rcfile 来生成配置文件。默认的 Pylintrc 可以在 Pylint 的目录 examples 中找到。如默认支持的变量名的正则表达式为：variable-rgx=[a-z_][a-z0-9_]{2,30}$，可以根据自己需要进行相应修改。其他配置如 reports 用于控制是否输出统计报告；max-module-lines 用于设置模块最大代码行数；max-line-length 用于设置代码行最大长度；max-args 用于设置函数的参数个数等。读者可自行查看 pylintrc 文件。

建议 77：进行高效的代码审查
建议 78：将包发布到 PyPI
可以是发布到官方的 PyPI 或者团队私有的 PyPI。这里先讲把包发布到官方的 PyPI，标准库 distutils 支持将包发布到 PyPI 的功能：

# 现在 PyPI 上注册一个用户
$ python setup.py register
# 注册包名
$ python setup.py register -n 
# 上传包
$ python setup.py sdist upload
第 8 章 性能剖析与优化
建议 79：了解代码优化的基本原则
代码优化是指在不改变程序运行结果的前提下使得程序运行的效率更高，优化的代码意味着代运行速度更快或者占用的资源更少。

优先保证代码是可工作的。

权衡优化的代价。

定义性能指标，集中力量解决首要问题。

不要忽略可读性。

建议 80：借助性能优化工具
常见的性能优化工具有 Psyco、Pypy 和 cPython 等。

Psyco：Psyco 是一个 just-in-time 的编译器，它能够在不改变源代码的情况下提高一定的性能，Psyco 将操作编译成部分优化的机器码，其操作分成三个不同的级别，有“运行时”、“编译时”和“虚拟时”变量，并根据需要提高和降低变量的级别。运行时变量只是常规 Python 解释器处理的原始字节码和对象结构。一旦 Psyco 将操作编译成机器码，那么编译时变量就会在机器寄存器和可直接访问的内存位置中表示。同时 Python 能高速缓存已编译的机器码以备以后重用，这样能节省一点时间。但 Psyco 也有其缺点，其本身所占内存较大。2012 年 Psyco 项目停止维护并正式结束，由 Pypy 所接替。

Pypy：Python 的动态编译器，是 Psyco 的后继项目。其目的是，做到 Psyco 没有做到的动态编译。Pypy 的实现分为两部分，第一部分“用 Python 实现的 Python”，实际上它是使用一个名为 RPython 的 Python 子集实现的，Pypy 能够将 Python 代码转成 C、.NET、Java 等语言和平台的代码；第二部分 Pypy 集成了一种编译 rPython 的即时（JIT）编译器，和许多编译器、解释器不同，这种编译器不关心 Python 代码的词法分析和语法树，所以它直接利用 Python 语言的 Code Object（Python 字节码的表示）。Pypy 直接分析 Python 代码所对应的字节码，这些字节码既不是以字符形式也不是以某种二进制格式保存在文件中。

建议 81：利用 cProfile 定位性能瓶颈
程序性能影响往往符合 80/20 法则，即 20% 的代码的运行时间占用了 80% 的总运行时间。

profile 是 Python 的标准库，可以统计程序里每一个函数的运行时间，并且提供了多样化的报表，而 cProfile 则是它的 C 实现版本，剖析过程本身需要消耗的资源更少。所以在 Python3 中，cProfile 代替了 profile，成为默认的性能剖析模块。

def foo():
    sum = 0
    for i in range(100):
        sum += i
    return sum
if __name__ == "__main__":
    import cProfile
    cProfile.run("foo()")
4 function calls in 0.000 seconds
Ordered by: standard name
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    0.000    0.000    0.000    0.000 <ipython-input-1-e5d41600b11d>:1(foo)
    1    0.000    0.000    0.000    0.000 <string>:1(<module>)
    1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
    1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
除了用这种方式，cProfile 还可以直接用 Python 解释器调用 cProfile 模块来剖析 Python 程序，如在命令行输入 python -m cProfile prof1.py结果和调用cProfile.run()一样。

cProfile 的统计结果分为 ncalls、tottime、percall、cumtime、percall、filename:lineno(function) 等若干列。

统计项意义ncalls函数的被调用次数tottime函数总计运行时间，不含调用的函数运行时间percall函数运行一次的平均时间，等于 tottime/ncallscumtime函数总计运行时间，含调用的函数运行时间percall函数运行一次的平均时间，等于 cumtime/ncallsfilename:lineno(function)函数所在的文件名、函数的行号、函数名

通常情况下，cProfile 的输出都直接输出到命令行，而且默认是按照文件名排序输出的。cProfile 简单地支持了一些需求，可以在 cProfile.run() 函数里再提供一个实参，就是保存输出的文件名。同样，在命令行参数里，也可以加多一个参数，用来保存 cProfile 的输出。

cProfile 解决了我们的对程序执行性能剖析的需求，但还有一个需求：以多种形式查看报表以便快速定位瓶颈。我们可以通过 pstats 模块的另一个类 Stats 来解决。Stats 的构造函数接受一个参数——就是 cProfile 的输出文件名。Status 提供了对 cProfile 输出结果进行排序、输出控制等功能。我们可以修改前文的程序：

if __name__ == "__main__":
    import cProfile
    cProfile.run("foo()", "prof.txt")
    import pstats
    p = pstats.Stats("prof.txt")
    p.sort_stats("time").print_stats()
Stats 有若干个函数，这些函数组合能输出不同的 cProfile 报表，功能非常强大，下面简单介绍一些：

函数函数的作用strip_dirs()用以除去文件名前面的路径信息add(filename,[...])把 profile 的输出文件加入 Stats 实例中统计dump_stats(filename)把 Stats 的统计结果保存到文件sort_stats(key, [...])把最重要的一个函数，用以排序 profile 的输出reverse_order()把 Stats 实例里的数据反序重排print_stats([restriction,...])把 Stats 报表输出到 stdoutprint_callers([restriction,...])输出调用了指定的函数的相关信息print_callees([restriction,...])输出指定的函数调用过的函数的相关信息

这里最重要的函数就是 sort_stats 和 print_stats，通过这两个函数我们几乎可以用适当的形式浏览所有的信息了。下面是详细介绍：

sort_stats() 接收一个或者多个字符串参数，如 time、name 等，表明要根据哪一列来排序。比如可以通过用 time 为 key 来排序得知最消耗时间的函数；也可以通过 cumtime 来排序，获知总消耗时间最多的函数。

参数意义ncalls被调用次数cumulative函数运行的总时间file文件名module模块名pcalls简单统计调用line行号name函数名nflName、file、linestdname标准函数名time函数内部运行时间

print_stats 输出最后一次调用 sort_stats 之后得到的报表。print_stats 有多个可选参数，用以筛选输出的数据。print_stats 的参数可以是数字也可以是 Perl 风格的正则表达式。

下面举一些例子：

# 将 stats 里的内容取前面 10%，然后再将包含 "foo:" 这个字符串的结果输出
print_stats(".1", "foo:")
# 将 stats 里的包含 "foo:" 字符串的内容的前 10% 输出
print_stats("foo:", ".1")
# 将 stats 里前 10 条数据输出
print_stats(10)
# profile 输出结果的时候相当于如下调用了 Stats 的函数
p.strip_dirs().sort_stats(-1).print_stats()
其中，sort_stats 函数的参数是 -1，这是为了与旧版本兼容而保留的。sort_stats 可以接受 -1、0、1、2 之一，这 4 个数分贝对应 "stdname"、"calls"、"time" 和 "cumulative"。但如果你使用了数字为参数，那么 pstats 只按照第一个参数进行排序，其他参数将被忽略。

除了编程接口外，pstats 还提供了友好的命令行交互环境，在命令行执行 python -m pstats 就可以进入交互环境，在交互环境里可以使用 read 或 add 指令读入或加载剖析结果文件， stats 指令用以查看报表，callees 和 callers 指令用以查看特定函数的被调用者和调用者。

如果我们想测试向 list 中添加一个元素需要多少时间，可以使用 timeit 模块：

class Timer([stmt="pass"[, setup="pass"[, timer=<time function>]]])
stmt 参数是字符串形式的一个代码段，这个代码段将被评测运行时间；

setup 参数用以设置 stmt 的运行环境；

timer 可以由用户使用自定义精度的计时函数。

timeit.Timer 有 3 个成员函数：

timeit([number=1000000]) ：timeit() 执行一次 Timer 构造函数中的 setup 语句之后，就重复执行 number 次 stmt 语句，然后返回总计运行消耗的时间；

repeat([repeat=3[, number=1000000]]) ：repeat() 函数以 number 为参数调用 timeit 函数 repeat 次，并返回总计运行消耗的时间；

print_exc([file=None]) ：print_exec() 函数以代替标准的 tracback，原因在于 print_exec() 会输出错行的源代码。

除了可以使用 timeit 的编程接口外，也可以在命令行里使用 timeit，非常方便：

python -m timeit [-n N] [-r N] [-s S] [-t] [-c] [-h] [statement ...]
其中参数的定义如下：

-n N/--number=N，statement 语句执行的次数

-r N/--repeat=N，重复多少次调用 timeit()，默认为 3

-s S/--setup=S，用以设置 statement 执行环境的语句，默认为 "pass"

-t/--time，计时函数，除了 Windows 平台外默认使用 time.time() 函数

-c/--clock，计时函数，Windows 平台默认使用 time.clock() 函数

-v/--verbose，输出更大精度的计时数值

-h/--help，简单的使用帮助

厉害：

python -m timeit "[].append(1)"
10000000 loops, best of 3: 0.116 usec per loop
建议 82：使用 memory_profiler 和 objgraph 剖析内存使用
Python 还提供了一些工具可以用来查看内存的使用情况以及追踪内存泄漏（如 memory_profiler、objgraph、cProfile、PySizer 及 Heapy 等），或者可视化地显示对象之间的引用（如 objgraph），从而为发现内存问题提供更直接的证据。我们来看看memory_profiler、objgraph两个工具的使用。

memory_profiler：在需要进行内存分析的代码之前用 @profile 进行装饰，然后运行命令 python -m memory_profiler 文件名 ，便可以输出每一行代码的内存使用以及增长情况。

Objgraph：

安装：pip install objgraph

功能分类：

统计，如 objgraph.count(typename[, objects]) 表示根据传入的参数显示被 gc 跟踪的对象的数目；objgraph.show_most_common_types([limit=10, objects]) 表示显示常用类型对应的对象的数目

定位和过滤对象，如 objgraph.by_type(typename[, objects]) 表示根据传入的参数显示被 gc 跟踪的对象信息；objgraph.at(addr) 表示根据给定的地址返回对象

遍历和显示对象图。如 objgraph.show_refs(objs[, max_depth=3, extra_ignore=(), filter=None, too_many=10, highlight=None, filename=None, extra_info=None, refcounts=False]) 表示从对象 objs 开始显示对象引用关系图；objgraph.show_backrefs(objs[, max_depth=3, extra_ignore=(), filter=None, too_many=10, highlight=None, filename=None, extra_info=None, refcounts=False]) 表示显示以 objs 的引用作为结束的对象关系图。

例子：

生成对象x的引用关系图：

>>> import objgraph
>>> x = ['a', '1', [2, 3]]
>>> objgraph.show_refs([x], filename="test.png")
显示常用类型不同类型对象的数目，限制输出前3行：

>>> objgraph.show_most_common_types(limit=3)
wrapper_descriptor            1031
function                    975
builtin_function_or_method    615
建议 83：努力降低算法复杂度
时间复杂度：

O(1) < O(log * n) < O(n) < O(n log n) < O(n^2) < O(c^n) < O(n!) < O(n^n)

常见数据结构基本操作时间复杂度：

建议 84：掌握循环优化的基本技巧
循环的优化应遵循的原则是尽量减少循环过程中的计算量，多重循环的情形下尽量将内层的计算提到上一层。

减少循环内部的计算：

# 每次循环都要重新计算
for i in range(iter):
    d = math.sqrt(y)
    j += i * d
# 高效率
d = math.sqrt(y)
for i in range(iter):
    j += i * d
将显式循环改为隐式循环：n * (n + 1) / 2，不必使用for循环计算，但要注意可读性

在循环中尽量引用局部变量，在命名空间中局部变量优先搜索，因此局部变量的查询会比全局变量要快，当在循环中需要多次引用某一个变量的时候，尽量将其转换为局部变量：

# 示例一
x = [10, 34, 56, 78]
def f(x):
    for i in range(len(x)):
        x[i] = math.sin(x[i])
    return x
# 示例二
def g(x):
    loc_sin = math.sin
    for i in range(len(x)):
        x[i] = loc_sin(x[i])
    return x
# 示例二比示例一性能更佳
关注内层嵌套循环，尽量将内层循环的计算往上层移：

# 示例一
for i in range(len(v1)):
    for j in range(len(v2)):
        x = v1[i] + v2[j]
# 示例二
for i in range(len(v1)):
    v1i = v1[i]
    for j in range(len(v2)):
        x = v1i + v2[j]
建议 85：使用生成器提高效率
放一张图来理解，来自这里



实际上当需要在循环过程中依次处理一个序列中的元素的时候，就应该考虑生成器。

当解释器执行遇到 yield 的时候，函数会自动返回 yield 语句之后的表达式的值。不过与 return 不同的是，yield 语句在返回的同时会保存所有的局部变量以及现场信息，以便在迭代器调用 next() 或 send() 方法的时候还原，而不是直接交给垃圾回收器（return() 方法返回后这些信息会被垃圾回收器处理）。

这样就能够保证对生成器的每一次迭代都会返回一个元素，而不是一次性在内存中生成所有的元素。自 Python2.5 开始，yield 语句变为表达式，可以直接将其值赋给其他变量。

生成器的优点总体来说有如下几条：

生成器提供了一种更为便利的产生迭代器的方式，用户一般不需要自己实现 iter 和 next 方法，它默认返回一个迭代器

代码更为简洁优雅

充分利用了延迟评估（Lazy evaluation）的特性，仅在需要的时候才产生对应的元素，而不是一次生成所有的元素，从而节省了内存空间，提高了效率，理论上无限循环成为了可能

使得协同程序更为容易实现。协同程序是有多个进入点，可以挂起恢复的函数，这基本就是 yield 的工作方式。Python2.5 之后生成器的功能更完善，加入了 send()、close() 和 throw() 方法。其中 send() 不仅可以传递值给 yield 语句，而且能够恢复生成器，因此生成器能大大简化协同程序的实现。

建议 86：使用不同的数据结构优化性能
如果 Python 中的查找、排序算法已经优化到极限，比如sort()使用 key 参数比使用cmp参数性能更高；那么首先应该考虑使用不同的数据结构优化性能。

list，它的内存管理类似 C++ 的 std::vector，即预先分配一定数量的”车位“，当预分配的内存用完时，又继续往里面插入元素，会启动新一轮的内存分配。

list 对象会根据内存增长算法申请一块更大的内存，然后将原有的所有元素拷贝过去，销毁之前的内存，再插入新元素。当删除元素时，也是类似，删除后发现已用空间比预分配空间的一半还少时，list 会另外申请一块小内存，再做一次元素拷贝，然后销毁原有的大内存。可见，如果 list 对象经常有元素数量的“巨变”，比如增加、删除得很频繁，那么应当考虑使用 deque。

deque 就是双端队列，同时具备栈和队列的特性，能够提供在两端插入和删除时复杂度为 O(1) 的操作。相对于 list，它最大的优势在于内存管理方面。如果不熟悉 C++ 的 std::deque，可以把 deque 想象为多个 list 连在一起，它的每一个 list 也可以存储多个元素。它的优势在于插入时，已有空间已经用完，那么它会申请一个新的内存空间来容纳新的元素，并将其与已有的其他内存空间串接起来，从而避免元素拷贝；在删除元素时也类似，无需移动元素。所以当元素数量巨变时，它的性能比 list 要好上许多倍。

对于 list 这种序列容器来说，除了 pop(0) 和 insert(0, v) 这种插入操作非常耗时之外，查找一元素是否在其中，也是 O(n) 的线性复杂度。在 C 语言中，标准库函数 bsearch() 能够通过二分查找算法在有序队列中快速查找是否存在某一元素。在 Python 中，对保持 list 对象有序以及在有序队列中查找元素有非常好的支持，这是通过标准库 bisect 来实现的。

bisect 并没有实现一种新的“数据结构”，其实它是用来维护“有序列表”的一组函数，可以兼容所有能够随机存取的序列容器，比如 list。它可使在有序列表中查找某一元素变得非常简单。

def index(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError
保持列表有序需要付出额外的维护工作，但如果业务需要在元素较多的列表中频繁查找某些元素是否存在或者需要频繁地有序访问这些元素，使用 bisect 则相当值得。

对于序列容器，除了插入、删除、查找之外，还有一种很常见的需求是获取其中的极大值或极小值元素，比如在查找最短路径的A*算法中就需要在Open表中快速找到预估值最小的元素。这时候，可以使用 heapq 模块。类似 bisect，heapq 也是维护列表的一组函数，其中 heapify() 的作用是把一个序列容器转化为一个堆。

In [1]: import heapq
In [2]: import random
In [3]: alist = [random.randint(0, 100) for i in range(10)]
In [4]: alist
Out[4]: [62, 72, 18, 55, 86, 26, 88, 21, 4, 97]
In [5]: heapq.heapify(alist)
In [6]: alist
Out[6]: [4, 21, 18, 55, 86, 26, 88, 72, 62, 97]
可以看到，转化为堆后，alist 的第一个元素 alist[0] 是整个列表中最小的元素，heapq 将保证这一点，从而保证从列表中获取最小值元素的时间复杂度是 O(1)

In [7]: heapq.heappop(alist)
Out[7]: 4
In [8]: alist
Out[8]: [18, 21, 26, 55, 86, 97, 88, 72, 62]
除了通过 heapify() 函数将一个列表转换为堆之外，也可以通过 heappush()、heappop() 函数插入、删除元素，针对常见的先插入新元素再获取最小元素、先获取最小元素再插入新元素的需求，还有 heappushpop(heap, item) 和 heapreplace(heap, item) 函数可以快速完成。另外可以看出，每次元素增减之后的序列变化很大，所以千万不要乱用 heapq，以免带来性能问题。

heapq 还有 3 个通用函数值得介绍，其中 merge() 能够把多个有序列表归并为一个有序列表（返回迭代器，不占用内存），而 nlargest() 和 nsmallest() 类似于 C++ 中的 std::nth_element()，能够返回无序列表中最大或最小的 n 个元素，并且性能比 sorted(iterable, key=key)[:n] 要高。

除了对容器的操作可能会出现性能问题外，容器中存储的元素也有很大的优化空间，这是因为在很多业务中，容器存储的元素往往是同一类型的，比如都是整数，而且整数的取值范围也确定，此时就可以用 array 优化程序性能。

array 实例化的时候需要指定其存储的元素类型，如c，表示存储的每个人元素都相当于C语言中的 char 类型，占用内存大小为 1 字节。

建议 87：充分利用 set 的优势
Python 中集合是通过 Hash 算法实现的无序不重复的元素集。



我们来做一些测试：

$ python -m timeit -n 1000 "[x for x in range(1000) if x in range(600, 1000)]"
1000 loops, best of 3: 6.44 msec per loop
$ python -m timeit -n 1000 "set(range(100)).intersection(range(60, 100))"   
1000 loops, best of 3: 9.18 usec per loop
实际上 set 的 union、intersection、difference 等操作要比 list 的迭代要快。因此如果涉及求 list 交集、并集或者差等问题可以转换为 set 来操作。

建议 88：使用 multiprocess 克服 GIL 的缺陷
多进程 Multiprocess 是 Python 中的多进程管理包，在 Python2.6 版本中引进的，主要用来帮助处理进程的创建以及它们之间的通信和相互协调。它主要解决了两个问题：一是尽量缩小平台之间的差异，提供高层次的 API 从而使得使用者忽略底层 IPC 的问题；二是提供对复杂对象的共享支持，支持本地和远程并发。

类 Process 是 multiprocess 中较为重要的一个类，用户创建进程，其构造函数如下：

Process([group[, target[, name[, args[, kwargs]]]]])

其中，参数 target 表示可调用对象；args 表示调用对象的位置参数元组；kwargs 表示调用对象的字典；name 为进程的名称；group 一般设置为 None。该类提供的方法与属性基本上与 threading.Thread 一致，包括 is_alive()、join([timeout])、run()、start()、terminate()、daemon（要通过 start() 设置）、exitcode、name、pid 等。

不同于线程，每个进程都有其独立的地址空间，进程间的数据空间也相互独立，因此进程之间数据的共享和传递不如线程来得方便。庆幸的是 multiprocess 模块中都提供了相应的机制：如进程间同步操作原语 Lock、Event、Condition、Semaphore，传统的管道通信机制 pipe 以及队列 Queue，用于共享资源的 multiprocess.Value 和 multiprocess.Array 以及 Manager 等。

Multiprocessing 模块在使用上需要注意以下几个要点：

进程之间的的通信优先考虑 Pipe 和 Queue，而不是 Lock、Event、Condition、Semaphore 等同步原语。进程中的类 Queue 使用 pipe 和一些 locks、semaphores 原语来实现，是进程安全的。该类的构造函数返回一个进程的共享队列，其支持的方法和线程中的 Queue 基本类似，除了方法 task_done()和 join() 是在其子类 JoinableQueue 中实现的以外。需要注意的是，由于底层使用 pipe 来实现，使用 Queue 进行进程之间的通信的时候，传输的对象必须是可以序列化的，否则 put 操作会导致 PicklingError。此外，为了提供 put 方法的超时控制，Queue 并不是直接将对象写到管道中而是先写到一个本地的缓存中，再将其从缓存中放入 pipe 中，内部有个专门的线程 feeder 负责这项工作。由于 feeder 的存在，Queue 还提供了以下特殊方法来处理进程退出时缓存中仍然存在数据的问题。

close()：表明不再存放数据到 queue 中。一旦所有缓冲的数据刷新到管道，后台线程将退出。

join_thread()：一般在 close 方法之后使用，它会阻止直到后台线程退出，确保所有缓冲区中的数据已经刷新到管道中。

cancel_join_thread()：需要立即退出当前进程，而无需等待排队的数据刷新到底层管道的时候可以使用该方法，表明无须阻止到后台进程的退出。

Multiprocessing 中还有个 SimpleQueue 队列，它是实现了锁机制的 pipe，内部去掉了 buffer，但没有提供 put 和 get 的超时处理，两个动作都是阻塞的。

除了 multiprocessing.Queue 之外，另一种很重要的通信方式是 multiprocessing.Pipe。它的构造函数为 multiprocess.Pipe([duplex])，其中 duplex 默认为 True，表示为双向管道，否则为单向。它返回一个 Connection 对象的组（conn1, conn2），分别表示管道的两端。Pipe 不支持进程安全，因此当有多个进程同时对管道的一端进行读操作或者写操作的时候可能会导致数据丢失或者损坏。因此在进程通信的时候，如果是超过 2 个以上的线程，可以使用 queue，但对于两个进程之间的通信而言 Pipe 性能更快。

from multiprocessing import Process, Pipe, Queue
import time
def reader_pipe(pipe):
    output_p, input_p = pipe    # 返回管道的两端
    inout_p.close()
    while True:
        try:
            msg = output_p.recv()    # 从 pipe 中读取消息
        except EOFError:
                break
def writer_pipe(count, input_p):    # 写消息到管道中
    for i in range(0, count):
        input_p.send(i)                # 发送消息
def reader_queue(queue):            # 利用队列来发送消息
    while True:
        msg = queue.get()            # 从队列中获取元素
        if msg == "DONE":
            break
def writer_queue(count, queue):
    for ii in range(0, count):
        queue.put(ii)                # 放入消息队列中
    queue.put("DONE")
if __name__ == "__main__":
    print("testing for pipe:")
    for count in [10 ** 3, 10 ** 4, 10 ** 5]:
        output_p, input_p = Pipe()
        reader_p = Process(target=reader_pipe, args=((output_p, input_p),))
        reader_p.start()            # 启动进程
        output_p.close()
        _start = time.time()
        writer_pipe(count, input_p)    # 写消息到管道中
        input_p.close()
        reader_p.join()                # 等待进程处理完毕
        print("Sending {} numbers to Pipe() took {} seconds".format(count, (time.time() - _start)))
    print("testsing for queue:")
    for count in [10 ** 3, 10 ** 4, 10 ** 5]:
        queue = Queue()                # 利用 queue 进行通信
        reader_p = Process(target=reader_queue, args=((queue),))
        reader_p.daemon = True
        reader_p.start()
        _start = time.time()
        writer_queue(count, queue)    # 写消息到 queue 中
        reader_p.join()
        print("Seding {} numbers to Queue() took {} seconds".format(count, (time.time() - _start)))
上面代码分别用来测试两个多线程的情况下使用 pipe 和 queue 进行通信发送相同数据的时候的性能，从函数输出可以看出，pipe 所消耗的时间较小，性能更好。

尽量避免资源共享。相比于线程，进程之间资源共享的开销较大，因此要尽量避免资源共享。但如果不可避免，可以通过 multiprocessing.Value 和 multiprocessing.Array 或者 multiprocessing.sharedctpyes 来实现内存共享，也可以通过服务器进程管理器 Manager() 来实现数据和状态的共享。这两种方式各有优势，总体来说共享内存的方式更快，效率更高，但服务器进程管理器 Manager() 使用起来更为方便，并且支持本地和远程内存共享。

# 示例一
import time
from multiprocessing import Process, Value
def func(val):    # 多个进程同时修改 val
    for i in range(10):
        time.sleep(0.1)
        val.value += 1
if __name__ == "__main__":
    v = Value("i", 0)    # 使用 value 来共享内存
    processList = [Process(target=func, args=(v,)) for i in range(10)]
    for p in processList: p.start()
    for p in processList: p.join()
    print v.value
# 修改 func 函数，真正控制同步访问
def func(val):
    for i in range(10):
        time.sleep(0.1)
        with val.get_lock():    # 仍然需要使用 get_lock 方法来获取锁对象
            val.value += 1
# 示例二
import multiprocessing
def f(ns):
    ns.x.append(1)
    ns.y.append("a")
if __name__ == "__main__":
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.x = []    # manager 内部包括可变对象
    ns.y = []
    print("before process operation: {}".format(ns))
    p = multiprocessing.Process(target=f, args=(ns,))
    p.start()
    p.join()
    print("after process operation {}".format(ns))    # 修改根本不会生效
# 修改
import multiprocessing
def f(ns, x, y):
    x.append(1)
    y.append("a")
    ns.x = x    # 将可变对象也作为参数传入
    ns.y = y
if __name__ == "__main__":
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    ns.x = []    # manager 内部包括可变对象
    ns.y = []
    print("before process operation: {}".format(ns))
    p = multiprocessing.Process(target=f, args=(ns, ns.x, ns.y))
    p.start()
    p.join()
    print("after process operation {}".format(ns))
注意平台之间的差异。由于 Linux 平台使用 fork() 来创建进程，因此父进程中所有的资源，如数据结构、打开的文件或者数据库的连接都会在子进程中共享，而 Windows 平台中父子进程相对独立，因此为了更好地保持平台的兼容性，最好能够将相关资源对象作为子进程的构造函数的参数传递进去。要避免如下方式：

f = None
def child(f):
    # do something
if __name__ == "__main__":
    f = open(filename, mode)
    p = Process(target=child)
    p.start()
    p.join()
# 推荐的方式
def child(f):
    print(f)
if __name__ == "__main__":
    f = open(filename, mode)
    p = Process(target=child, args=(f, ))    # 将资源对象作为构造函数参数传入
    p.start()
    p.join()
需要注意的是，Linux 平台上 multiprocessing 的实现是基于 C 库中的 fork()，所有子进程与父进程的数据是完全相同，因此父进程中所有的资源，如数据结构、打开的文件或者数据库的连接都会在子进程中共享。但 Windows 平台上由于没有 fork() 函数，父子进程相对独立，因此保持了平台的兼容性，最好在脚本中加上 if name == "main" 的判断，这样可以避免出现 RuntimeError 或者死锁。

尽量避免使用 terminate() 方式终止进程，并且确保 pool.map 中传入的参数是可以序列化的。

import multiprocessing
def unwrap_self_f(*args, **kwargs):
    return calculate.f(*args, **kwargs)    # 返回一个对象
class calculate(object):
    def f(self, x):
        return x * x
    def run(self):
        p = multiprocessing.Pool()
        return p.map(unwrap_self_f, zip([self] * 3, [1, 2, 3]))
if __name__ == "__main__":
    c1 = calculate()
    print(c1.run())
建议 89：使用线程池提高效率
我们知道线程的生命周期分为 5 个状态：创建、就绪、运行、阻塞和终止。自线程创建到终止，线程便不断在运行、就绪和阻塞这 3 个状态之间转换直至销毁。而真正占有 CPU 的只有运行、创建和销毁这 3 个状态。一个线程的运行时间由此可以分为 3 部分：线程的启动时间（Ts）、线程体的运行时间（Tr）以及线程的销毁时间（Td）。在多线程处理的情境中，如果线程不能够被重用，就意味着每次创建都需要经过启动、销毁和运行这 3 个过程。这必然会增加系统的相应时间，降低效率。而线程体的运行时间 Tr 不可控制，在这种情况下要提高线程运行的效率，线程池便是一个解决方案。

线程池通过实现创建多个能够执行任务的线程放入池中，所要执行的任务通常被安排在队列中。通常情况下，需要处理的任务比线程的数目要多，线程执行完当前任务后，会从队列中取下一个任务，直到所有的任务已经完成。

由于线程预先被创建并放入线程池中，同时处理完当前任务之后并不销毁而是被安排处理下一个任务，因此能够避免多次创建线程，从而节省线程创建和销毁的开销，带来更好的性能和系统稳定性。线程池技术适合处理突发性大量请求或者需要大量线程来完成任务、但任务实际处理时间较短的应用场景，它能有效避免由于系统中创建线程过多而导致的系统性能负载过大、响应过慢等问题。

Python 中利用线程池有两种解决方案：一是自己实现线程池模式，二是使用线程池模块。

先来看一个线程池模式的简单实现：线程池代码

自行实现线程，需要定义一个 Worker 处理工作请求，定义 WorkerManager 来进行线程池的管理和创建，它包含一个工作请求队列和执行结果队列，具体的下载工作通过 download_file 方法实现。

相比自己实现的线程池模型，使用现成的线程池模块往往更简单。Python 中线程池模块的下载地址。该模块提供了以下基本类和方法：

threadpool.ThreadPool：线程池类，主要的作用是用来分派任务请求和收集运行结果。主要有以下方法：

init(self, num_workers, q_size=0, resq_size=0, poll_timeout=5)：建立线程池，并启动对应 num_workers 的线程；q_size 表示任务请求队列的大小，resq_size 表示存放运行结果队列的大小。

createWorkers(self, num_workers, poll_timeout=5)：将 num_workers 数量对应的线程加入线程池中。

dismissWorkers(self, num_workers, do_join=False)：告诉 num_workers 数量的工作线程当执行完当前任务后退出

joinAllDismissedWorkers(self)：在设置为退出的线程上执行 Thread.join

putRequest(self, request, block=True, timeout=None)：将工作请求放入队列中

poll(self, block=False)：处理任务队列中新的请求wait(self)：阻塞用于等待所有执行结果。注意当所有执行结果返回后，线程池内部的线程并没有销毁，而是在等待新的任务。因此，wait() 之后仍然可以再次调用 pool.putRequests()往其中添加任务

threadpool.WorkRequest：包含有具体执行方法的工作请求类

threadpool.WorkerThread：处理任务的工作线程，主要有 run() 方法以及 dismiss() 方法。

makeRequests(callable_, args_list, callback=None, exec_callback=_handle_thread_exception)：主要函数，作用是创建具有相同的执行函数但参数不同的一系列工作请求。

再来看一个线程池实现的例子：

import urllib2
import os
import time
import threadpool
def download_file(url):
    print("begin download {}".format(url ))
    urlhandler = urllib2.urlopen(url)
    fname = os.path.basename(url) + ".html"
    with open(fname, "wb") as f:
        while True：
            chunk = urlhandler.read(1024)
            if not chunk:
                break
            f.write(chunk)
urls = ["http://wiki.python.org/moni/WebProgramming",
       "https://www.createspace.com/3611970",
       "http://wiki.python.org/moin/Documention"]
pool_size = 2
pool = threadpool.ThreadPool(pool_size)    # 创建线程池，大小为 2
requests = threadpool.makrRequests(download_file, urls)    # 创建工作请求
[pool.putRequest(req) for req in requests]
print("putting request to pool")
pool.putRequest(threadpool.WorkRequest(download_file, args=["http://chrisarndt.de/projects/threadpool/api/",]))    # 将具体的请求放入线程池
pool.putRequest(threadpool.WorkRequest(download_file, args=["https://pypi.python.org/pypi/threadpool",]))
pool.poll()    # 处理任务队列中的新的请求
pool.wait()
print("destory all threads before exist")
pool.dismissWorkers(pool_size, do_join=True)    # 完成后退出
建议 90：使用 C/C++ 模块扩展高性能
Python 具有良好的可扩展性，利用 Python 提供的 API，如宏、类型、函数等，可以让 Python 方便地进行 C/C++ 扩展，从而获得较优的执行性能。所有这些 API 却包含在 Python.h 的头文件中，在编写 C 代码的时候引入该头文件即可。

来看一个简单的例子：

1、先用 C 实现相关函数，实现素数判断，也可以直接使用 C 语言实现相关函数功能后再使用 Python 进行包装。

#include "Python.h"
static PyObject * pr_isprime(PyObject, *self, PyObject * args) {
  int n, num;
  if (!PyArg_ParseTuple(args, "i", &num))    // 解析参数
    return NULL;
  if (num < 1) {
    return Py_BuildValue("i", 0);    // C 类型的数据结构转换成 Python 对象
  }
  n = num - 1;
  while (n > 1) {
    if (num % n == 0) {
      return Py_BuildValue("i", 0);
      n--;
    }
  }
  return Py_BuildValue("i", 1);
}
static PyMethodDef PrMethods[] = {
  {"isPrime", pr_isprime, METH_VARARGS, "check if an input number is prime or not."},
  {NULL, NULL, 0, NULL}
};
void initpr(void) {
  (void) Py_InitModule("pr", PrMethods);
}
上面的代码包含以下 3 部分：

导出函数：C 模块对外暴露的接口函数 pr_isprime，带有 self 和 args 两个参数，其中参数 args 中包含了 Python 解释器要传递给 C 函数的所有参数，通常使用函数 PyArg_ParseTuple() 来获得这些参数值

初始化函数：以便 Python 解释器能够对模块进行正确的初始化，初始化时要以 init 开头，如 initp

方法列表：提供给外部的 Python 程序使用的一个 C 模块函数名称映射表 PrMethods。它是一个 PyMethodDef 结构体，其中成员依次表示方法名、导出函数、参数传递方式和方法描述。看下面的例子：

 struct PyMethodDef {
    char * m1_name;        // 方法名
    PyCFunction m1_meth;    // 导出函数
    int m1_flags;            // 参数传递方法
    char * m1_doc;        // 方法描述
 }
参数传递方法一般设置为 METH_VARARGS，如果想传入关键字参数，则可以将其与 METH_KEYWORDS 进行或运算。若不想接受任何参数，则可以将其设置为 METH_NOARGS。该结构体必须与 {NULL, NULL, 0, NULL} 所表示的一条空记录来结尾。

2、编写 setup.py 脚本。

from distutils.core import setup, Extension
module = Extension("pr", sources=["testextend.c"])
setup(name="Pr test", version="1.0", ext_modules=[module])
3、使用 python setup.py build 进行编译，系统会在当前目录下生成一个 build 子目录，里面包含 pr.so 和 pr.o 文件。

4、将生成的文件 py.so 复制到 Python 的 site_packages 目录下，或者将 pr.so 所在目录的路径添加到 sys.path 中，就可以使用 C 扩展的模块了。

更多关于 C 模块扩展的内容请读者参考 。

建议 91：使用 Cython 编写扩展模块
Python-API 让大家可以方便地使用 C/C++ 编写扩展模块，从而通过重写应用中的瓶颈代码获得性能提升。但是，这种方式仍然有几个问题：

掌握 C/C++ 编程语言、工具链有巨大的学习成本

即便是 C/C++ 熟手，重写代码也有非常多的工作，比如编写特定数据结构、算法的 C/C++ 版本，费时费力还容易出错

所以整个 Python 社区都在努力实现一个 ”编译器“，它可以把 Python 代码直接编译成等价的 C/C++ 代码，从而获得性能提升，如 Pyrex、Py2C 和 Cython 等。而从 Pyrex 发展而来的 Cython 是其中的集大成者。

Cython 通过给 Python 代码增加类型声明和直接调用 C 函数，使得从 Python 代码中转换的 C 代码能够有非常高的执行效率。它的优势在于它几乎支持全部 Python 特性，也就是说，基本上所有的 Python 代码都是有效的 Cython 代码，这使得将 Cython 技术引入项目的成本降到最低。除此之外，Cython 支持使用 decorator 语法声明类型，甚至支持专门的类型声明文件，以使原有的 Python 代码能够继续保持独立，这些特性都使得它得到广泛应用，比如 PyAMF、PyYAML 等库都使用它编写自己的高效率版本。

# 安装
$ pip install -U cython
# 生成 .c 文件
$ cython arithmetic.py
# 提交编译器
$ gcc -shared -pthread -fPIC -fwrapv -02 -Wall -fno-strict-aliasing -I /usr/include/python2.7 -o arithmetic.so arithmetic.c
# 这时生成了 arithmetic.so 文件
# 我们就可以像 import 普通模块一样使用它
每一次都需要编译、等待有点麻烦，所以 Cython 很体贴地提供了无需显式编译的方案：pyximport。只要将原有的 Python 代码后缀名从 .py 改为 .pyx 即可。

$ cp arithmetic.py arithmetic.pyx
$ cd ~
$ python
>>> import pyximport; pyximport.install()
>>> import arithmetic
>>> arithmetic.__file__
从 file 属性可以看出，这个 .pyx 文件已经被编译链接为共享库了，pyximport 的确方便啊！

接下来我们看看 Cython 是如何提升性能的。

在 GIS 中，经常需要计算地球表面上两点之间的距离：

import math
def great_circle(lon1, lat1, lon2, lat2):
    radius = 3956    # miles
    x = math.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos(math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta))
    return radius * c
接下来尝试 Cython 进行改写：

import math
def great_circle(float lon1, float lat1, float lon2, float lat2):
    cdef float radius = 3956.0
    cdef float pi = 3.14159265
    cdef float x = pi / 180.0
    cdef float a, b, theta, c
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos(math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta))
    return radius * c
通过给 great_circle 函数的参数、中间变量增加类型声明，Cython 代码业务逻辑代码一行没改。使用 timeit 库可以测定提速将近 2 成，说明类型声明对性能提升非常有帮助。这时候，还有一个性能瓶颈，调用的 math 库是一个 Python 库，性能较差，可以直接调用 C 函数来解决：

cdef extern from "math.h":
    float cosf(float theta)
    float sinf(float theta)
    float acosf(float theta)
def greate_circle(float lon1, float lat1, float lon2, float lat2):
    cdef float radius = 3956.0
    cdef float pi = 3.14159265
    cdef float x = pi / 180.0
    cdef float a, b, theta, c
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = acosf((cosf(a) * cosf(b)) + (sinf(a) * sinf(b) * cosf(theta)))
    return radius * c
Cython 使用 cdef extern from 语法，将 math.h 这个 C 语言库头文件里声明的 cofs、sinf、acosf 等函数导入代码中。因为减少了 Python 函数调用和调用时产生的类型转换开销，使用 timeit 测试这个版本的代码性能提升了 5 倍有余。

通过这个例子，可以掌握 Cython 的两大技能：类型声明和直接调用 C 函数。比起直接使用 C/C++ 编写扩展模块，使用 Cython 的方法方便得多。

