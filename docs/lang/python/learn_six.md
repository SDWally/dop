# six包与py2/py3的兼容性

Six provides simple utilities for wrapping over differences between Python 2 and Python 3.

使用示例
++++++++


判断所用Python的版本
--------------------
::

    >>> from six import PY2, PY3
    >>> PY2
    False
    >>> PY3
    True

类型判断
--------
::

    >>> from six import class_types, integer_types, string_types, text_types, binary_types
    >>> a = 1
    >>> isinstance(a, class_types)
    False
    >>> isinstance(a, integer_types)
    True

面向对象兼容性
-------------

绑定方法的处理
::

    >>> from six import get_unbound_function, get_method_function, get_method_self, get_function_closure, get_function_code, get_function_defaults

字典处理
::

    >>> from six import iterkeys, itervalues, iteritems, iterlists, viewkeys, viewvalues, viewitems

语法兼容性
----------

::

    >>> from six import exec_, print_, raise_from, reraise, with_metaclass, add_metaclass

字符串兼容性
-----------

::

    >>> from six import b, u, unichr, int2byte, byte2int, indexbytes, iterbytes, StringIO, BytesIO, python_2_unicode_compatible


一些包和属性的重命名
------------------

::

    >>> from six.moves import html_parser, reload_module, cPickle


更多重命名的信息，请参考　https://six.readthedocs.io/#module-six.moves
