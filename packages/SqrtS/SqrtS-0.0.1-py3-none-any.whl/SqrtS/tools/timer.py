import time
import threading


class Timer:
    """
    定时器类
    """

    def __init__(self, put: int, call_func):
        self.alive = True
        self.put = put
        self.start_time = int(time.time())
        self.passtime = 0
        self.call_func = call_func

    def check_time(self):
        while self.alive:
            self.passtime = int(time.time()) - self.start_time
            if self.put <= self.passtime:
                self.call_func()
                self.alive = False

    def run_timer(self):
        thread = threading.Thread(target=self.check_time)
        thread.start()

    def stop(self):
        self.alive = False


class AccurateTimer:
    def __init__(self, put: int, call_func):
        self.alive = True
        self.put = put
        self.start_time = int(time.time() * 1000)
        self.passtime = 0
        self.call_func = call_func

    def check_time(self):
        while self.alive:
            self.passtime = int(time.time() * 1000) - self.start_time
            if self.put <= self.passtime:
                self.call_func()
                self.alive = False

    def run_timer(self):
        thread = threading.Thread(target=self.check_time)
        thread.start()

    def stop(self):
        self.alive = False


class CirculateTimer:
    def __init__(self, put: int, call_func):
        self.alive = True
        self.put = put
        self.start_time = int(time.time())
        self.passtime = 0
        self.call_func = call_func

    def check_time(self):
        while self.alive:
            self.passtime = int(time.time()) - self.start_time
            if self.put <= self.passtime:
                self.call_func()
                self.start_time = int(time.time())

    def run_timer(self):
        thread = threading.Thread(target=self.check_time)
        thread.start()

    def stop(self):
        self.alive = False


class AccurateCirculateTimer:
    def __init__(self, put: int, call_func):
        self.alive = True
        self.put = put
        self.start_time = int(time.time() * 1000)
        self.passtime = 0
        self.call_func = call_func

    def check_time(self):
        while self.alive:
            self.passtime = int(time.time() * 1000) - self.start_time
            if self.put <= self.passtime:
                self.call_func()
                self.start_time = int(time.time() * 1000)

    def run_timer(self):
        thread = threading.Thread(target=self.check_time)
        thread.start()

    def stop(self):
        self.alive = False


class TimesCirculateTimer:
    def __init__(self, put: int, call_func, times):
        self.times = times
        self.alive = True
        self.put = put
        self.start_time = int(time.time() * 1000)
        self.passtime = 0
        self.call_func = call_func

    def check_time(self):
        while self.alive and self.times:
            self.passtime = int(time.time() * 1000) - self.start_time
            if self.put <= self.passtime:
                self.call_func()
                self.start_time = int(time.time() * 1000)
                self.times -= 1

    def run_timer(self):
        thread = threading.Thread(target=self.check_time)
        thread.start()

    def stop(self):
        self.alive = False


if __name__ == "__main__":
    def say_hello():
        print("hello!")


    t = TimesCirculateTimer(500, say_hello, 5)
    t.run_timer()
