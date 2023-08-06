import pygame
from SqrtS.Widgets.Widget import Widget
from SqrtS.Widgets.Button import ImageTextButton
from SqrtS.Core.event_process import MOUSEUP, MOUSEDOWN, EVERYTIME


class ListBox(Widget):
    def __init__(self, size,
                 IDname,
                 theme,
                 font,
                 style=None,
                 choose_color=(255, 0, 0),
                 background=None
                 ):
        """

        :param size: [int,int]
        :param IDname: str
        :param theme: Theme
        :param font: Font
        :param style: [(),()]
        :param choose_color:[int,int,int]
        :param background: [int,int,int]
        """
        super().__init__(size, IDname)

        self.if_this_time_call_on = None
        self.chosen = None

        self.move_out_function = None
        self.move_on_function = None
        self.up_function = None
        self.call_function = None

        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME]

        self.pos = []
        self.listbox_img_formal = pygame.transform.scale(theme.get_theme()["listbox"], size)
        self.list_box_img_chosen = pygame.transform.scale(theme.get_theme()["listbox_chosen"], size)
        self.font = font
        self.style = style

        self.list_choosing = False

        self.listbox_img_now = self.listbox_img_formal

        self.list_item = []

        self.choose_color = choose_color
        self.background = background

        self.final_choose = ""
        self.final_choose_sur = self.font.render_text(text=self.final_choose,
                                                      color=self.choose_color,
                                                      background=self.background)
        self.text_pos = []

    def _render_choose(self):
        """
        渲染选择
        :return: None
        """
        self.final_choose_sur = self.font.render_text(text=self.final_choose,
                                                      color=self.choose_color,
                                                      background=self.background)
        self._compute_text_pos(self.final_choose_sur.get_rect())

    def _compute_text_pos(self, text_rect):
        """
        计算新的文字坐标
        :param text_rect:文字对象surface
        :return: 坐标列表
        """
        x = int((self.size[0] / 2) - (text_rect[2] / 2))
        y = int((self.size[1] / 2) - (text_rect[3] / 2))
        self.text_pos = [self.pos[0] + x, self.pos[1] + y]

    def _choose_update(self, args):
        """
        绑定给最终选择的函数，被按钮调用当做回调函数
        :param args: None
        :return: None
        """
        self.final_choose = args.IDname
        self._render_choose()

    def append_item(self, item_text):
        """
        初始时调用，即在未调用register函数前
        :param item_text: str
        :return: None
        """
        btn = ImageTextButton(button_size=self.size,
                              image_list=[self.listbox_img_formal,
                                          self.listbox_img_formal,
                                          self.list_box_img_chosen],
                              IDname=f"{item_text}",
                              button_text=item_text,
                              font=self.font,
                              style=self.style)
        btn.bind_call_func(self._choose_update)
        self.list_item.append(btn)

        self._compute_items_poses()

    def append_items(self, item_texts):
        """
        初始时调用，即在未调用register函数前
        :param item_texts: list
        :return: None
        """
        for i in item_texts:
            self.append_item(i)

    def add_items(self, item_texts, window):
        """
        任何时候追加选型都可以！
        :param item_texts: list
        :param window: Window
        :return: None
        """
        for item_text in item_texts:
            btn = ImageTextButton(button_size=self.size,
                                  image_list=[self.listbox_img_formal,
                                              self.listbox_img_formal,
                                              self.list_box_img_chosen],
                                  IDname=f"{item_text}",
                                  button_text=item_text,
                                  font=self.font,
                                  style=self.style)
            btn.bind_call_func(self._choose_update)
            self.list_item.append(btn)
            self._compute_items_poses()
            btn.register_for_event(window)

    def _compute_items_poses(self):
        """
        计算选项坐标
        :return: None
        """
        index = 1
        for i in self.list_item:
            i.bind_pos([self.pos[0], self.pos[1] + self.size[1] * index])
            index += 1

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos: list
        :return: None
        """
        self.pos = new_pos

    def blit_text(self, window):
        """
        画出文字
        :param window: Window
        :return: None
        """
        if self.final_choose:
            window.get_window().blit(self.final_choose_sur, self.text_pos)

    def blit(self, window):
        """
        画图
        :param window: Window
        :return: None
        """
        window.get_window().blit(self.listbox_img_now, self.pos)
        self.blit_text(window)
        if self.list_choosing:
            for i in self.list_item:
                i.blit(window=window)

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
            self.list_choosing = True

            if self.call_function:
                self.call_function(self)
        else:
            self.list_choosing = False

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
            if self.up_function:
                self.up_function(self)
        else:
            self.list_choosing = False

    def weight_everytime_event(self, window):
        """
        每时每刻都在运行的函数为everytime函数，按钮内用于处理按钮移动上去的事件
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_pos[1] < \
                self.pos[1] + self.size[1] and not self.list_choosing:
            self.listbox_img_now = self.list_box_img_chosen
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
            self.listbox_img_now = self.listbox_img_formal

    def register_for_event(self, window):
        for i in self.list_item:
            i.register_for_event(window)
        """
        注册函数，将目标函数注册到EventProcessor中
        :param window: window对象
        :return: None
        """
        window.event_processor.register_event(MOUSEDOWN, self.check_mouse_down)
        window.event_processor.register_event(MOUSEUP, self.check_mouse_up)
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

    def get_final_choose(self):
        """
        获取最终选择，str
        :return: None
        """
        return self.final_choose

    def clear_items(self, window):
        self.list_item = []
        self.final_choose = ""
        self.final_choose_sur = self.font.render_text(text=self.final_choose,
                                                      color=self.choose_color,
                                                      background=self.background)
        self.list_choosing = False

        for i in self.list_item:
            i.destroy_widget(window=window)

    def delete_item(self, index, window):
        if len(self.list_item):
            self.list_item[index].destroy_widget(window=window)
            self.list_item.remove(self.list_item[index])
            self.list_choosing = False
