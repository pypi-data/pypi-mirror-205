import pygame
from SqrtS.Widgets.Widget import Widget
from SqrtS.Core.event_process import MOUSEUP, MOUSEDOWN, EVERYTIME, KEYDOWN, TEXTINPUT, MOUSE_BUTTON_LEFT_DOWN, \
    MOUSE_BUTTON_LEFT_UP
from SqrtS.Core.TaskSystem import INFINITE

# 按键映射字典表
KEYMAP = {
    pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f",
    pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l",
    pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r",
    pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x",
    pygame.K_y: "y", pygame.K_z: "z",

    pygame.K_KP0: "0", pygame.K_KP1: "1", pygame.K_KP2: "2", pygame.K_KP3: "3", pygame.K_KP4: "4",
    pygame.K_KP5: "5", pygame.K_KP6: "6", pygame.K_KP7: "7", pygame.K_KP8: "8", pygame.K_KP9: "9",

    pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5",
    pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9",

    pygame.K_TAB: "    ", pygame.K_COMMA: ",", pygame.K_PERIOD: ".", pygame.K_SLASH: "/", pygame.K_SEMICOLON: ";",
    pygame.K_BACKQUOTE: "`", pygame.K_QUOTE: "'", pygame.K_SPACE: " ",
    pygame.K_LEFTBRACKET: "[", pygame.K_RIGHTBRACKET: "]", pygame.K_BACKSLASH: "\\",

    pygame.K_PLUS: "+", pygame.K_MINUS: "-", pygame.K_EQUALS: "=",

    pygame.K_KP_MULTIPLY: "*", pygame.K_KP_PLUS: "+", pygame.K_KP_MINUS: "-", pygame.K_KP_EQUALS: "=",
    pygame.K_KP_DIVIDE: "/", pygame.K_KP_PERIOD: "."
}

# 热键映射字典表
HOTKEY = [
    pygame.K_LSHIFT,
    pygame.K_RSHIFT,
    pygame.K_LCTRL,
    pygame.K_RCTRL,
    pygame.K_LALT,
    pygame.K_RALT
]

# 大写转换对应表
UperCheck = {
    pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D", pygame.K_e: "E", pygame.K_f: "F",
    pygame.K_g: "G", pygame.K_h: "H", pygame.K_i: "I", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L",
    pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O", pygame.K_p: "P", pygame.K_q: "Q", pygame.K_r: "R",
    pygame.K_s: "S", pygame.K_t: "T", pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X",
    pygame.K_y: "Y", pygame.K_z: "Z",

    pygame.K_0: ")", pygame.K_1: "!", pygame.K_2: "@", pygame.K_3: "#", pygame.K_4: "$", pygame.K_5: "%",
    pygame.K_6: "^", pygame.K_7: "&", pygame.K_8: "*", pygame.K_9: "(",

    pygame.K_COMMA: "<", pygame.K_PERIOD: ">", pygame.K_SLASH: "?", pygame.K_SEMICOLON: ":",
    pygame.K_BACKQUOTE: "~", pygame.K_QUOTE: "\"",
    pygame.K_LEFTBRACKET: "{", pygame.K_RIGHTBRACKET: "}", pygame.K_BACKSLASH: "|",

    pygame.K_MINUS: "_", pygame.K_EQUALS: "+",

}


def check_hotkey(keys):
    """
    检测是否是热键
    :param keys: []
    :return: bool
    """
    for i in HOTKEY:
        if keys[i]:
            return True
    return False


