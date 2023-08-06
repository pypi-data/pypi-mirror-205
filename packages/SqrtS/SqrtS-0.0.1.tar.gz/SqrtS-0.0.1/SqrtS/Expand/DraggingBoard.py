from SqrtS.Core.event_process import MOUSEDOWN, MOUSEUP, EVERYTIME
from SqrtS.Widgets.Widget import Widget
import pygame

"""
拓展模块之一：拖拽板
可以检测拖拽并且调用相应的函数！
"""


class DraggingBoard(Widget):
    """
    拖拽板
    """

    def __init__(self, size, IDname):
        """
        :param size:[int,int]
        :param IDname: str
        """
        super().__init__(size, IDname)
        self.pos = []
        self.if_mouse_down = False
        self.last_mouse_pos = []

        self.call_slide_function = None

    def bind_pos(self, new_pos: list):
        """
        固定绑定坐标
        :param new_pos:[]
        :return: None
        """
        self.pos = new_pos

    def blit(self, window):
        """
        拖拽板哪里有绘图函数?为了直接兼容，所以只能写这个函数
        :param window: None
        :return: None
        """
        ...

    def bind_call_slide(self, func):
        """
        绑定滑动函数
        :param func:函数体
        :return: None
        """
        self.call_slide_function = func

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.if_mouse_down = True
            self.last_mouse_pos = pygame.mouse.get_pos()
        else:
            self.if_mouse_down = False

    def check_mouse_up(self, event, window):
        """
        检测鼠标弹起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.if_mouse_down = False
        else:
            self.if_mouse_down = False

    def weight_everytime_event(self, window):
        """
        内部函数的实时函数
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.size[1]:
            if self.if_mouse_down and mouse_pos != self.last_mouse_pos:
                self.call_slide_function()
        else:
            ...

    def register_for_event(self, window):
        """
        注册函数
        :param window: Window
        :return: None
        """
        window.event_processor.register_event(MOUSEDOWN, self.check_mouse_down)
        window.event_processor.register_event(MOUSEUP, self.check_mouse_up)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)


class GlobalDraggingBoard(DraggingBoard):
    """
    全局拖拽板（☞可以获取全局坐标的改变）
    """
    def __init__(self, size, IDname):
        super().__init__(size, IDname)
        self.window_pos = []
        self.abs_pos = []

    def update_info(self, window):
        """
        更新信息，内部函数
        :param window:
        :return:
        """
        self.window_pos = window.window_mover.get_window_pos()

    def check_pos_in(self, pos_click):
        """
        检测坐标是否在控件内部
        :param pos_click: 需要判断的坐标[int, int]
        :return: bool
        """
        if self.pos[0] < pos_click[0] < self.pos[0] + self.size[0] and self.pos[1] < pos_click[1] < \
                self.pos[1] + self.size[1]:
            return True
        else:
            return False

    def check_pos_in_abs(self, pos_click):
        """
        检测绝对坐标是否在控件内
        :param pos_click: 坐标[int, int]
        :return: None
        """
        if self.abs_pos[0] < pos_click[0] < self.abs_pos[0] + self.size[0] and self.abs_pos[1] < pos_click[1] < \
                self.abs_pos[1] + self.size[1]:
            return True
        else:
            return False

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        abs_mouse_pos = [mouse_click_pos[0] + self.window_pos[0],
                         mouse_click_pos[1] + self.window_pos[1]]

        self.abs_pos = [
            self.pos[0] + self.window_pos[0],
            self.pos[1] + self.window_pos[1]
        ]

        if self.check_pos_in_abs(abs_mouse_pos):
            self.if_mouse_down = True
            self.last_mouse_pos = pygame.mouse.get_pos()
        else:
            self.if_mouse_down = False

    def check_mouse_up(self, event, window):
        """
        检测鼠标弹起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        abs_mouse_pos = [mouse_click_pos[0] + self.window_pos[0],
                         mouse_click_pos[1] + self.window_pos[1]]
        self.abs_pos = [
            self.pos[0] + self.window_pos[0],
            self.pos[1] + self.window_pos[1]
        ]

        if self.check_pos_in_abs(abs_mouse_pos):
            self.if_mouse_down = False
        else:
            self.if_mouse_down = False

    def weight_everytime_event(self, window):
        """
        注册实时事件
        :return:
        """
        if self.if_mouse_down:
            self.call_slide_function()
        else:
            ...



