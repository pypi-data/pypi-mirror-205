import win32con
import win32gui  # 界面


def get_hwnd(name):
    """
    获取窗口权柄
    :param name: 窗口名称
    :return: 窗口权柄int
    """
    ck = 0

    def get_all_hwnd(hwnd, mouse):
        nonlocal ck
        hwnd_title = dict()
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
        for h, t in hwnd_title.items():
            if t == name:
                ck = h

    win32gui.EnumWindows(get_all_hwnd, 0)

    return ck


def _get_window_pos(hwnd):
    """
    获得窗口坐标
    :param hwnd:窗口权柄
    :return: pos_list
    """
    x, y, _, _ = win32gui.GetWindowRect(hwnd)
    return [x, y]


class WindowMover:
    """
    窗口移动器
    """
    def __init__(self):
        """
        None_param
        """
        self.title = None
        self.size = None
        self.ck = None

    def update(self, window):
        """
        更新坐标，内部函数
        :param window: Window
        :return: None
        """
        self.title = window.title
        self.size = window.get_real_window_size()
        self.ck = get_hwnd(self.title)

    def moveto(self, new_pos):
        """
        移动到坐标
        :param new_pos:[int,int]
        :return: None
        """
        win32gui.SetWindowPos(self.ck,
                              win32con.HWND_TOPMOST,  # 设置的窗口位置，最上面
                              new_pos[0],
                              new_pos[1],  # y坐标
                              self.size[0],  # 窗口长度
                              self.size[1],  # 窗口宽度
                              win32con.SWP_SHOWWINDOW  # 显示窗口
                              )

    def get_window_pos(self):
        """
        获取窗口坐标
        :return: pos
        """
        return _get_window_pos(self.ck)


if __name__ == "__main__":
    ...
