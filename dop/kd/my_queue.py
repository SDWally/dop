# -*- coding: UTF-8 -*-

def binary_search_insertion_index(arr: list, target: int):
    """
    二分查找，确定待插入元素的索引

    Parameters
    ----------
    arr: 待查询的单调递增序列
    target: 待插入目标值
    """
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


class MyQueue:
    def __init__(self, lifetime: int):
        self.lifetime = lifetime
        self.data_list = []
        self.lifetime_list = []

    def _check_lifetime(self, timestamp: int):
        """
        自动弹出存在时间超过lifetime的元素

        Parameters
        ----------
        timestamp: 当前的时间戳，以纳秒记，严格单调递增
        """
        valid_timestamp = timestamp - self.lifetime
        # 二分查找，快速确定已超时元素索引区间并进行切片
        insertion_index = binary_search_insertion_index(self.lifetime_list, valid_timestamp)
        self.data_list = self.data_list[insertion_index:]
        self.lifetime_list = self.lifetime_list[insertion_index:]

    def push(self, timestamp: int, id: int):
        """
        插入队列

        Parameters
        ----------
        timestamp: 当前的时间戳，以纳秒记，严格单调递增
        id: 当前入队的元素id
        """
        if len(self.data_list) > 0:
            self._check_lifetime(timestamp)
        self.data_list.append(id)
        self.lifetime_list.append(timestamp)

    def query_length(self, timestamp: int) -> int:
        """
        查询队列当前长度

        Parameters
        ----------
        timestamp: 当前的时间戳，以纳秒记，严格单调递增
        """
        if len(self.data_list) > 0:
            self._check_lifetime(timestamp)
        return len(self.data_list)

    def remove(self, id: int):
        """
        删除指定id的元素（如果这个元素还在队列内的话）

        Parameters
        ----------
        id: 要删除的元素id
        """
        # 二分查找，当返回的索引值不为元素长度（防止索引越界）且查询后的元素值与目标值相等，执行删除
        insertion_index = binary_search_insertion_index(self.data_list, id)
        if insertion_index != len(self.data_list) and self.data_list[insertion_index] == id:
            del self.data_list[insertion_index]
            del self.lifetime_list[insertion_index]
