import pygame
from SqrtS.Widgets.Widget import Widget
from SqrtS.tools.font import SqrtSFont, SystemFont
from SqrtS.Core.event_process import MOUSEUP, MOUSEDOWN, EVERYTIME, MOUSE_BUTTON_LEFT_DOWN, MOUSE_BUTTON_LEFT_UP


class Texts(Widget):
    def __init__(self,
                 text,
                 color,
                 font,
                 IDname: str,
                 if_antialias=True,
                 background=None):
        """

        :param text: str
        :param color: [int,int,int]
        :param font: SqrtSFont
        :param IDname: str
        :param if_antialias:bool
        :param background: [int,int,int]
        """

        self.chosen = False
        self.if_this_time_call_on = False
        self.click = False
        self.move_out_function = None
        self.up_function = None
        self.call_function = None
        self.move_on_function = None

        self.pos = []
        self.text_surface = font.render_text(text, color, if_antialias, background)
        self.size = self.text_surface.get_rect()[2:]
        self.font = font
        self.text = text
        self.color = color
        super().__init__(size=self.size,
                         IDname=IDname)

        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME]

    def change_text(self, new_text, color, font=None, if_antialias=True, background=None):
        """
        重新更改文字和类型
        :param new_text:新的文字
        :param color: 颜色
        :param font: 字体，SqrtSFont类型
        :param if_antialias: 是否抗锯齿（默认为True）
        :param background: 背景颜色三元组，默认为None
        :return: None
        """
        if font is not None:
            self.font = font
        self.text = new_text
        self.text_surface = font.render_text(self.text, color, if_antialias, background)
        self.size = self.text_surface.get_rect()[2:]

    def change_style(self, color, font=None, if_antialias=True, background=None):
        """
        简简单单地改变样式，只是对上面的change_text做了二次封装而已
        :param color: 上
        :param font: 上
        :param if_antialias:上
        :param background: 上
        :return: None
        """
        if font is not None:
            self.font = font
        self.change_text(self.text, color, font=self.font, if_antialias=if_antialias, background=background)

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos:
        :return:
        """
        self.pos = new_pos

    def blit(self, window):
        """
        画出图像
        :param window:Window
        :return: None
        """
        window.get_window().blit(self.text_surface, self.pos)

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param window:
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.click = True
            if self.call_function:
                self.call_function(self)

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param window:
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.click = False
            if self.up_function:
                self.up_function(self)

    def check_mouse_left_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param window:
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.click = True
            if self.call_function:
                self.call_function(self)

    def check_mouse_left_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param window:
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.click = False
            if self.up_function:
                self.up_function(self)

    def weight_everytime_event(self, window):
        """
        每时每刻都在运行的函数为everytime函数，按钮内用于处理按钮移动上去的事件
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.size[1] and not self.click:
            self.chosen = True
            if self.move_on_function and not self.if_this_time_call_on:
                self.move_on_function(self)
                self.if_this_time_call_on = True
        elif self.click:
            ...
        elif self.chosen:
            if self.move_out_function:
                self.move_out_function(self)
            self.chosen = False
            self.if_this_time_call_on = False

    def register_for_event(self, window):
        """
        注册函数，将目标函数注册到EventProcessor中
        :param window: window对象
        :return: None
        """
        window.event_processor.register_event(MOUSE_BUTTON_LEFT_DOWN, self.check_mouse_left_down)
        window.event_processor.register_event(MOUSE_BUTTON_LEFT_UP, self.check_mouse_left_up)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)

    def bind_call_func(self, func):
        """
        绑定回调函数
        :param func:函数体
        :return: None
        """
        self.call_function = func

    def bind_up_func(self, func):
        """
        绑定结束函数
        :param func:函数体
        :return: None
        """
        self.up_function = func

    def bind_on_func(self, func):
        """
        绑定鼠标一上去的函数
        :param func:函数体
        :return: None
        """
        self.move_on_function = func

    def bind_out_func(self, func):
        """
        绑定鼠标一出去的函数
        :param func:函数体
        :return: None
        """
        self.move_out_function = func


class LineTexts(Texts):
    def __init__(self,
                 text,
                 color,
                 font: SqrtSFont,
                 line_length: int,
                 IDname: str,
                 if_antialias=True,
                 background=None):
        super().__init__(text=text,
                         color=color,
                         font=font,
                         if_antialias=if_antialias,
                         background=background,
                         IDname=IDname)
        self.background = background
        self.line_length = line_length
        self.text_list = []
        self.text_surface_list = []

        self.split_texts()

    def split_texts(self):
        """
        划分文字的内部函数
        :return: None
        """
        step = self.line_length
        new_list = []
        for i in range(0, len(self.text), step):
            new_list.append(self.text[i:i + step])

        self.text_list = new_list

        new_surface_lst = []
        for o in self.text_list:
            new_surface_lst.append(
                self.font.render_text(o, self.color, background=self.background)
            )
        self.text_surface_list = new_surface_lst

        self.size = [self.text_surface_list[0].get_rect()[2:][0],
                     self.text_surface_list[0].get_rect()[2:][1] * len(self.text_surface_list)]
        self.size = [self.text_surface_list[0].get_rect()[2:][0],
                     self.text_surface_list[0].get_rect()[2:][1] * len(self.text_surface_list)]

    def change_text(self, new_text, color, font=None, if_antialias=True, background=None):
        """
        重新更改文字和类型
        :param new_text:新的文字
        :param color: 颜色
        :param font: 字体，SqrtSFont类型
        :param if_antialias: 是否抗锯齿（默认为True）
        :param background: 背景颜色三元组，默认为None
        :return: None
        """
        if font is not None:
            self.font = font
        self.text = new_text
        self.background = background
        self.color = color
        self.split_texts()
        self.size = [self.text_surface_list[0].get_rect()[2:][0],
                     self.text_surface_list[0].get_rect()[2:][1] * len(self.text_surface_list)]

    def blit(self, window):
        """
        画图
        :param window:
        :return:
        """
        for index, i in enumerate(self.text_surface_list):
            window.get_window().blit(i, [self.pos[0], self.pos[1] + self.text_surface_list[0].get_rect()[3] * index])
