import ctypes
from typing import Tuple, Callable, Any
import pygame
import threading
import clr
from System.Windows.Forms import *  # pycharm报语法错误
from System.Threading import Thread, ApartmentState, ThreadStart  # pycharm报语法错误

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')

_app = Application  # pycharm报语法错误
_user32 = ctypes.windll.user32


class _Form(object):
    pass


class WebView(object):
    def __init__(self, window: pygame.Surface, size: Tuple[int, int] = (1200, 550), url: str = '',
                 script_errors_suppressed: bool = True, menu_enabled: bool = False):

        self._width, self._height = size

        form = _Form()
        threading.Thread(target=self._get_web, args=(form, self._width, self._height)).run()

        while True:
            try:
                ie = form.web
                break
            except AttributeError:
                pass

        ie.ScriptErrorsSuppressed = script_errors_suppressed
        self.ie_hwnd = int(str(ie.Handle))
        self.x, self.y = 0, 0
        _user32.SetParent(self.ie_hwnd, pygame.display.get_wm_info()['window'])  # 嵌入窗口
        _user32.MoveWindow(self.ie_hwnd, self.x, self.y, self._width, self._height, True)  # 移动窗口

        if url != '':
            ie.Navigate(url)
        self.ie = ie
        self.ie.IsWebBrowserContextMenuEnabled = menu_enabled
        self.ie.NewWindow += self._before_window

    @staticmethod
    def _get_web(form: _Form, width: int, height: int):
        web = WebBrowser()  # pycharm报语法错误
        form.web = web
        web.Width = width
        web.Height = height

    @staticmethod
    def _before_window(sender, e):
        href = sender.Document.ActiveElement.GetAttribute('href')
        sender.Navigate(href)
        e.Cancel = True

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, set_pos: Tuple[int, int]):
        self.x, self.y = set_pos
        _user32.MoveWindow(self.ie_hwnd, self.x, self.y, self._width, self._height, True)

    def set_url(self, url: str):
        self.ie.Navigate(url)

    def show_url(self, func: Callable[[], Any]):
        self.ie.Navigating += func

    def resize(self, width: int, height: int):
        self._width, self._height = width, height
        self.ie.Width = width
        self.ie.Height = height

    def destroy(self):
        self.ie.Dispose()
        del self.ie

    def go_back(self):
        self.ie.GoBack()

    def go_forward(self):
        self.ie.GoForward()

    def refresh(self):
        self.ie.Refresh()
