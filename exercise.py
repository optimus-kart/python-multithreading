from threading import Thread
from time import sleep

class RunPeriodic(Thread):
    def __init__(self,sleep_time,func):
        Thread.__init__(self)
        self.sleep_time=sleep_time
        self.func = func

    def run(self):
        self.func()
        sleep(self.sleep_time)

    def stop(self):
        print("Stopping thread..")




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


