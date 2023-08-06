KEYDOWN = 0
KEYUP = 1
MOUSEDOWN = 2
MOUSEUP = 3
EVERYTIME = 4
DROPFILE = 5
TEXTINPUT = 6

MOUSE_BUTTON_LEFT_DOWN = 7
MOUSE_MID_DOWN = 8
MOUSE_RIGHT_DOWN = 9

MOUSE_BUTTON_LEFT_UP = 10
MOUSE_MID_UP = 11
MOUSE_RIGHT_UP = 12

MOUSE_WHEEL_UP = 13
MOUSE_WHEEL_DOWN = 14


class EventProcessor:
    def __init__(self):
        self.key_down_pool = []
        self.key_up_pool = []
        self.mouse_up_pool = []
        self.mouse_down_pool = []
        self.everytime_pool = []
        self.dropfile_pool = []
        self.input_pool = []

        self.mouse_left_down_pool = []
        self.mouse_left_up_pool = []

        self.mouse_mid_down_pool = []
        self.mouse_mid_up_pool = []

        self.mouse_right_down_pool = []
        self.mouse_right_up_pool = []

        self.mouse_wheel_down_pool = []
        self.mouse_wheel_up_pool = []

    def key_down_process(self, event, window):
        """
        刷新按下按键池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.key_down_pool:
            i(event, window)

    def key_up_process(self, event, window):
        """
        刷新抬起按键池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.key_up_pool:
            i(event, window)

    def mouse_down(self, event, window):
        """
        刷新按下鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_down_pool:
            i(event, window)

    def mouse_up(self, event, window):
        """
        刷新抬起鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_up_pool:
            i(event, window)

    def everytime_event(self, window):
        """
        刷新周期事件池
        :return: None
        """
        for i in self.everytime_pool:
            i(window)

    def drop_file_event(self, event, window):
        """
        拖拽文件事件池
        :param event: 事件
        :param window: 窗口
        :return:
        """
        for i in self.dropfile_pool:
            i(event, window)

    def text_input_event(self, event, window):
        """
        文字输入池，支持多种文字
        :param event: 事件
        :param window: 窗口
        :return: None
        """
        for i in self.input_pool:
            i(event, window)

    def register_event(self, type_, function):
        """
        注册事件，所有被注册函数都需要有一个参数：event
        :param type_: 注册类型
        :param function: 函数体
        :return: None
        """
        if type_ == KEYDOWN:
            self.key_down_pool.append(function)
        elif type_ == KEYUP:
            self.key_up_pool.append(function)
        elif type_ == MOUSEDOWN:
            self.mouse_down_pool.append(function)
        elif type_ == MOUSEUP:
            self.mouse_up_pool.append(function)
        elif type_ == EVERYTIME:
            self.everytime_pool.append(function)
        elif type_ == DROPFILE:
            self.dropfile_pool.append(function)
        elif type_ == TEXTINPUT:
            self.input_pool.append(function)

        elif type_ == MOUSE_BUTTON_LEFT_DOWN:
            self.mouse_left_down_pool.append(function)
        elif type_ == MOUSE_BUTTON_LEFT_UP:
            self.mouse_left_up_pool.append(function)

        elif type_ == MOUSE_RIGHT_DOWN:
            self.mouse_right_down_pool.append(function)
        elif type_ == MOUSE_RIGHT_UP:
            self.mouse_right_up_pool.append(function)

        elif type_ == MOUSE_MID_DOWN:
            self.mouse_mid_down_pool.append(function)
        elif type_ == MOUSE_MID_UP:
            self.mouse_mid_up_pool.append(function)

        elif type_ == MOUSE_WHEEL_DOWN:
            self.mouse_wheel_down_pool.append(function)
        elif type_ == MOUSE_WHEEL_UP:
            self.mouse_wheel_up_pool.append(function)

    def destroy_event(self, type_, function):
        """
        注销事件，传进函数体
        :param type_: 注册类型
        :param function: 函数体
        :return: None
        """
        if type_ == KEYDOWN:
            for i in self.key_down_pool:
                if i == function:
                    self.key_down_pool.remove(i)

        elif type_ == KEYUP:
            for i in self.key_up_pool:
                if i == function:
                    self.key_up_pool.remove(i)

        elif type_ == MOUSEDOWN:
            for i in self.mouse_down_pool:
                if i == function:
                    self.mouse_down_pool.remove(i)

        elif type_ == MOUSEUP:
            for i in self.mouse_up_pool:
                if i == function:
                    self.mouse_up_pool.remove(i)

        elif type_ == EVERYTIME:
            for i in self.everytime_pool:
                if i == function:
                    self.everytime_pool.remove(i)

        elif type_ == DROPFILE:
            for i in self.dropfile_pool:
                if i == function:
                    self.dropfile_pool.remove(i)

        elif type_ == TEXTINPUT:
            for i in self.input_pool:
                if i == function:
                    self.input_pool.remove(i)

        elif type_ == MOUSE_BUTTON_LEFT_DOWN:
            for i in self.mouse_left_down_pool:
                if i == function:
                    self.mouse_left_down_pool.remove(i)
        elif type_ == MOUSE_BUTTON_LEFT_UP:
            for i in self.mouse_left_up_pool:
                if i == function:
                    self.mouse_left_up_pool.remove(i)
        elif type_ == MOUSE_RIGHT_DOWN:
            for i in self.mouse_right_down_pool:
                if i == function:
                    self.mouse_right_down_pool.remove(i)
        elif type_ == MOUSE_RIGHT_UP:
            for i in self.mouse_right_down_pool:
                if i == function:
                    self.mouse_right_up_pool.remove(i)
        elif type_ == MOUSE_MID_DOWN:
            for i in self.mouse_mid_down_pool:
                if i == function:
                    self.mouse_mid_down_pool.remove(i)
        elif type_ == MOUSE_MID_UP:
            for i in self.mouse_mid_up_pool:
                if i == function:
                    self.mouse_mid_up_pool.remove(i)

        elif type_ == MOUSE_WHEEL_DOWN:
            for i in self.mouse_wheel_down_pool:
                if i == function:
                    self.mouse_wheel_down_pool.remove(i)
        elif type_ == MOUSE_WHEEL_UP:
            for i in self.mouse_wheel_up_pool:
                if i == function:
                    self.mouse_wheel_up_pool.remove(i)

    def mouse_left_down(self, event, window):
        """
        刷新按下鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_left_down_pool:
            i(event, window)

    def mouse_left_up(self, event, window):
        """
        刷新抬起鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_left_up_pool:
            i(event, window)

    def mouse_mid_down(self, event, window):
        """
        刷新按下鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_mid_down_pool:
            i(event, window)

    def mouse_mid_up(self, event, window):
        """
        刷新抬起鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_mid_up_pool:
            i(event, window)

    def mouse_right_down(self, event, window):
        """
        刷新按下鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_right_down_pool:
            i(event, window)

    def mouse_right_up(self, event, window):
        """
        刷新抬起鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_right_up_pool:
            i(event, window)

    def mouse_wheel_down(self, event, window):
        """
        刷新按下鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_wheel_down_pool:
            i(event, window)

    def mouse_wheel_up(self, event, window):
        """
        刷新抬起鼠标池
        :param window: Window
        :param event: 事件
        :return: None
        """
        for i in self.mouse_wheel_up_pool:
            i(event, window)
