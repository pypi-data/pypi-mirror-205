"""
hello!  :)

你又来看代码了！这个文件主要定义了一大堆错误，其实每个定义都很简单！
想看具体的错误类型的就翻一下这个文件吧！
"""


class WidgetNotFound(Exception):
    """
    这个错误主要存在于Window.get_widget_by_IDname这个函数！
    如果IDname输错了或者根本没有这个控件就会报这个错误
    """
    ...


class StrayHasBeenRunningError(Exception):
    """
    这个错误主要存在于系统托盘的调用中，当托盘线程启动时，无法动态添加选项！
    """
