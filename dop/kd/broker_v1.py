# -*- coding: UTF-8 -*-

import heapq
from .project.base import BaseBroker


class Broker(BaseBroker):

    def __init__(self):
        self.ask_book = []  # 卖
        self.bid_book = []  # 买
        self.ask_book_map = {}
        self.bid_book_map = {}

    def transact(self, order: tuple, **kwargs):
        """
        Transact: deal with each order sequentially.

        Args:
            order (Any): Required.
        """
        idx, _time, price, volume, quote_type, order_type = order
        idx = int(idx)
        price = float(price)
        volume = int(volume)
        if quote_type == "BID":
            while self.ask_book:
                priority_key, (ask_price, ask_volume) = heapq.heappop(self.ask_book)
                if order_type == "MARKET":
                    price = ask_price
                if ask_price <= price:
                    if ask_volume > volume:
                        ask_volume -= volume
                        volume = 0
                        self.ask_book_map[ask_price] = ask_volume
                        heapq.heappush(self.ask_book, (priority_key, (ask_price, ask_volume)))
                        break
                    elif ask_volume == volume:
                        volume = 0
                        del self.ask_book_map[ask_price]
                        break
                    else:
                        volume -= ask_volume
                        continue
                else:
                    break
            if volume > 0:
                # 买单用价格的相反数存储，以保证高价格先成交
                if price in self.bid_book_map:
                    self.bid_book_map[price] += volume
                else:
                    self.bid_book_map[price] = volume
                heapq.heappush(self.bid_book, ((-price, _time, idx), (price, volume)))
        elif quote_type == "ASK":
            while self.bid_book:
                priority_key, (bid_price, bid_volume) = heapq.heappop(self.bid_book)
                if order_type == "MARKET":
                    price = bid_price
                if bid_price >= price:
                    if bid_volume > volume:
                        bid_volume -= volume
                        volume = 0
                        self.bid_book_map[bid_price] = bid_volume
                        heapq.heappush(self.bid_book, (priority_key, (bid_price, bid_volume)))
                        break
                    elif bid_volume == volume:
                        volume = 0
                        del self.ask_book_map[bid_price]
                        break
                    else:
                        volume -= bid_volume
                        continue
                else:
                    break
            if volume > 0:
                if price in self.ask_book_map:
                    self.ask_book_map[price] += volume
                else:
                    self.ask_book_map[price] = volume
                heapq.heappush(self.ask_book, ((price, _time, idx), (price, volume)))
        else:
            pass

    @staticmethod
    def _gen_order_book(book_map, level, quote_type):
        book_tuple = [(key, value) for key, value in book_map.items()]
        return [(quote_type + str(i + 1), key, value) for i, (key, value) in enumerate(sorted(book_tuple, key=lambda x: x[1], reverse=True)[:level])]

    def order_book(self, level: int = 5, **kwargs):
        """
        Order book: N level.

        Args:
            level (int): Optional, N-level, default is 5.
        """
        return self._gen_order_book(self.bid_book_map, level, "bid") + self._gen_order_book(self.ask_book_map, level, "ask")
