import abc
import threading


class DynamicEffects:
    def __init__(self):
        self.if_finished = False

    def times_call(self, time_interval, times_, func):
        """
        内部函数，用于多次调用，内部采用递归实现
        :param time_interval: 时间间隔
        :param times_: 次数
        :param func: 函数体
        :return: None
        """
        times_ = times_
        count = 0

        def _times_call():
            """
            内部函数
            :return:None
            """
            nonlocal count
            count += 1
            func()
            if count < times_:
                t = threading.Timer(time_interval, _times_call)
                t.start()
            else:
                self.if_finished = True

        _times_call()

    @abc.abstractmethod
    def update(self, window):
        ...

    @abc.abstractmethod
    def _update_dynamic_effects(self):
        ...
