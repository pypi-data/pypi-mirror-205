from SqrtS.Core.event_process import MOUSEDOWN, MOUSEUP, EVERYTIME
from SqrtS.Widgets.Widget import Widget
import pygame


class MouseClickBoard(Widget):
    def __init__(self, size, IDname):
        """

        :param size: [int,int]
        :param IDname: str
        """
        super().__init__(size, IDname)
        self.click_poses = []
        self.up_poses = []
        self.pos = []
        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME]

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos:[int,int]
        :return: None
        """
        self.pos = new_pos

    def blit(self, window):
        """

        :param window: None
        :return: None
        """
        ...

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.click_poses.append(mouse_click_pos)
        else:
            ...

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.up_poses.append(mouse_click_pos)
        else:
            ...

    def register_for_event(self, window):
        """
        注册函数
        :param window:Window
        :return:
        """
        window.event_processor.register_event(MOUSEDOWN, self.check_mouse_down)
        window.event_processor.register_event(MOUSEUP, self.check_mouse_up)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)
