
class Singleton(object):

    def __init__(self, name):
        self.name = name

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    @staticmethod
    def instance_2(*args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance


single_1 = Singleton.instance_2('第1次创建')
single_2 = Singleton.instance_2('第2次创建')

print(single_1 is single_2)

from threading import RLock


lock = RLock()


class Singleton(object):

    def __init__(self, name):
        self.name = name

    def __new__(cls, *args, **kwargs):
        with lock:
            if not hasattr(cls, "_instance"):
                cls._instance = super().__new__(cls)
        return cls._instance


single_1 = Singleton('第1次创建')
single_2 = Singleton('第2次创建')

print(single_1 is single_2)