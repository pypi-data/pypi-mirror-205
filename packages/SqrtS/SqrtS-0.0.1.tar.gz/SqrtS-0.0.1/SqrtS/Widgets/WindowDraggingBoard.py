import pyautogui
from SqrtS.Expand.DraggingBoard import GlobalDraggingBoard
from SqrtS.Core.TaskSystem import ONCE
from SqrtS.Expand.WindowMove import WindowMover
from SqrtS.Widgets.Widget import Widget


class WindowDraggingBoard(Widget):
    """
    未经测试
    """
    def __init__(self, window_size, window, size, IDname):
        """

        :param window_size: [int,int]
        :param window: Window
        :param size: [int,int]
        :param IDname: str
        """
        super().__init__(size, IDname)
        self.pos = []
        self.offset_address = window.offset_address
        self.window_size = window_size
        self.dragging_board = GlobalDraggingBoard([self.window_size[0], self.offset_address], "_slide_board")
        self.dragging_board.register_for_event(window=window)
        self.dragging_board.bind_pos([0, 0])
        self.dragging_board.bind_call_slide(self._drag)

        self.window_mover = WindowMover()

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos:
        :return:
        """
        self.pos = new_pos

    def blit(self, window):
        ...

    def register_for_event(self, window):
        """
        注册时间
        :param window:
        :return:
        """
        window.register_for_task(type_=ONCE, func=self.dragging_board.update_info, time_interval=1, args=window)

    def _drag(self):
        """
        拖动
        :return:
        """
        abs_mouse_pos = pyautogui.position()
        pygame_pos = self.dragging_board.last_mouse_pos
        self.window_mover.moveto([abs_mouse_pos[0] - pygame_pos[0], abs_mouse_pos[1] - pygame_pos[1]])
