# -*- coding:utf-8 -*-
# 一个指标计算的框架，支持计算不同资产、不同频率、周期（period）的指标；例如 基金、股票近1年日累计收益率、近1年周度累计收益率等。

class Operator:

    def total_ret(self, daily_ret):
        """
        累计收益率指标
        daily_ret: np.array, daily return
        return np.float32 total return
        """
        pass

    def max_draw(self, daily_ret):
        """
        最大回撤指标
        daily_ret: np.array, daily return
        return np.float32 max draw
        """
        pass

    def sample(self, daily_ret, periods):
        """
        周期采样
        """
        return

    def cut_recently(self, daily_ret, freqs):
        """
        频率剪切
        """
        return


class IndicatorModel:

    def __init__(self, operator):
        self.operator = operator

    def cal(self, daily_ret, freqs, periods, indicator_classes):
        """
        daily_ret: np.array, daily return
        freqs: list, ['1d', '1w', '1m', '1季度', '1y', '3y', '5y']
        periods: list, ['d', 'w', 'm', '季度', 'y']
        indicator_classes: list, ['total_ret', 'max_draw', 'm', '季度', 'y']
        return: dict,
        """
        res_dic = {}
        # 针对不同频率和周期，进行收益率的采样和数据剪切，并遍历计算出对应指标值并返回
        # 进行基本的参数有效性检验和log提示
        for indicator in indicator_classes:
            get_attr(self.operator, indicator)(daily_ret)
        return res_dic


if __name__ == "__main__":
    import unittest
    class IndicatorModelTest(unittest.TestCase):

        def test_cal_all(self):
            funds = [[], []]  # 不同资产日收益率序列
            stocks = [[], []]  # 不同资产日收益率序列
            # todo 此处补充完测试样例

