# -*- coding:utf-8 -*-
# 用途： 生成斐波那契数列
# 创建日期: 19-6-20 下午11:46
import time


def make_fib_func():
    a, b = 1, 1
    def gen_fib():
        global a, b
        a, b = b, a + b
        return b
    return gen_fib


if __name__ == "__main__":
    start_t = time.time()

    pass

    print("use time: %s" % (time.time() - start_t))