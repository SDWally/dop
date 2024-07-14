# -*- coding: UTF-8 -*-
import unittest
from .broker_v1 import Broker
import time
import pandas as pd


class SearchTest(unittest.TestCase):

    def test_broker(self):
        start_time = time.time()
        with open("F:\source\dop\dop\kd\project\order.csv", "r") as f:
            text_str = f.read()
        line_list = text_str.split()
        order_list = [line.split(",") for line in line_list[1:]]
        # print(order_list)
        broker_ins = Broker()
        n = 0
        for order in order_list:
            broker_ins.transact(tuple(order))
            print(broker_ins.order_book(1))

        use_time = time.time() - start_time
        print(use_time)
