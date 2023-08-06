import win32api
import win32con
import win32gui
import pygame


def window_transparency(window):
    """
    窗口透明化函数
    :param window:Window
    :return: None
    """
    transparency_color = (20, 20, 20)  # Transparency color
    window.bind_background_color(transparency_color)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency_color), 0, win32con.LWA_COLORKEY)
