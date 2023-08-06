from SqrtS.Widgets.Label import LineLabel, Label
from SqrtS.Widgets.FrameBox import FrameBox
from SqrtS.Widgets.Widget import Widget
from SqrtS.Core.TaskSystem import TIMES
import pygame


class Bubble(Widget):
    def __init__(self, size,
                 theme,
                 title_font,
                 message_font,
                 title,
                 message,
                 IDname,
                 title_color=(255, 255, 255),
                 message_color=(255, 255, 255),
                 title_background=None,
                 message_background=None):
        """

        :param size: []
        :param theme: Theme
        :param title_font: SqrtFont
        :param message_font: SqrtFont
        :param title: str
        :param message: str
        :param IDname: str
        :param title_color:str
        :param message_color:(int,int,int)
        :param title_background: (int,int,int)
        :param message_background: (int,int,int)
        """
        super().__init__(size, IDname)
        line_length = int(size[0] / message_font.font_size)
        self.alive = True
        self.pos = []
        self.size = size
        self.IDname = IDname
        self.bubble_img = pygame.transform.scale(theme.get_theme()["bubble"], size)
        self.frame_box = FrameBox("framebox>" + IDname)

        self.title_label = Label(title, title_color, title_font, "label>" + self.IDname, background=title_background)
        self.message_label = LineLabel(message, message_color, message_font, line_length, "label2>" + IDname,
                                       background=message_background)

        self.frame_box.appends_widgets([self.title_label, self.message_label])
        self.frame_box.bind_widgets_poses({"label>" + self.IDname: [10, 10], "label2>" + self.IDname: [10, 50]})

    def bind_pos(self, new_pos: list):
        self.pos = new_pos
        self.frame_box.bind_pos(self.pos)

    def blit(self, window):
        window.get_window().blit(self.bubble_img, self.pos)
        self.frame_box.blit(window)

    def register_for_event(self, window):
        self.frame_box.register_for_event(window)
        window.register_for_task(TIMES, self.update, args=window,times=10)

    def update(self, window):
        ...

    def raise_bubble(self, window):
        window_size = window.get_window_size()
        self.bind_pos([window_size[0] - self.size[0], window_size[1]])
