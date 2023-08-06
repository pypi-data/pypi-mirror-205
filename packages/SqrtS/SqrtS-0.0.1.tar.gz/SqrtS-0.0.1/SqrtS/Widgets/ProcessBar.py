import copy
from abc import ABC

from SqrtS.tools.load_theme import Theme
from SqrtS.Widgets import Widget
from SqrtS.Widgets.Button import _SlideButton, BROADWISE
from SqrtS.Core.event_process import MOUSEUP, MOUSEDOWN, EVERYTIME
import pygame


class SlideBar(Widget.Widget):
    def __init__(self,
                 theme: Theme,
                 size: list,
                 button_size: list,
                 IDname: str, ):
        """
        不确定
        :param theme:
        :param size:
        :param button_size:
        :param IDname:

        """
        super().__init__(size, many_weights=False, IDname=IDname)
        self.move_out_function = None
        self.if_this_time_call_on = None
        self.move_on_function = None
        self.chosen = None
        self.up_function = None
        self.call_function = None
        self.pos = []
        # 导入素材     1.滑块正常背景  2.滑块被选择时的背景  3.滑块按钮正常时的样子  4.滑块按钮被选择时的样子  5.滑块按钮被点击拖动时的样子  6.背景覆盖的图像拉伸（推荐纯色）
        self.process_bar_base_img_formal = pygame.transform.scale(theme.get_theme()["sb_formal"], size)
        self.process_bar_chosen_img = pygame.transform.scale(theme.get_theme()["sb_chosen"], size)

        self.process_bar_head_button_img_formal = pygame.transform.scale(theme.get_theme()["sb_b_formal"], button_size)
        self.process_bar_head_button_img_chosen = pygame.transform.scale(theme.get_theme()["sb_b_chosen"], button_size)
        self.process_bar_head_button_img_click = pygame.transform.scale(theme.get_theme()["sb_b_click"], button_size)

        self.now_bar_img = self.process_bar_base_img_formal
        self.now_button_img = self.process_bar_head_button_img_formal

        # button_size,img_list,motion_range,limit_direction
        self.slide_button = _SlideButton([self.size[1], self.size[1]],
                                         [self.process_bar_head_button_img_formal,
                                          self.process_bar_head_button_img_click,
                                          self.process_bar_head_button_img_chosen],
                                         BROADWISE, IDname="process_bar_button")

        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME]

    def bind_pos(self, new_pos: list):
        """
        绑定新坐标
        """
        self.pos = new_pos
        pos_copy = copy.copy(new_pos)
        self.slide_button.bind_pos(pos_copy)
        self.slide_button.bind_move_length(pos_copy, self.size[0])

    def blit(self, window):
        """
        在屏幕上画出图
        """
        window.get_window().blit(self.now_bar_img, self.pos)
        self.slide_button.blit(window)

    def _compute_value(self):
        """计算值"""
        ...

    @staticmethod
    def _compute_central_pos(left_top, size):
        return [int(left_top[0] + size[0] / 2), int(left_top[1] + size[1])]

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[
            1] < \
                self.pos[1] + self.size[1]:
            self.locate_pos_by_mouse(mouse_click_pos)
            if self.call_function:
                self.call_function(self)
        else:
            ...

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[
            1] < \
                self.pos[1] + self.size[1]:
            if self.up_function:
                self.up_function(self)
        else:
            ...

    def weight_everytime_event(self, window):
        """
        每时每刻都在运行的函数为everytime函数，按钮内用于处理按钮移动上去的事件
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.size[1]:
            self.now_bar_img = self.process_bar_chosen_img
            if self.move_on_function and not self.if_this_time_call_on:
                self.move_on_function(self)
                self.if_this_time_call_on = True
        elif self.chosen:
            self.now_bar_img = self.process_bar_base_img_formal
            if self.move_out_function:
                self.move_out_function(self)
        else:
            self.now_bar_img = self.process_bar_base_img_formal

    def register_for_event(self, window):
        window.event_processor.register_event(MOUSEDOWN, self.check_mouse_down)
        window.event_processor.register_event(MOUSEUP, self.check_mouse_up)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)
        self.slide_button.register_for_event(window=window)

    def bind_call_func(self, func):
        self.call_function = func

    def bind_up_func(self, func):
        self.up_function = func

    def bind_on_func(self, func):
        self.move_on_function = func

    def bind_out_func(self, func):
        self.move_out_function = func

    def locate_pos_by_mouse(self, mouse_pos):
        self.slide_button.bind_pos([mouse_pos[0] - int(self.size[1] / 2), self.slide_button.pos[1]])

    def get_value(self):
        return self._compute_value()


class FollowSlideBar(SlideBar):
    def __init__(self, theme: Theme,
                 size: list,
                 button_size: list,
                 IDname: str):
        super().__init__(theme, size, button_size, IDname)

        self.process_bar_over_formal = pygame.transform.scale(theme.get_theme()["sb_cover"], size)

    def update_over_size(self):
        self.process_bar_over_formal = pygame.transform.scale(self.process_bar_over_formal,
                                                              [self.slide_button.pos[0], self.size[1]])

    def blit(self, window):
        self.update_over_size()
        window.get_window().blit(self.now_bar_img, self.pos)
        window.get_window().blit(self.process_bar_over_formal, self.pos)
        self.slide_button.blit(window)


class ProcessBar(Widget.Widget):
    def __init__(self, theme: Theme,
                 size: list,
                 IDname: str,
                 unit_length: int):
        """
        进度条
        :param theme: Theme
        :param size: 单位长度下的尺寸
        :param IDname: ID
        :param unit_length:单位长度
        例如，size为【1,100】，unit_length=2，意为尺寸为1-100，每一个尺寸数值对应像素长度2
        """
        super().__init__(size, IDname)

        self.unit_size = unit_length
        self.size = [size[0] * unit_length, size[1] * unit_length]
        self.IDname = IDname

        self.max_length = int(self.size[0] / self.unit_size)

        self.over_size = 1
        self.pos = []

        self.bar_formal_img = pygame.transform.scale(theme.get_theme()["pb_formal"], self.size)
        self.bar_over_img = theme.get_theme()["pb_over"]

    def bind_pos(self, new_pos: list):
        self.pos = new_pos

    def update_over(self):
        self.bar_over_img = pygame.transform.scale(self.bar_over_img, [self.over_size * self.unit_size, self.size[1]])

    def blit(self, window):
        self.update_over()
        window.get_window().blit(self.bar_formal_img, self.pos)
        window.get_window().blit(self.bar_over_img, self.pos)

    def register_for_event(self, window):
        ...

    def add_process(self, num):
        if (self.over_size + num) <= self.max_length:
            self.over_size += num
        else:
            self.over_size = self.max_length

    def cut_process(self, num):
        if (self.over_size - num) >= 0:
            self.over_size -= num
        else:
            self.over_size = 0

    def set_process(self, num):
        if 0 <= num <= self.max_length:
            self.over_size = num


if __name__ == "__main__":
    ...
