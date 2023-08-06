from abc import abstractmethod  # 抽象方法装饰器，声明一个必须被实现的方法
from SqrtS.Widgets.Widget import Widget


class Layout:
    """
    所有布局的基础类
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def compute_poses(self):
        """
        计算更新坐标
        :return: None
        """
        ...

    @abstractmethod
    def blit_all(self, window):
        """
        在屏幕上画出所有的控件
        :return: None
        """
        ...

    @abstractmethod
    def append(self, weight: Widget):
        ...

    @abstractmethod
    def appends(self, weights: list):
        ...
