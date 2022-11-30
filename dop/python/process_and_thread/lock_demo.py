# Python线程锁和进程锁


# 线程锁
import threading

lock = threading.Lock()
lock.acquire()
lock.release()

# 进程锁

import multiprocessing

process_lock = multiprocessing.Lock()

process_lock.acquire()
process_lock.release()

