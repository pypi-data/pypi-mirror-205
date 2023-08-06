import threading
from threading import Lock, Event
import time

# EXAMPLE 1  ----------------------------------------------------------------
# correct example - threading works
# notice the use of lock argument - that's becasue we declare lock = Lock() inside a funtion.
# if it's global, then we don;t need to pass lock into arguments
x = 0

def thread_task(lock):
    global x
    for i in range(100000):
        with lock:
            x += 1


def main_task():
    lock = Lock()

    t1 = threading.Thread(target=thread_task, args=(lock,))
    t2 = threading.Thread(target=thread_task, args=(lock,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # expected behavior: we CONSISTENTLY get the same result (200000)

main_task()
print(f'total {x}')

# END EXAMPLE 1  ----------------------------------------------------------------


# EXAMPLE 2  ----------------------------------------------------------------
stack = 10
lock = Lock()

def add_book():
    global stack
    for i in range(100000):
        with lock:
            stack += 1

def take_book():
    global stack
    for i in range(100000):
        with lock:
            stack -= 1

# thread1 = threading.Thread(target=add_book, args=(lock,))
# thread2 = threading.Thread(target=take_book, args=(lock,))
thread1 = threading.Thread(target=add_book)
thread2 = threading.Thread(target=take_book)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(stack)

# END EXAMPLE 2  ----------------------------------------------------------------



























