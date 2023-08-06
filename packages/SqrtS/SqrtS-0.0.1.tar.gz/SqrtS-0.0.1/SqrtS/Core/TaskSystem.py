import threading

"""
我想你来到这又是一脸懵对不对？怎么前面一个事件处理器，这么这里又来了一个任务处理器？
这个不同于事件处理器，这个是处理用户定义的任务的。
比如，你有一个任务想要长期执行，每间隔多少秒，那么你就可以调用register_for_infinite_task啦！是不是很方便？
亦或者，你想执行一个任务，间隔多少秒，你就可以调用register_for_times_task
注意！这里的注册函数，一旦注册便会开始计数！也就是一旦注册便会进行运行倒计时！

from:__CEMEYE__  
:)
"""

ONCE = 111
TIMES = 222
INFINITE = 333
TERMINABLE_INFINITE = 444
PAUSING = 555


class TaskSystem:
    """
    挺无聊的类，我也不想去额外定义一个任务类了
    """

    def __init__(self):
        self.infinite_task_pool = []
        self.once_task_pool = []
        self.times_task_pool = []
        self.pausing_task_pool = []
        self.pausing_task_names = {}

        self.terminable_infinite_task = []
        self.terminable_task_names = {}

    def register_for_infinite_task(self, task_func, time_interval):
        """
        注册永久任务
        :param task_func: 目标函数
        :param time_interval: 时间间隔(s)
        :return: None
        """
        self.infinite_task_pool.append([task_func, time_interval])

    def register_for_terminable_infinite_task(self, task_func, time_interval, task_name):
        """
        注册永久任务
        :param task_name: 可停止无限函数的ID名
        :param task_func: 目标函数
        :param time_interval: 时间间隔(s)
        :return: None
        """
        self.terminable_infinite_task.append([task_func, time_interval, task_name])
        self.terminable_task_names[task_name] = True

    def register_fot_once_task(self, task_func, time_interval, args=None):
        """
        注册一次性任务
        :param task_func:任务函数
        :param time_interval: 任务间隔（多少秒后执行？）
        :param args: 参数，可选
        :return: None
        """
        self.once_task_pool.append([task_func, time_interval, args])

    def register_for_times_task(self, task_func, times, time_interval, args):
        """
        注册多次的任务
        :param args: 参数
        :param task_func: 任务函数体
        :param times: 次数
        :param time_interval:时间间隔
        :return:None
        """
        self.times_task_pool.append([task_func, time_interval, times, args])

    def register_for_pausing_task(self, task_func, time_interval, task_name):
        """
        注册暂停时期的任务，时间间隔可以为0
        :param task_func: 任务函数体
        :param time_interval:时间间隔
        :return:None
        """
        self.pausing_task_pool.append([task_func, time_interval, task_name])
        self.pausing_task_names[task_name] = True

    def infinite_call(self, time_interval, func):
        """
        内部方法，无线调用函数
        :param time_interval:时间间隔
        :param func: 函数体
        :return: None
        """
        func()
        threading.Timer(time_interval, self.infinite_call, args=[time_interval, func]).start()

    def terminable_infinite_call(self, time_interval, func, task_name):
        func()
        if self.terminable_task_names[task_name]:
            threading.Timer(time_interval, self.terminable_infinite_call, args=[time_interval, func, task_name]).start()

    def terminable_infinite_pausing_call(self, time_interval, func, task_name):
        func()
        if self.pausing_task_names[task_name]:
            threading.Timer(time_interval, self.terminable_infinite_pausing_call,
                            args=[time_interval, func, task_name]).start()

    def times_call(self, time_interval, times_, func, i, args):
        """
        内部函数，用于多次调用，内部采用递归实现
        :param time_interval: 时间间隔
        :param times_: 次数
        :param func: 函数体
        :param i: 这个函数被for循环调用，所以需要传i
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
                t = threading.Timer(time_interval, _times_call, args=[args])
                t.start()
            else:
                try:
                    self.times_task_pool.remove(i)
                except ValueError as e:
                    ...

        _times_call()

    def task_system_update(self):
        """
        任务系统更新，内部函数
        :return: None
        """
        for i in self.once_task_pool:
            threading.Timer(i[1], i[0], args=[i[2], ]).start()
            self.once_task_pool.remove(i)

        for i in self.times_task_pool:
            self.times_call(i[1], i[2], i[0], i, args=i[-1])
            self.times_task_pool.remove(i)

        for i in self.infinite_task_pool:
            self.infinite_call(i[1], i[0])
            self.infinite_task_pool.remove(i)

        for i in self.terminable_infinite_task:
            self.terminable_infinite_call(i[1], i[0], i[2])
            self.terminable_infinite_task.remove(i)

    def start_pausing_tasks(self):
        """
        暂停时期的任务系统更新，内部函数
        :return: None
        """
        for i in self.pausing_task_pool:
            self.terminable_infinite_pausing_call(i[1], i[0], i[2])
            self.pausing_task_pool.remove(i)

    def destroy_pausing_type(self):
        """
        停止暂停状态
        :return: None
        """
        for key in self.pausing_task_names.keys():
            self.pausing_task_names[key] = False

    def destroy_terminable_infinite_pausing_task(self, task_name):
        """
        注销某个暂停时期的可停止的任务
        :param task_name:任务名
        :return: None
        """
        self.pausing_task_names[task_name] = False

    def destroy_terminable_infinite_task(self, task_name):
        """
        注销某个可停止的任务
        :param task_name:任务名
        :return: None
        """
        self.terminable_task_names[task_name] = False


if __name__ == "__main__":
    def once():
        print("once task!")


    def times():
        print("times!")


    def infinite():
        print("infinite!")


    def async_register(ts):
        ts.register_for_times_task(times, 2, 3)


    ts = TaskSystem()

    threading.Timer(0.01, async_register, args=[ts]).start()

    ts.register_for_infinite_task(infinite, 0.01)

    while True:
        ts.task_system_update()
