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


定义接口
--------
::

    import abc

    from six import with_metaclass

　　　class AbstractAccount(with_metaclass(abc.ABCMeta)):

新语法
------

@object.__new__

一个上下文管理器
--------------

这个管理器可以实现，在执行一个动作的时候，可以在执行动作之前和之后，分别执行别的动作。

::

    class CallbackManager(object):
        """Create a context manager from a pre-execution callback and a
        post-execution callback.

        Parameters
        ----------
        pre : (...) -> any, optional
            A pre-execution callback. This will be passed ``*args`` and
            ``**kwargs``.
        post : (...) -> any, optional
            A post-execution callback. This will be passed ``*args`` and
            ``**kwargs``.

        Notes
        -----
        The enter value of this context manager will be the result of calling
        ``pre(*args, **kwargs)``

        Examples
        --------
        >>> def pre(where):
        ...     print('entering %s block' % where)
        >>> def post(where):
        ...     print('exiting %s block' % where)
        >>> manager = CallbackManager(pre, post)
        >>> with manager('example'):
        ...    print('inside example block')
        entering example block
        inside example block
        exiting example block

        These are reusable with different args:
        >>> with manager('another'):
        ...     print('inside another block')
        entering another block
        inside another block
        exiting another block
        """
        def __init__(self, pre=None, post=None):
            self.pre = pre if pre is not None else _nop
            self.post = post if post is not None else _nop

        def __call__(self, *args, **kwargs):
            return _ManagedCallbackContext(self.pre, self.post, args, kwargs)

        # special case, if no extra args are passed make this a context manager
        # which forwards no args to pre and post
        def __enter__(self):
            return self.pre()

        def __exit__(self, *excinfo):
            self.post()


    class _ManagedCallbackContext(object):
        def __init__(self, pre, post, args, kwargs):
            self._pre = pre
            self._post = post
            self._args = args
            self._kwargs = kwargs

        def __enter__(self):
            return self._pre(*self._args, **self._kwargs)

        def __exit__(self, *excinfo):
            self._post(*self._args, **self._kwargs)


