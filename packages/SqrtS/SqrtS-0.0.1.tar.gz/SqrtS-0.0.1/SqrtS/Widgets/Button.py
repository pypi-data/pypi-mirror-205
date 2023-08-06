import pygame
from SqrtS.tools.load_theme import Theme
from SqrtS.Core.event_process import MOUSEUP, MOUSEDOWN, EVERYTIME
from SqrtS.Widgets import Widget
from SqrtS.Core.event_process import MOUSEUP, MOUSEDOWN, EVERYTIME

BROADWISE = 0
DIRECTION = 1


class Button(Widget.Widget):
    def __init__(self, button_size: list,
                 button_text: str,
                 theme: Theme,
                 font,
                 IDname: str,
                 style=None,
                 ):
        """

        :param button_size: [int,int]
        :param button_text: str
        :param theme: Theme
        :param font: SqrtSFont
        :param IDname: str
        :param style: [(int,int,int),(int,int,int)]
        """
        super().__init__(size=button_size, many_weights=False, IDname=IDname)
        if style is None:
            self.style = [(0, 0, 255), True, None]
        else:
            self.style = style

        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME]

        self.IDname = IDname

        self.button_text = button_text
        self.button_size = button_size

        # 获取按钮图像
        if theme is not None:
            self.button_formal = theme.get_theme()["button"]
            self.button_click = theme.get_theme()["button_click"]
            self.button_chosen = theme.get_theme()["button_chosen"]

        # 重新更改按钮大小
        self.button_formal = pygame.transform.scale(self.button_formal, button_size)
        self.button_click = pygame.transform.scale(self.button_click, button_size)
        self.button_chosen = pygame.transform.scale(self.button_chosen, button_size)
        self.button_img = self.button_formal
        # 设置按钮的坐标属性
        self.pos = []
        # 定义字体
        self.font = font
        # 按钮文本surface
        self.text_sur = None
        self.text_pos = [0, 0]
        self.text_sur = self.font.render_text(self.button_text, self.style[0], self.style[1], self.style[2])
        self.text_sur_size = self.text_sur.get_rect()

        self.call_function = None
        self.up_function = None
        self.move_on_function = None
        self.move_out_function = None

        self.if_this_time_call_on = False
        self.click = False
        self.chosen = False

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.button_img = self.button_click
            self.click = True
            if self.call_function:
                self.call_function(self)
        else:
            self.click = False

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.button_img = self.button_formal
            self.click = False
            if self.up_function:
                self.up_function(self)
        else:
            self.click = False

    def weight_everytime_event(self, window):
        """
        每时每刻都在运行的函数为everytime函数，按钮内用于处理按钮移动上去的事件
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.button_size[1] and not self.click:
            self.button_img = self.button_chosen
            self.chosen = True
            if self.move_on_function and not self.if_this_time_call_on:
                self.move_on_function(self)
                self.if_this_time_call_on = True
        elif self.chosen:
            if self.move_out_function:
                self.move_out_function(self)
            self.chosen = False
            self.if_this_time_call_on = False
        else:
            self.button_img = self.button_formal

    def bind_pos(self, new_pos):
        """
        绑定新的按钮坐标
        :param new_pos:list
        :return: None
        """
        self.pos = new_pos
        if self.text_sur is not None:
            self._compute_text_pos(self.text_sur.get_rect())

    def register_for_event(self, window):
        """
        注册函数，将目标函数注册到EventProcessor中
        :param window: window对象
        :return: None
        """
        window.event_processor.register_event(MOUSEDOWN, self.check_mouse_down)
        window.event_processor.register_event(MOUSEUP, self.check_mouse_up)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)

    def _compute_text_pos(self, text_rect):
        """
        计算新的文字坐标
        :param text_rect:文字对象surface
        :return: 坐标列表
        """
        x = int((self.button_size[0] / 2) - (text_rect[2] / 2))
        y = int((self.button_size[1] / 2) - (text_rect[3] / 2))
        self.text_pos = [self.pos[0] + x, self.pos[1] + y]

    def blit_text(self, window):
        """
        画出控件的文本
        :return:None
        """
        window.get_window().blit(self.text_sur, self.text_pos)

    def blit(self, window):
        """
        画出控件
        :param window:窗口类
        :return: None
        """
        window.get_window().blit(self.button_img, self.pos)
        self.blit_text(window)

    def reset_text(self, new_text, new_style):
        """
        重设按钮文字大小
        :param new_text:更新的文字
        :param new_style: 更新的样式[颜色元组，是否抗锯齿，背景颜色（没有可设为None）]
        :return: None
        """
        self.button_text = new_text
        self.style = new_style
        self.text_sur = self.font.render_text(self.button_text, self.style[0], self.style[1], self.style[2])
        self.text_sur_size = self.text_sur.get_rect()

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


class ImageButton(Button):
    """
    图片按钮，继承自Button
    """

    def __init__(self, button_size: list,
                 image_list: list,
                 IDname: str):
        """
        图片按钮，用于创建没有文字，只有图片的按钮
        :param button_size: 按钮的大小
        :param image_list: ImageSurface对象的列表，第一个元素为正常时候的图片，第二个元素为按下时的图片，第三个元素为选中但不按下是的图片
        """
        self.widget_alive = True
        self.many_weight = False
        self.size = button_size
        self.button_size = button_size
        self.text_sur = None
        self.text_pos = None
        self.text_sur_size = None
        self.button_text = None
        self.IDname = IDname
        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME]

        # 获取按钮图像
        self.button_formal = image_list[0]
        self.button_click = image_list[1]
        self.button_chosen = image_list[2]
        # 重新更改按钮大小
        if not type(self.button_formal) == pygame.Surface:
            self.button_formal = pygame.transform.scale(self.button_formal.return_surface(), button_size)
            self.button_click = pygame.transform.scale(self.button_click.return_surface(), button_size)
            self.button_chosen = pygame.transform.scale(self.button_chosen.return_surface(), button_size)
            self.button_img = self.button_formal
        else:
            self.button_formal = pygame.transform.scale(self.button_formal, button_size)
            self.button_click = pygame.transform.scale(self.button_click, button_size)
            self.button_chosen = pygame.transform.scale(self.button_chosen, button_size)
            self.button_img = self.button_formal
        # 设置按钮的坐标属性
        self.pos = []

        self.call_function = None
        self.up_function = None
        self.move_on_function = None
        self.move_out_function = None

        self.if_this_time_call_on = False
        self.click = False
        self.chosen = False

    def _compute_text_pos(self, text_rect):
        ...

    def blit_text(self, window):
        ...

    def reset_text(self, new_text, new_style):
        ...


class ImageTextButton(ImageButton):
    def __init__(self, button_size: list,
                 image_list: list,
                 IDname: str,
                 button_text,
                 font,
                 style=None):
        """

        :param button_size: [int,int]
        :param image_list: [IS,IS,IS]
        :param IDname: str
        :param button_text:str
        :param font: SqrtSSFont
        :param style: [(),()]
        """
        super().__init__(button_size, image_list, IDname)
        if style is None:
            self.style = [(0, 0, 255), True, None]
        else:
            self.style = style
        self.button_text = button_text
        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME]
        self.font = font
        # 按钮文本surface
        self.text_sur = None
        self.text_pos = [0, 0]
        self.text_sur = self.font.render_text(self.button_text, self.style[0], self.style[1], self.style[2])
        self.text_sur_size = self.text_sur.get_rect()

    def _compute_text_pos(self, text_rect):
        """
        计算新的文字坐标
        :param text_rect:文字对象surface
        :return: 坐标列表
        """
        x = int((self.button_size[0] / 2) - (text_rect[2] / 2))
        y = int((self.button_size[1] / 2) - (text_rect[3] / 2))
        self.text_pos = [self.pos[0] + x, self.pos[1] + y]

    def blit_text(self, window):
        """
        画出控件的文本
        :return:None
        """
        window.get_window().blit(self.text_sur, self.text_pos)

    def reset_text(self, new_text, new_style):
        """
        重设按钮文字大小
        :param new_text:更新的文字
        :param new_style: 更新的样式[颜色元组，是否抗锯齿，背景颜色（没有可设为None）]
        :return: None
        """
        self.button_text = new_text
        self.style = new_style
        self.text_sur = self.font.render_text(self.button_text, self.style[0], self.style[1], self.style[2])
        self.text_sur_size = self.text_sur.get_rect()


class CheckBox(ImageButton):
    def __init__(self,
                 button_size: list,
                 theme: Theme,
                 IDname: str,
                 image_list=None
                 ):
        """

        :param button_size: [int,int]
        :param theme: Theme
        :param IDname: str
        :param image_list:[IS,IS,IS]
        """

        if not image_list:
            image_list = [
                theme.get_theme()["checkbox"],
                theme.get_theme()["checkbox_click"],
                theme.get_theme()["checkbox_chosen"]
            ]
        else:
            image_list = image_list

        super().__init__(button_size=button_size, image_list=image_list, IDname=IDname)

        self.if_chose = False

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.click = True
            self.if_chose = not self.if_chose
            if self.if_chose:
                self.button_img = self.button_click
            else:
                self.button_img = self.button_chosen
            if self.call_function:
                self.call_function(self)
        else:
            self.click = False

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.click = False
            if self.up_function:
                self.up_function(self)
        else:
            self.click = False

    def weight_everytime_event(self, window):
        """
        每时每刻都在运行的函数为everytime函数，按钮内用于处理按钮移动上去的事件
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.button_size[1] and not self.click and not self.if_chose:
            self.button_img = self.button_chosen
            self.chosen = True
            if self.move_on_function and not self.if_this_time_call_on:
                self.move_on_function()
                self.if_this_time_call_on = True
        elif self.click:
            ...
        elif self.chosen:
            if self.move_out_function:
                self.move_out_function()
            self.chosen = False
            self.if_this_time_call_on = False
        elif self.if_chose:
            ...
        else:
            self.button_img = self.button_formal
            self.click = False


