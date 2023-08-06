from SqrtS.Animation.VectorMove import VectorMove, Vector
from SqrtS.Widgets.FrameBox import FrameBox
from SqrtS.Core.core import get_screen_pixel
from SqrtS.Widgets.Widget import Widget


class SideBar(Widget):
    def __init__(self,
                 window_size,
                 width,
                 time_interval,
                 background_image_path,
                 direction="left",
                 x_speed=1):
        """
        侧边栏类
        :param width:侧边栏宽度
        :param time_interval:移动刷新时间间隔（移动一次需要的时间，其实0.01即可）
        :param background_image_path: 背景图片路径
        :param direction: 方向,只有left和right
        :param x_speed: 每一次移动多少？最好不要改，否则会出现奇怪的效果！
        """
        # 获取窗口大小
        super().__init__([width, window_size[1]], "sidebar")
        self.screen_size = window_size

        self.widget_framebox = FrameBox("sidebar_framebox", size=[width, self.screen_size[1]],
                                        background_image_path=background_image_path)

        self.x_speed = x_speed
        self.direction = direction
        self.width = width
        self.time_interval = time_interval

        if self.direction == "left":
            self.widget_framebox.bind_pos([0, 0])
            self.move_in_vector = VectorMove(Vector(-int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                             x_speed=self.x_speed)
            self.move_out_vector = VectorMove(Vector(int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                              x_speed=self.x_speed)
            self.move_in_vector.bind_widget(self.widget_framebox)
            self.move_out_vector.bind_widget(self.widget_framebox)
        elif self.direction == "right":
            self.widget_framebox.bind_pos([0, self.screen_size[0] - self.width])
            self.move_in_vector = VectorMove(Vector(int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                             x_speed=self.x_speed)
            self.move_out_vector = VectorMove(Vector(-int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                              x_speed=self.x_speed)
            self.move_in_vector.bind_widget(self.widget_framebox)
            self.move_out_vector.bind_widget(self.widget_framebox)

        self.if_out = True

    def bind_pos(self, new_pos: list):
        """
        最好不要用！
        :param new_pos:新坐标
        :return: None
        """
        self.widget_framebox.bind_pos(new_pos)

    def blit(self, window):
        self.widget_framebox.blit(window)

    def register_for_event(self, window):
        """
        注册事件
        :param window: Window
        :return: None
        """
        self.widget_framebox.register_for_event(window=window)

    def appends_widgets(self, widgets_list):
        """
        添加控件列表！
        :param widgets_list:控件
        :return:
        """
        self.widget_framebox.appends_widgets(widgets_list=widgets_list)

    def _make_vector_in(self):
        """
        因为vectorMove是一次性的，所以需要重新生成
        :return: 你猜有没有？
        """
        if self.direction == "left":
            self.move_in_vector = VectorMove(Vector(-int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                             x_speed=self.x_speed)
            self.move_in_vector.bind_widget(self.widget_framebox)
        elif self.direction == "right":
            self.move_in_vector = VectorMove(Vector(int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                             x_speed=self.x_speed)
            self.move_in_vector.bind_widget(self.widget_framebox)

    def _make_vector_out(self):
        """
        因为vectorMove是一次性的，所以需要重新生成
        :return: 你猜有没有？
        """
        if self.direction == "left":
            self.move_out_vector = VectorMove(Vector(int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                              x_speed=self.x_speed)
            self.move_out_vector.bind_widget(self.widget_framebox)
        elif self.direction == "right":
            self.move_out_vector = VectorMove(Vector(-int(abs(self.width) / self.x_speed), 0), self.time_interval,
                                              x_speed=self.x_speed)
            self.move_out_vector.bind_widget(self.widget_framebox)

    def move_in(self, window):
        """
        触发向内移动函数
        :param window: Window
        :return: ∅
        """
        if self.if_out:
            self._make_vector_in()
            window.register_for_dynamic_effect(self.move_in_vector)
            self.if_out = False

    def get_if_out(self):
        return self.if_out

    def move_out(self, window):
        """
        触发向外移动函数
        :param window:Window
        :return: ∅
        """
        if not self.if_out:
            self._make_vector_out()
            window.register_for_dynamic_effect(self.move_out_vector)
            self.if_out = True

    def bind_widgets_poses(self, pos_dict):
        self.widget_framebox.bind_widgets_poses(pos_dict)


if __name__ == "__main__":
    # C:\Users\Administrator\PycharmProjects\SqrtSGUI\sources
    ...