class TextInput(Widget):
    """
    输入框基类
    """

    def __init__(self,
                 size,
                 IDname,
                 theme,
                 font,
                 text_color=(255, 255, 255),
                 text_background=None,
                 cursor_color=(255, 0, 0)):
        """

        :param size: [int,int]
        :param IDname: str
        :param theme: Theme
        :param font: Font
        :param text_color:[int,int,int]
        :param text_background: [int,int,int]
        :param cursor_color: [int,int,int]
        """
        super().__init__(size, IDname)
        self.up_function = None
        self.call_function = None
        self.text_color = text_color
        self.text_background = text_background
        self.cursor_color = cursor_color
        self.size = size
        self.pos = [0, 0]
        self.font = font

        self.formal_input_image = pygame.transform.scale(theme.get_theme()["formal_input"], self.size)
        self.chosen_input_image = pygame.transform.scale(theme.get_theme()["chosen_input"], self.size)

        self.input_img = self.formal_input_image

        self.input_text_list = []

        self.alive = False

        self.hot_key_dict = {}

        self.cursor_pos = [0, 0]
        self.cursor_if_blit = False
        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME, KEYDOWN]

    def return_input_text(self):
        """
        返回现在有的文字
        :return: None
        """
        str_text = ""
        for i in self.input_text_list:
            str_text += i
        return str_text

    def clear_text(self):
        """
        清空文字
        :return:None
        """
        self.input_text_list = []
        self.cursor_pos = self.pos

    def _compute_cursor_pos(self, rect):
        """
        重新计算光标坐标
        :param rect:
        :return:
        """
        self.cursor_pos = [self.pos[0] + rect[2], self.pos[1]]

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos:[]
        :return:
        """
        self.pos = new_pos
        self.cursor_pos = new_pos

    def _blit_cursor(self, screen):
        """
        光标绘画
        :return:NONE
        """
        if self.cursor_if_blit and self.alive:
            start_pos = [self.cursor_pos[0], self.cursor_pos[1] + 5]
            end_pos = [self.cursor_pos[0], self.cursor_pos[1] + self.size[1] - 5]
            pygame.draw.line(screen, self.cursor_color, start_pos, end_pos)

    def _change_cursor(self):
        """
        被当做任务调用！
        :return: None
        """
        self.cursor_if_blit = not self.cursor_if_blit

    def render_text(self):
        """
        递归判断是否当前文字长度超出范围
        :return:
        """
        text = ""
        for i in self.input_text_list:
            text += i
        text_surface = self.font.render_text(text, self.text_color, background=self.text_background)
        self._compute_cursor_pos(text_surface.get_rect())
        return text_surface

    def blit(self, window):
        """
        绘图
        :param window:
        :return:
        """
        screen = window.get_window()
        screen.blit(self.input_img, self.pos)
        self._blit_cursor(screen)
        if len(self.input_text_list):
            screen.blit(self.render_text(), [self.pos[0], self.pos[1]])

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.input_img = self.chosen_input_image
            self.alive = True
            if self.call_function:
                self.call_function(self)
        else:
            self.alive = False

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.input_img = self.chosen_input_image
            self.alive = True
            if self.up_function:
                self.up_function(self)
        else:
            self.input_img = self.formal_input_image
            self.alive = False

    def register_for_event(self, window):
        """
        注册函数，将目标函数注册到EventProcessor中
        :param window: window对象
        :return: None
        """
        window.event_processor.register_event(MOUSEDOWN, self.check_mouse_down)
        window.event_processor.register_event(MOUSEUP, self.check_mouse_up)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)
        window.event_processor.register_event(KEYDOWN, self.check_key_down)
        # window.event_processor.register_event(KEYUP, self.check_key_up)
        window.register_for_task(INFINITE, self._change_cursor, 0.2)

    def process_ctrl_hotkey(self, key):
        """
        处理ctrl的快捷键
        :param key:
        :return:
        """
        if key == pygame.K_c:
            print("这里执行复制的操作....")
        elif key == pygame.K_v:
            print("这里执行粘贴的操作.....")
        elif key == pygame.K_x:
            print("这里执行剪切的操作.......")
        elif key == pygame.K_a:
            print("这里执行全选的操作.........")
        elif key == pygame.K_b:
            print("这里执行什么也不知道的操作....(只是cemeye想要炫耀一下这个可以随意定义快捷键的功能啦~)")

        # 这个是用来执行自定义的快捷键的（仅限有关Ctrl的）
        for i in self.hot_key_dict.keys():
            if pygame.K_LCTRL in i or pygame.K_RCTRL in i:
                if key in i:
                    self.hot_key_dict[i]()

    def process_alt_hotkey(self, key):
        """
        处理alt的快捷键
        :param key:
        :return:
        """
        # 这个是用来执行自定义的快捷键的（仅限有关alt的）
        for i in self.hot_key_dict.keys():
            if pygame.K_LALT in i or pygame.K_RALT in i:
                if key in i:
                    self.hot_key_dict[i]()

    def process_shift_hotkey(self, key):
        """
        处理shift的快捷键
        :param key:
        :return:
        """
        # 这个是用来执行自定义的快捷键的（仅限有关shift的）
        for i in self.hot_key_dict.keys():
            if pygame.K_LSHIFT in i or pygame.K_RSHIFT in i:
                if key in i:
                    self.hot_key_dict[i]()

    def check_key_down(self, event, window):
        """
        检测是否有按键按下
        :param event: Event
        :return: None
        """
        if self.alive:
            keys = pygame.key.get_pressed()
            if_hot = check_hotkey(keys)
            if not if_hot:
                try:
                    self.input_text_list.append(KEYMAP[event.key])
                except KeyError as e:
                    self.process_special_key(event.key)
            else:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    self.process_shift_hotkey(keys)
                    if event.key in UperCheck.keys():
                        self.input_text_list.append(UperCheck[event.key])
                elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    self.process_ctrl_hotkey(event.key)
                elif keys[pygame.K_LALT] or keys[pygame.K_RALT]:
                    self.process_alt_hotkey(event.key)

    def check_key_up(self, event, window):
        """
        检测按键抬起
        :param event: Event
        :return: None
        """
        ...

    def process_special_key(self, key):
        """
        处理热键的函数
        :param key:键
        :return: None
        """
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self.alive = False
            self.input_img = self.formal_input_image
        elif key == pygame.K_BACKSPACE:
            self.delete_str()
        else:
            ...

    def delete_str(self):
        """
        删除字符的函数
        :return:
        """
        self.input_text_list = self.input_text_list[:-1]


class Input(Widget):
    def __init__(self,
                 size,
                 IDname,
                 theme,
                 font,
                 text_color=(255, 255, 255),
                 text_background=None,
                 cursor_color=(255, 0, 0),
                 password=False,
                 password_char="*"):
        """

        :param size: [int,int]
        :param IDname: str
        :param theme: Theme
        :param font: Font
        :param text_color:[int,int,int]
        :param text_background: [int,int,int]
        :param cursor_color: [int,int,int]
        """
        super().__init__(size, IDname)
        self.finish_call = None
        self.change_text_func = None
        self.password = password
        self.password_char = password_char
        self.up_function = None
        self.call_function = None
        self.text_color = text_color
        self.text_background = text_background
        self.cursor_color = cursor_color
        self.size = size
        self.pos = [0, 0]
        self.font = font

        self.formal_input_image = pygame.transform.scale(theme.get_theme()["formal_input"], self.size)
        self.chosen_input_image = pygame.transform.scale(theme.get_theme()["chosen_input"], self.size)

        self.input_img = self.formal_input_image

        self.input_text_list = []

        self.alive = False

        self.hot_key_dict = {}

        self.cursor_pos = [0, 0]
        self.cursor_if_blit = False
        self.event_types = [MOUSEDOWN, MOUSEUP, EVERYTIME, KEYDOWN]

    def return_input_text(self):
        """
        返回现在有的文字
        :return: None
        """
        str_text = ""
        for i in self.input_text_list:
            str_text += i
        return str_text

    def clear_text(self):
        """
        清空文字
        :return:None
        """
        self.input_text_list = []
        self.cursor_pos = self.pos

    def _compute_cursor_pos(self, rect):
        """
        重新计算光标坐标
        :param rect:
        :return:
        """
        self.cursor_pos = [self.pos[0] + rect[2], self.pos[1]]

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos:[]
        :return:
        """
        self.pos = new_pos
        self.cursor_pos = new_pos

    def _blit_cursor(self, screen):
        """
        光标绘画
        :return:NONE
        """
        if self.cursor_if_blit and self.alive:
            start_pos = [self.cursor_pos[0], self.cursor_pos[1] + 5]
            end_pos = [self.cursor_pos[0], self.cursor_pos[1] + self.size[1] - 5]
            pygame.draw.line(screen, self.cursor_color, start_pos, end_pos)

    def _change_cursor(self):
        """
        被当做任务调用！
        :return: None
        """
        self.cursor_if_blit = not self.cursor_if_blit

    def render_text(self):
        """
        递归判断是否当前文字长度超出范围
        :return:
        """
        if not self.password:
            text = ""
            for i in self.input_text_list:
                text += i
            text_surface = self.font.render_text(text, self.text_color, background=self.text_background)
            self._compute_cursor_pos(text_surface.get_rect())
            return text_surface
        else:
            text = self.password_char * len(self.input_text_list)
            text_surface = self.font.render_text(text, self.text_color, background=self.text_background)
            self._compute_cursor_pos(text_surface.get_rect())
            return text_surface

    def blit(self, window):
        """
        绘图
        :param window:
        :return:
        """
        screen = window.get_window()
        screen.blit(self.input_img, self.pos)
        self._blit_cursor(screen)
        if len(self.input_text_list):
            screen.blit(self.render_text(),
                        [self.pos[0], self.pos[1] + int((self.size[1] - int(self.font.font_size)) / 2)])

    def check_mouse_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.input_img = self.chosen_input_image
            self.alive = True
            if self.call_function:
                self.call_function(self)
        else:
            self.alive = False

    def check_mouse_left_down(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.input_img = self.chosen_input_image
            self.alive = True
            if self.call_function:
                self.call_function(self)
        else:
            self.alive = False

    def check_mouse_left_up(self, event, window):
        """
        检测鼠标按下并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.input_img = self.chosen_input_image
            self.alive = True
            if self.up_function:
                self.up_function(self)
        else:
            self.input_img = self.formal_input_image
            self.alive = False

    def check_mouse_up(self, event, window):
        """
        检测鼠标抬起并且调用回调函数的函数（笑）
        :param event:事件
        :return:None
        """
        mouse_click_pos = pygame.mouse.get_pos()
        if self.pos[0] < mouse_click_pos[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse_click_pos[1] < \
                self.pos[1] + self.size[1]:
            self.input_img = self.chosen_input_image
            self.alive = True
            if self.up_function:
                self.up_function(self)
        else:
            self.input_img = self.formal_input_image
            self.alive = False

    def register_for_event(self, window):
        """
        注册函数，将目标函数注册到EventProcessor中
        :param window: window对象
        :return: None
        """
        # window.event_processor.register_event(MOUSEDOWN, self.check_mouse_down)
        window.event_processor.register_event(MOUSE_BUTTON_LEFT_DOWN, self.check_mouse_left_down)
        window.event_processor.register_event(MOUSE_BUTTON_LEFT_UP, self.check_mouse_left_up)
        window.event_processor.register_event(EVERYTIME, self.weight_everytime_event)
        window.event_processor.register_event(KEYDOWN, self.check_key_down)
        window.event_processor.register_event(TEXTINPUT, self.check_text_input)
        window.register_for_task(INFINITE, self._change_cursor, 0.5)

    def process_ctrl_hotkey(self, key):
        """
        处理ctrl的快捷键
        :param key:
        :return:
        """
        if key == pygame.K_c:
            print("这里执行复制的操作....")
        elif key == pygame.K_v:
            print("这里执行粘贴的操作.....")
        elif key == pygame.K_x:
            print("这里执行剪切的操作.......")
        elif key == pygame.K_a:
            print("这里执行全选的操作.........")
        elif key == pygame.K_b:
            print("这里执行什么也不知道的操作....(只是cemeye想要炫耀一下这个可以随意定义快捷键的功能啦~)")

        # 这个是用来执行自定义的快捷键的（仅限有关Ctrl的）
        for i in self.hot_key_dict.keys():
            if pygame.K_LCTRL in i or pygame.K_RCTRL in i:
                if key in i:
                    self.hot_key_dict[i]()

    def process_alt_hotkey(self, key):
        """
        处理alt的快捷键
        :param key:
        :return:
        """
        # 这个是用来执行自定义的快捷键的（仅限有关alt的）
        for i in self.hot_key_dict.keys():
            if pygame.K_LALT in i or pygame.K_RALT in i:
                if key in i:
                    self.hot_key_dict[i]()

    def process_shift_hotkey(self, key):
        """
        处理shift的快捷键
        :param key:
        :return:
        """
        # 这个是用来执行自定义的快捷键的（仅限有关shift的）
        for i in self.hot_key_dict.keys():
            if pygame.K_LSHIFT in i or pygame.K_RSHIFT in i:
                if key in i:
                    self.hot_key_dict[i]()

    def check_key_down(self, event, window):
        """
        检测是否有按键按下
        :param event: Event
        :return: None
        """
        if self.alive:
            keys = pygame.key.get_pressed()
            if_hot = check_hotkey(keys)
            self.process_special_key(event.key)
            if if_hot:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    self.process_shift_hotkey(keys)

                elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    self.process_ctrl_hotkey(event.key)
                elif keys[pygame.K_LALT] or keys[pygame.K_RALT]:
                    self.process_alt_hotkey(event.key)

    def check_text_input(self, event, window):
        if self.alive:
            for i in event.text:
                self.input_text_list.append(i)
            if self.change_text_func:
                self.change_text_func()
            self.render_text()

    def process_special_key(self, key):
        """
        处理热键的函数
        :param key:键
        :return: None
        """
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self.alive = False
            self.input_img = self.formal_input_image
            if self.finish_call:
                self.finish_call()
        elif key == pygame.K_BACKSPACE:
            self.delete_str()
        else:
            ...

    def delete_str(self):
        """
        删除字符的函数
        :return:None
        """
        self.input_text_list = self.input_text_list[:-1]
        if len(self.input_text_list) == 0:
            self.cursor_pos = self.pos

    def change_to_password_type(self, password_char="*"):
        self.password_char = password_char
        self.password = True

    def change_to_formal_type(self):
        self.password = False

    def bind_change_text_func(self, func):
        self.change_text_func = func

    def bind_finish_call(self, func):
        """
        绑定回调函数
        :param func:func
        :return: None
        """
        self.finish_call = func
