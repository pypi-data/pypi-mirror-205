from SqrtS.Layouts.Layout import Layout
from SqrtS.Widgets.Widget import Widget


class FloatingLayout(Layout):
    """
    浮动布局
    """

    def __init__(self, name):
        """

        :param name:布局名
        """
        super().__init__(name=name)
        self.widgets_poses = {}
        self.widgets = []

    def compute_poses(self):
        """
        计算更新坐标
        :return: None
        """
        for i in self.widgets_poses.keys():
            for ii in self.widgets:
                if ii.IDname == i:
                    ii.bind_pos(self.widgets_poses[i])

    def bind_widgets_poses(self, widgets_pos_dict: dict):
        """
        绑定每个控件的坐标
        :param widgets_pos_dict: 空间坐标字典,{"IDname?":[int,int],...}
        :return: None
        """
        for key in widgets_pos_dict.keys():
            self.widgets_poses[str(key)] = widgets_pos_dict[key]

        self.compute_poses()

    def blit_all(self, window):
        """
        在屏幕上画出所有的控件
        :return: None
        """
        for i in self.widgets:
            if i.widget_alive:
                i.blit(window)
            else:
                self.widgets.remove(i)

    def append(self, weight: Widget):
        """
        添加控件
        :param weight:Widget
        :return: None
        """
        self.widgets.append(weight)
        self.compute_poses()

    def appends(self, weights: list):
        """
        批量添加控件（推荐）
        :param weights: []
        :return: None
        """
        for i in weights:
            self.widgets.append(i)
        self.compute_poses()

    def adds(self, weights):
        """
        追加已经由外部设定好坐标的控件
        :param weights: list
        :return: None
        """
        for i in weights:
            self.widgets.append(i)
