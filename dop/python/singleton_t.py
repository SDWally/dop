import time
import threading


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print('new successfully')
            time.sleep(1)
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print('init successfully')


def task():
    obj = Singleton()
    print(id(obj))


if __name__ == '__main__':
    for i in range(3):
        t = threading.Thread(target=task)
        t.start()