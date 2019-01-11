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

主动计算

class Asset:

    def __init__(self):
        self._money = 0
        self._market_money = 0
        self._total = 0
        
    def add_money(self, money):
        self._money += money
        self._update_total()
        
    def total(self):
        return self._total

    def _update_total(self):
        self._total = self._money + self._market_money


被动计算

::

class Asset:

    def __init__(self):
        self._money = 0
        self._market_money = 0
        self._total = 0
        
    def add_money(self, money):
        self._money += money
        
    @property
    def total(self):
        self._total = self._money + self._market_money
        return self._total
    
对于主动计算与被动计算的处理：

主动计算变被动计算
~~~~~~~~~~~~~~~~~~

对于一些频繁更新的值，如果要引起比较大的其他相关的变量的值的变化，然后又有一定的计算量，但是计算结果又不会每次都必要。
则可以优化为被动计算，仅当需要该值时，再行计算并更新。

被动计算变主动计算
~~~~~~~~~~~~~~~~~~

对于一些需要及时相应的值的计算，需要在值更新时，直接进行主动计算，而后再获取最新值时，便可以不经过计算，直接进行响应。满足时效要求。
