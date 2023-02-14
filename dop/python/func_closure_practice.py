# -*- coding:utf-8 -*-

# 学习参考 the closure in python
# 计算移动平均数的高阶函数


def make_average():
    """

    :return:
    >>> avg = make_average()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0
    """
    series = []

    def average(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)

    return average()
