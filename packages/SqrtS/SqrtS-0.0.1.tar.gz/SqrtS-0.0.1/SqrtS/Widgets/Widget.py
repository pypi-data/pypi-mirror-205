from abc import abstractmethod
from SqrtS.Core.event_process import *


class Widget:
    """
    所有控件的基础类
    """

    def __init__(self, size, IDname, many_weights=False):
        self.size = size
        self.many_weight = many_weights
        self.IDname = IDname
        self.event_types = []
        self.widget_alive = True

    @abstractmethod
    def bind_pos(self, new_pos: list):
        ...

    @abstractmethod
    def blit(self, window):
        ...

    @abstractmethod
    def register_for_event(self, window):
        ...

    def destroy_for_event(self, window, types_):
        target_func = None
        for type_ in types_:
            if type_ == MOUSEDOWN:
                target_func = self.check_mouse_down
            elif type_ == MOUSEUP:
                target_func = self.check_mouse_up
            elif type_ == KEYDOWN:
                target_func = self.check_key_down
            elif type_ == KEYUP:
                target_func = self.check_key_up

            elif type_ == MOUSE_BUTTON_LEFT_DOWN:
                target_func = self.check_mouse_left_down
            elif type_ == MOUSE_BUTTON_LEFT_UP:
                target_func = self.check_mouse_left_up
            elif type_ == MOUSE_MID_DOWN:
                target_func = self.check_mouse_mid_down
            elif type_ == MOUSE_MID_UP:
                target_func = self.check_mouse_mid_down
            elif type_ == MOUSE_RIGHT_DOWN:
                target_func = self.check_mouse_right_down
            elif type_ == MOUSE_RIGHT_UP:
                target_func = self.check_mouse_right_up

            elif type_ == MOUSE_WHEEL_DOWN:
                target_func = self.check_mouse_wheel_down
            elif type_ == MOUSE_WHEEL_UP:
                target_func = self.check_mouse_wheel_up
            window.event_processor.destroy_event(type_, target_func)

    def destroy_widget(self, window):
        self.destroy_for_event(window, self.event_types)

        self.widget_alive = False

    def check_key_down(self, event, window):
        ...

    def check_key_up(self, event, window):
        ...

    def check_mouse_down(self, event, window):
        ...

    def check_mouse_up(self, event, window):
        ...

    def weight_everytime_event(self, window):
        ...

    def check_drop_file(self, event, window):
        ...

    def check_text_input(self, event, window):
        ...

    def process_many_weight_poses(self):
        ...

    def check_mouse_left_down(self, event, window):
        ...

    def check_mouse_left_up(self, event, window):
        ...

    def check_mouse_right_down(self, event, window):
        ...

    def check_mouse_right_up(self, event, window):
        ...

    def check_mouse_mid_down(self, event, window):
        ...

    def check_mouse_mid_up(self, event, window):
        ...

    def check_mouse_wheel_down(self, event, window):
        ...

    def check_mouse_wheel_up(self, event, window):
        ...
