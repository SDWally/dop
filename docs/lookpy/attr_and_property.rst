Python中的属性与特性
+++++++++++++++++++++

属性
------

属性一般为类内部的属性。包含四种操作：create, set, get, delete.

::

    >>> class Example:
    ...     pass
    >>> e = Example()
    >>> e.attribute = "value"
    >>> e.attribute
    'value'
    >>> del e.attribute

获取或删除一个未赋值属性会引发异常.

使用types.SimpleNamespace 类创建实例，可以直接赋值。

    >>> import types
    >>> n = types.SimpleNamespace()
    >>> n.attribute = "value"
    >>> n.attribute
    'value'
    
非封装属性示例
---------------

::

    class Person:
        name = 'tom'              # 类中特性

        def get_name(self):        # 通过访问器方法访问特性
            return self.name

        def set_name(self, value): # 通过访问器方法改变特性
            self.name = value
            
特性
-------
对属性的封装方式

封装方式一：

::

    class Person:
        name = 'yoda'              # 类中特性

        def get_name(self):        # 通过访问器方法访问特性
            return self.name

        def set_name(self, value): # 通过访问器方法改变特性
            self.name = value

        person = property(get_name,set_name)
        
封装方式二：

::

    class Person:
        def __init__(self):
            self.name = 'yoda'
          
        @property
        def person(self):
            return self.name
            
        @person.setter
        def person(self,value):
            self.name = value

对于只读特性，则不需要设计setter即可。

经过特性封装，可以使得外部无法直接改变该属性的值，减少预期外的错误操作。

特性与主动计算、被动计算
-----------------------
