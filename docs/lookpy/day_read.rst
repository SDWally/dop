日常阅读
++++++++

《Python高性能编程》

Python访问变量的过程
--------------------

首先查找locals()数组，这是唯一不需要字典查询的部分，而是保存在一个极小的数组中。

然后搜索globals()字典，

最后搜索　__builtin__对象（其实是搜索这个模块的locals()字典）

从一个模块中显示导入函数，可以增加可读性，还可以加速代码。

高频率调用的外部变量，可以通过本地化进行加速。

range方法的实现（2.7）
--------------------

创建一个空列表，依次append每个范围内元素，返回整个列表。

如何将一个列表变成迭代器
--------------------
使用iter()函数即可。

如何知道其中有多少个数字可以被３整除
-------------------------------

::

    divisible_by_three = sum((1 for n in list_of_numbers if n % 3 == 0))

线程安全的一种实现方式
--------------------
::

    import threading
    context = threading.local()


    def get_algo_instance():
        return getattr(context, 'algorithm', None)


    def set_algo_instance(algo):
        context.algorithm = algo

一种类特性
----------
::

    class classproperty(object):
        """Class property
        """
        def __init__(self, fget):
            self.fget = fget

        def __get__(self, instance, owner):
            return self.fget(owner)


