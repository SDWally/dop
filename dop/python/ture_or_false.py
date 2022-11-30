# -*- coding:utf-8 -*-
# Python中一些语法特性的真假识别


def p1():
    t1 = (1, 2, 3)
    t2 = (1, 2, 3)
    t3 = tuple(t1)
    t4 = t1[:]
    print(t2 is t1)
    print(t3 is t1)
    print(t4 is t1)
    return


def p2():
    t1 = (1, 2, 3)
    t3 = tuple(t1)


if __name__ == '__main__':

    pass
