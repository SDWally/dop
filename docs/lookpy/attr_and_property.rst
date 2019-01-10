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