class _RadioButton(ImageButton):
    def __init__(self,
                 button_size: list,
                 theme: Theme,
                 group,
                 IDname: str,
                 index: int):
        """

        :param button_size: [int,int]
        :param theme: Theme
        :param group: SqrtSRadioButtonGroup
        :param IDname: str
        :param index: int
        """
        self.radiobutton_group = group
        self.index = index
        image_list = [
            theme.get_theme()["radiobutton"],
            theme.get_theme()["radiobutton_click"],
            theme.get_theme()["radiobutton_chosen"]
        ]

        super().__init__(button_size=button_size, image_list=image_list, IDname=IDname)
        self.if_chose_radio = False

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.click = True
            self.if_chose_radio = True
            for i in self.radiobutton_group.radio_buttons:
                if i.index != self.index and i.if_chose_radio:
                    i.if_chose_radio = False
                    i.button_img = i.button_formal
                    self.radiobutton_group.final_chose = self.index
            if self.if_chose_radio:
                self.button_img = self.button_click
            else:
                self.button_img = self.button_chosen
            if self.call_function:
                self.call_function(self)
        else:
            self.click = False

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.click = False
            if self.up_function:
                self.up_function()
        else:
            self.click = False

    def weight_everytime_event(self, window):
        """
        每时每刻都在运行的函数为everytime函数，按钮内用于处理按钮移动上去的事件
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.button_size[1] and not self.click and not self.if_chose_radio:
            self.button_img = self.button_chosen
            self.chosen = True
            if self.index != self.radiobutton_group.final_chose and self.if_chose_radio:
                self.if_chose_radio = False
                self.button_img = self.button_formal
            if self.move_on_function and not self.if_this_time_call_on:
                self.move_on_function()
                self.if_this_time_call_on = True
        elif self.click:
            ...
        elif self.chosen:
            if self.move_out_function:
                self.move_out_function()
            self.chosen = False
            self.if_this_time_call_on = False
        elif self.if_chose_radio:
            ...
        else:
            self.button_img = self.button_formal


class SqrtSRadioButtonGroup(Widget.Widget):
    def __init__(self,
                 button_numbers,
                 button_size: list,
                 theme: Theme,
                 IDname: str,
                 default=0,
                 padding=5):
        self.button_size = button_size
        self.button_numbers = button_numbers
        self.radio_buttons = [_RadioButton(button_size, theme, self, IDname + str(i), i) for i in range(button_numbers)]
        self.final_chose = default
        self.radio_buttons[default].if_chose_radio = True
        self.pos = []
        self.padding = padding
        self.call_function = None
        self.up_function = None
        self.move_on_function = None
        self.move_out_function = None

        super().__init__(button_size, many_weights=True, IDname=IDname)

    def blit(self, window):
        for i in self.radio_buttons:
            i.blit(window)

    def register_for_event(self, window):
        for i in self.radio_buttons:
            i.register_for_event(window)

    def bind_pos(self, new_pos: list):
        """
        绑定新的按钮坐标
        :param new_pos:list
        :return: None
        """
        self.pos = new_pos
        self.update_radio_buttons_pos()

    def bind_call_func(self, func):
        """
        绑定回调函数
        :param func:函数体
        :return: None
        """
        self.call_function = func
        for i in self.radio_buttons:
            i.bind_call_func(self.call_function)

    def bind_up_func(self, func):
        """
        绑定结束函数
        :param func:函数体
        :return: None
        """
        self.up_function = func
        for i in self.radio_buttons:
            i.bind_call_func(self.up_function)

    def bind_on_func(self, func):
        """
        绑定鼠标一上去的函数
        :param func:函数体
        :return: None
        """
        self.move_on_function = func
        for i in self.radio_buttons:
            i.bind_call_func(self.move_on_function)

    def bind_out_func(self, func):
        """
        绑定鼠标一出去的函数
        :param func:函数体
        :return: None
        """
        self.move_out_function = func
        for i in self.radio_buttons:
            i.bind_call_func(self.move_out_function)

    def update_radio_buttons_pos(self):
        for index, i in enumerate(self.radio_buttons):
            i_pos = [
                self.pos[0],
                self.pos[1] + (self.button_size[1] + self.padding) * index,
            ]
            i.bind_pos(i_pos)
        self.pos = self.radio_buttons[-1].pos
        self.size = [self.button_size[0], (self.button_size[1] + self.padding) * self.button_numbers]

    def process_many_weight_poses(self):
        self.size = [self.size[0], (self.size[1] + self.padding) * self.button_numbers]


class SwitchButton1(CheckBox):
    def __init__(self, button_size: list,
                 theme: Theme,
                 IDname: str):
        """

        :param button_size: [int,int]
        :param theme: Theme
        :param IDname: str
        """
        image_list = [
            theme.get_theme()["switch"],
            theme.get_theme()["switch_click"],
            theme.get_theme()["switch"]
        ]
        self.IDname = IDname
        super().__init__(button_size, theme, image_list=image_list, IDname=IDname)


class SwitchButton2(CheckBox):
    def __init__(self, button_size: list,
                 theme: Theme,
                 IDname: str):
        """

        :param button_size: [int,int]
        :param theme: Theme
        :param IDname: str
        """
        image_list = [
            theme.get_theme()["switch2"],
            theme.get_theme()["switch2_click"],
            theme.get_theme()["switch2"]
        ]
        self.IDname = IDname
        super().__init__(button_size, theme, image_list=image_list, IDname=IDname)


# ——————————————————————不确定——————————————————————
class _SlideButton(ImageButton):
    def __init__(self, button_size,
                 img_list,
                 limit_direction,
                 IDname: str):
        super().__init__(button_size, img_list, IDname)
        self.pos = []
        self.motion_range = []
        self.move_length = 0
        self.limit_forward = limit_direction
        if limit_direction == 0:
            self.other_direction = 1
        else:
            self.other_direction = 0

    def blit(self, window):
        window.get_window().blit(self.button_img, self.pos)

    def bind_pos(self, new_pos):
        self.pos = new_pos

    def bind_move_length(self, pos, length):
        motion_range = [pos[0], pos[1] + length]
        self.move_length = length
        self.motion_range = motion_range

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.button_img = self.button_click
            self.click = True
            if self.call_function:
                self.call_function(self)

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.button_size[1]:
            self.button_img = self.button_formal
            self.click = False
            if self.up_function:
                self.up_function(self)

    def weight_everytime_event(self, window):
        """
        每时每刻都在运行的函数为everytime函数，按钮内用于处理按钮移动上去的事件
        :return: None
        """
        self.check_pos()
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.button_size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.button_size[1] and not self.click:
            self.button_img = self.button_chosen
            self.chosen = True
            if self.move_on_function and not self.if_this_time_call_on:
                self.move_on_function(self)
                self.if_this_time_call_on = True
        elif self.click:
            if not self.pos[self.limit_forward] < mouse_pos[self.limit_forward] < self.pos[self.limit_forward] + \
                   self.size[self.limit_forward]:
                self.click = False
            if not self.pos[self.other_direction] < mouse_pos[self.other_direction] < self.pos[self.other_direction] + \
                   self.size[self.other_direction]:
                self.click = False
            if self.motion_range[0] < mouse_pos[self.limit_forward] < self.motion_range[1]:
                self.pos[self.limit_forward] = mouse_pos[self.limit_forward] - int(self.size[self.limit_forward] / 2)

        elif self.chosen:
            if self.move_out_function:
                self.move_out_function(self)
            self.chosen = False
            self.if_this_time_call_on = False
        else:
            self.button_img = self.button_formal

    def check_pos(self):
        if self.pos[0] < self.motion_range[0]:
            self.pos[0] = self.motion_range[0]
        if self.pos[0] > self.motion_range[1] - self.button_size[0]:
            self.pos[0] = self.motion_range[1] - self.button_size[0]

    def get_pos(self):
        """获取坐标"""
        return self.pos

    def get_move_length(self):
        """
        获得移动长度
        :return:
        """
        return self.move_length
