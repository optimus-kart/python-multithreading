class Test:
    def __init__(self):
        self.tests = {}

    def add(self, fn, tests):
        self.tests[fn] = tests

    def run(self):
        for fn, tests in self.tests.items():
            for test in tests:
                self.run_test(fn, test)

    def run_test(self, fn, test):
        test.setdefault("args", ())
        test.setdefault("kwargs", {})
        test.setdefault("returns", None)
        test.setdefault("raises", None)
        result = "Testing {}(".format(fn.__qualname__)
        if test["args"]:
            s = [str(x) for x in test["args"]]
            result += ", ".join(s)

        if test["kwargs"]:
            if test["args"]: result += ", "
            records = ["{}={}".format(k, str(v)) \
                       for k, v in test["kwargs"].items()]
            result += ", ".join(records)
        result += ") -> "
        result += "{}".format(test["raises"] if test["raises"] \
                                  else test["returns"])

        try:
            ret = fn(*test["args"], **test["kwargs"])
            if ret == test["returns"]:
                result += ": ok."
            else:
                result += ": *** failed\n    (got {})".format(ret)
        except Exception as e:
            if type(e) is not type(test["raises"]) or \
                            str(e) != str(test["raises"]):
                result += ": *** failed\n    (raised {})".format(e)
            else:
                result += ": ok."

        print(result)


-----------------------------------------------------
from time import sleep


def foo():
    for i in range(10):
        yield
        sleep(1)
        print("foo: counting {}".format(i))


def bar():
    for i in range(10):
        yield
        sleep(1)
        print("bar: counting {}".format(i))


if __name__ == '__main__':
    f = foo()
    b = bar()

    while True:
        next(f)
        next(b)

-----------------------------------------------------------
# https://public.etherpad-mozilla.org/p/Advanced_Python

from time import sleep


def foo():
    for i in range(10):
        sleep(1)
        print("foo: counting {}".format(i))


def bar():
    for i in range(10):
        sleep(1)
        print("bar: counting {}".format(i))


if __name__ == '__main__':
    from threading import Thread

    f = Thread(target=foo)
    b = Thread(target=bar)

    f.start()
    b.start()
    print("Two threads created...")
------------------------------------------------------------
# https://public.etherpad-mozilla.org/p/Advanced_Python

from itertools import count


def foo():
    for i in count():
        print("foo: counting {}".format(i))


def bar():
    for i in count():
        print("bar: counting {}".format(i))


if __name__ == '__main__':
    from threading import Thread

    f = Thread(target=foo)
    b = Thread(target=bar)
    f.start()
    b.start()

    for i in count():
        print("main: counting {}".format(i))
------------------------------------------------------------

from time import sleep


def foo():
    for i in range(7):
        print("foo: counting {}".format(i))
        sleep(1)


def bar():
    for i in range(20):
        print("bar: counting {}".format(i))
        sleep(1)


if __name__ == '__main__':
    from threading import Thread

    f = Thread(target=foo)
    b = Thread(target=bar)
    f.start()

    b.daemon = True
    b.start()

    for i in range(5):
        print("main: counting {}".format(i))
        sleep(1)

----------------------------------------------------------
from threading import Thread
from time import sleep


class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.thread_name = name

    def run(self):
        for i in range(10):
            print("{}: counting: {}".format(self.thread_name, i))
            sleep(1)


if __name__ == '__main__':
    t1 = MyThread("test-thread-1")
    t2 = MyThread("test-thread-2")

    t1.start()
    t2.start()
----------------------------------------------------------

"""
Exercise:
---------
Implement the class - RunPeriodic that allows a function
to be executed at periodic intervals in a separate thread.
[Available at https://public.etherpad-mozilla.org/p/Advanced_Python ]
"""

from threading import Thread


class RunPeriodic(Thread):
    pass  # TODO: Implement the logic here.


if __name__ == '__main__':

    def print_test():
        print("Running print_test...")


    def hello_world():
        print("Hello world....")


    print_thread = RunPeriodic(5, print_test)
    print_thread.start()
    # Execute print_test() function every 5 seconds

    hello_thread = RunPeriodic(2, hello_world)
    hello_thread.start()
    # Execute hello_thread() function every 2 seconds

    from time import sleep

    for i in range(40):
        print("main thread: counting", i)
        sleep(0.5)

    # Issue a stop request to both threads after 20 seconds
    print_thread.stop()
    hello_thread.stop()

    # Wait for both threads to finish.
    print_thread.join()
    hello_thread.join()

    print("main thread: finished.")
--------------------------------------------------------------
"""
Exercise:
---------
Implement the class - RunPeriodic that allows a function
to be executed at periodic intervals in a separate thread.
[Available at https://public.etherpad-mozilla.org/p/Advanced_Python ]
"""

from threading import Thread


