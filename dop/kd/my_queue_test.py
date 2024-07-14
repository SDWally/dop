# -*- coding: UTF-8 -*-
import unittest
from my_queue import binary_search_insertion_index


class SearchTest(unittest.TestCase):

    def test_check_one(self):
        # 示例使用
        arr = [1, 3, 5, 7, 9]
        target = 10
        insertion_index = binary_search_insertion_index(arr, target)

        print(f"元素 {target} 应该插入到列表中的位置是: {insertion_index}")
        if insertion_index == len(arr):
            pass
        elif arr[insertion_index] == target:
            del arr[insertion_index]
        print(arr)