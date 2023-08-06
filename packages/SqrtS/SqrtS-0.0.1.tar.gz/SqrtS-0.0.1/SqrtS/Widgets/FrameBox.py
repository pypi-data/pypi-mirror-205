from SqrtS.Widgets.Widget import Widget
from SqrtS.Errors.widgets_error import BindPosesError
import pygame


class FrameBox(Widget):
    def __init__(self, IDname, size, background_image_path=""):
        super().__init__([0, 0], IDname)
        self.size = size

        if len(background_image_path):
            self.background_sur = pygame.transform.scale(pygame.image.load(background_image_path), size)
        else:
            self.background_sur = None

        self.pos = [0, 0]
        self.offset_pos = {}
        self.widgets = []

    def appends_widgets(self, widgets_list):
        for i in widgets_list:
            self.offset_pos[i.IDname] = []
            self.widgets.append(i)

    def bind_pos(self, new_pos: list):
        self.pos = new_pos
        try:
            for i in self.widgets:
                i.bind_pos([self.pos[0] + self.offset_pos[i.IDname][0], self.pos[1] + self.offset_pos[i.IDname][1]])
        except IndexError as e:
            raise BindPosesError("绑定坐标错误！")

    def blit(self, window):
        if self.background_sur:
            window.get_window().blit(self.background_sur, self.pos)
        for i in self.widgets:
            i.blit(window)

    def register_for_event(self, window):
        for i in self.widgets:
            i.register_for_event(window)

    def bind_widgets_poses(self, pos_dict):
        """
        为framebox内的控件绑定坐标
        :param pos_dict:
        :return:
        """
        for key in pos_dict.keys():
            for i in self.widgets:
                if i.IDname == key:
                    i.bind_pos([self.pos[0] + pos_dict[key][0], self.pos[1] + pos_dict[key][1]])
                    self.offset_pos[key] = pos_dict[key]


class LinerFrameBox(FrameBox):
    def __init__(self, IDname, size, direction="longitudinal"):
        """

        :param IDname: str
        :param size: [int,int]
        :param direction: longitudinal(纵向排列) or lateral(横向排列)
        """
        super().__init__(IDname, size)
        self.direction = direction
        self.offset_now = 0
        self.buffer_widgets = []
        self.size = [0, 0]

    def bind_widgets_poses(self, pos_dict):
        ...

    def compute_poses(self):
        if self.direction == "longitudinal":
            for i in self.buffer_widgets:
                self.offset_pos[i.IDname] = []
                self.widgets.append(i)
                i.bind_pos([self.pos[0], self.pos[1] + self.offset_now])
                self.offset_pos[i.IDname] = [self.pos[0], self.offset_now]
                self.offset_now += i.size[1]

        elif self.direction == "lateral":
            for i in self.buffer_widgets:
                self.offset_pos[i.IDname] = []
                self.widgets.append(i)
                i.bind_pos([self.pos[1] + self.offset_now, self.pos[1]])
                self.offset_pos[i.IDname] = [self.offset_now, self.pos[1]]
                self.offset_now += i.size[0]

        max_height = 0
        max_width = 0
        for i in self.widgets:
            if i.size[0] > max_width:
                max_width = i.size[0]
            if i.size[1] > max_height:
                max_height = i.size[1]

        self.size = [max_width, max_height]

    def appends_widgets(self, widgets_list):
        for i in widgets_list:
            self.buffer_widgets.append(i)

        max_height = 0
        max_width = 0
        for i in self.widgets:
            if i.size[0] > max_width:
                max_width = i.size[0]
            if i.size[1] > max_height:
                max_height = i.size[1]

        self.size = [max_width, max_height]