class RunPeriodic(Thread):
    def __init__(self, interval, fn, args=(), kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.fn = fn
        self.fn_args = args
        self.fn_kwargs = kwargs

    def run(self):
        from time import sleep
        while not hasattr(self, "cancel"):
            self.fn(*self.fn_args, **self.fn_kwargs)
            sleep(self.interval)

    def stop(self):
        self.cancel = True


if __name__ == '__main__':

    def print_test():
        print("Running print_test...")


    def hello_world():
        print("Hello world....")


    print_thread = RunPeriodic(5, print_test)
    print_thread.start()
    # Execute print_test() function every 5 seconds

    hello_thread = RunPeriodic(2, hello_world)
    hello_thread.start()
    # Execute hello_thread() function every 2 seconds

    from time import sleep

    for i in range(40):
        print("main thread: counting", i)
        sleep(0.5)

    # Issue a stop request to both threads after 20 seconds
    print_thread.stop()
    hello_thread.stop()

    # Wait for both threads to finish.
    print_thread.join()
    hello_thread.join()

    print("main thread: finished.")
------------------------------------------------------------------
from time import sleep
from threading import Thread, current_thread


def foo():
    current = current_thread()
    for i in range(20):
        if hasattr(current, "cancel"): break
        print("foo: counting {}".format(i))
        sleep(1)


if __name__ == '__main__':
    f = Thread(target=foo)
    f.start()

    for i in range(5):
        print("main: counting {}".format(i))
        sleep(1)

    f.join(2)
    if (f.is_alive()):
        f.cancel = "True"

    f.join()
    print("main: foo joined...")

-----------------------------------------------------------------------
from random import random
from time import sleep
from threading import Thread

a = [10, 2, 4, 5, 6, 7]

b = [2, 3, 4]


def square(coll):
    for i, v in enumerate(coll):
        coll[i] = v * v
        sleep(random())


def cube(coll):
    for i, v in enumerate(coll):
        coll[i] = v ** 3
        sleep(random())


if __name__ == '__main__':
    print(a, b)
    s = Thread(target=square, args=(a,))
    c = Thread(target=cube, args=(b,))

    threads = [(s, a), (c, b)]

    s.start()
    c.start()

    while threads:
        t, r = threads.pop()
        t.join(0.1)
        if not t.is_alive():
            print(r)
        else:
            threads.insert(0, (t, r))

-----------------------------------------------------------
from __future__ import print_function

from threading import Thread

SIZE = 100000

a = list(range(SIZE))


def square_list_item(i):
    a[i] = a[i] * a[i]


def square_list():
    for i in range(SIZE):
        square_list_item(i)


if __name__ == '__main__':
    t1 = Thread(target=square_list)
    t2 = Thread(target=square_list)

    # b = a.copy()
    b = list(a)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    for i, v in enumerate(a):
        if (b[i] ** 4) != v:
            print("a[{}] = {} NOT consistent with b[{}] ** 4 = {}".format(
                i, v, i, b[i] ** 4))

-------------------------------------------------------------------
from __future__ import print_function

from threading import Thread, Lock

SIZE = 100000

a = list(range(SIZE))
lock = Lock()


def square_list_item_old(i):
    try:
        lock.acquire()
        a[i] = a[i] * a[i]
    finally:
        lock.release()


def square_list_item(i):
    with lock:
        a[i] = a[i] * a[i]


def square_list():
    for i in range(SIZE):
        square_list_item(i)


if __name__ == '__main__':
    t1 = Thread(target=square_list)
    t2 = Thread(target=square_list)

    # b = a.copy()
    b = list(a)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    for i, v in enumerate(a):
        if (b[i] ** 4) != v:
            print("a[{}] = {} NOT consistent with b[{}] ** 4 = {}".format(
                i, v, i, b[i] ** 4))

-------------------------------------------------------------------------


def access_url(method, url):
    import requests
    from time import time

    if hasattr(requests, method):
        start = time()
        response = getattr(requests, method)(url)
        duration = time() - start
        output = "{} {} took {} seconds with response code {}"
        print(output.format(method.upper(), url, duration,
                            response.status_code))


def benchmark_urls(filename):
    with open(filename) as url_file:
        for line in url_file:
            method, url = line.strip().split(" ")
            access_url(method.lower(), url)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("filename",
                        help="path to a text file containing list of URLs")

    args = parser.parse_args()

    benchmark_urls(args.filename)

--------------------------------------------------------------------------------
from threading import Thread, Condition, Lock
from time import sleep
from random import randint
from collections import deque


class SimpleQueue:
    def __init__(self, size=10):
        self.empty_slots = size
        self.queue = deque()
        self.empty = Condition()
        self.full = Condition()
        self.lock = Lock()

    def show(self):
        with self.lock:
            r = str(self.queue)
        return r

    def put(self, v):
        with self.full:
            if not self.empty_slots: self.full.wait()

        with self.empty:
            with self.lock: self.queue.append(v)
            self.empty_slots -= 1
            self.empty.notify()

    def get(self):
        with self.empty:
            if len(self.queue) == 0: self.empty.wait()

        with self.full:
            with self.lock: v = self.queue.popleft()
            self.empty_slots += 1
            self.full.notify()

        return v


queue = SimpleQueue(10)


def producer():
    while True:
        v = randint(1, 100)
        print("Produced: ", v, "Queue =", queue.show())
        queue.put(v)
        sleep(v / 200)


def consumer():
    while True:
        v = queue.get()
        print("Consumed: ", v, "Queue =", queue.show())
        sleep(v / 100)


p = Thread(target=producer)
c = Thread(target=consumer)

p.start()
c.start()

-----------------------------------------------------
from threading import Thread, Semaphore, Lock
from time import sleep
from random import randint
from collections import deque


class SimpleQueue:
    def __init__(self, size):
        self.queue = deque()
        self.reader = Semaphore(0)
        self.writer = Semaphore(size)
        self.lock = Lock()

    def show(self):
        with self.lock:
            s = str(self.queue)
        print(s)

    def put(self, v):
        self.writer.acquire()

        with self.lock: self.queue.append(v)

        self.reader.release()

    def get(self):
        self.reader.acquire()

        with self.lock: v = self.queue.popleft()

        self.writer.release()

        return v


queue = SimpleQueue(10)


def producer():
    while True:
        v = randint(1, 100)
        print("Produced: ", v)
        queue.put(v)
        # sleep(v/100.0)


def consumer():
    while True:
        v = queue.get()
        print("Consumed: ", v)
        sleep((v / 100.0) + 0.3)


p = Thread(target=producer)
c = Thread(target=consumer)

p.start()
c.start()




