from SqrtS.Widgets.Widget import Widget
from SqrtS.Core.event_process import DROPFILE, EVERYTIME
import pygame


class FileDropper(Widget):
    """
    文件拖拽
    """

    def __init__(self, size, IDname, theme):
        super().__init__(size, IDname)
        self.pos = []
        self.file_dropper_img = pygame.transform.scale(theme.get_theme()["file_dropper"], size)
        self.cursor_in = False

        self.drop_files = []

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos: [int,int]
        :return: None
        """
        self.pos = new_pos

    def blit(self, window):
        """
        画出控件
        :param window: Window
        :return: None
        """
        window.get_window().blit(self.file_dropper_img, self.pos)

    def weight_everytime_event(self, window):
        """
        实时事件
        :param window:Window
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.size[1]:
            self.cursor_in = True
        else:
            self.cursor_in = False

    def check_drop_file(self, event, window):
        """
        检测拖拽文件的函数
        :param event: 事件
        :param window: Window
        :return: None
        """
        if self.cursor_in:
            self.drop_files.append(event.file)

    def register_for_event(self, window):
        """
        注册事件
        :param window: Window
        :return: None
        """
        window.event_processor.register_event(DROPFILE, self.check_drop_file)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)

    def get_last_file(self):
        """
        获取最后一个文件
        :return: str
        """
        if len(self.drop_files):
            return self.drop_files[-1]
        else:
            return None

    def get_all_file(self):
        """
        获取所有的文件
        :return: None
        """
        return self.drop_files
