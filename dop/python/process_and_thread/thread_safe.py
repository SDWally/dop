import threading
from threading import Lock

# 线程不安全的示例

number = 0

def add():
    global number
    for i in range(1000000):
        number += 1

thread_1 = threading.Thread(target=add)
thread_2 = threading.Thread(target=add)
thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()

print(number)

# 线程安全的示例

number = 0

lock = Lock()

def add():
    global number
    for i in range(1000000):
        with lock:
            number += 1

thread_1 = threading.Thread(target=add)
thread_2 = threading.Thread(target=add)
thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()

print(number)