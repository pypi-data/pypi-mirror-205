import pygame
import os
from SqrtS.Widgets.Button import ImageButton
from SqrtS.Widgets.Text import Texts


class FalseWindow:
    """
    闲的没事写的，忘记删了
    """
    def __init__(self, true_window):
        self.screen = true_window.get_window()

    def get_window(self):
        """
        获取窗口
        :return:
        """
        return self.screen


class WindowBorder:
    """
    基础窗口框
    """
    def __init__(self, theme,
                 border_size: list,
                 window,
                 font,
                 icon_path=None,
                 icon_size=(25, 25),
                 title="SqrtS GUI",
                 title_color=(255, 255, 255),
                 title_background=None,
                 button_length=30,
                 button_interval=3, ):
        """
        参数
        :param theme: Theme
        :param border_size:[int,int]
        :param window: Window
        :param font: SqrtSFont
        :param icon_path: str
        :param icon_size: [int,int]
        :param title: str
        :param title_color:[int,int,int]
        :param title_background: [int,int,int]
        :param button_length: int
        :param button_interval: int
        """
        self.pos = (0, 0)

        self.title_color = title_color
        self.title_background = title_background
        self.icon_size = icon_size

        self.font = font
        self.title = title
        self.title_sur = self.font.render_text(text=self.title, color=title_color, background=title_background)
        if not icon_path:
            self.icon_path = pygame.transform.scale(theme.get_theme()["formal_icon"], icon_size)
        else:
            self.icon_path = pygame.transform.scale(pygame.image.load(icon_path), icon_size)

        self.background = pygame.transform.scale(theme.get_theme()["border"], border_size)
        self.close_btn_img_list = [
            theme.get_theme()["kill_window"],
            theme.get_theme()["kill_window_click"],
            theme.get_theme()["kill_window_chosen"]
        ]
        self.cancel_btn_img_list = [
            theme.get_theme()["cancel"],
            theme.get_theme()["cancel_click"],
            theme.get_theme()["cancel_chosen"]
        ]
        self.close_btn = ImageButton(button_size=[button_length, border_size[1]], image_list=self.close_btn_img_list,
                                     IDname="close")
        self.min_button = ImageButton(button_size=[button_length, border_size[1]], image_list=self.cancel_btn_img_list,
                                      IDname="cancel")
        self.close_btn.bind_call_func(self._close)
        self.min_button.bind_call_func(self._iconify_window)

        self.close_btn.bind_pos([window.get_window_size()[0] - self.close_btn.size[0], 0])
        self.min_button.bind_pos(
            [window.get_window_size()[0] - self.close_btn.size[0] - button_interval - self.min_button.size[0], 0])

        self.close_btn.register_for_event(window)
        self.min_button.register_for_event(window)

    @staticmethod
    def _iconify_window(args):
        """
        最小化窗口的函数
        :param args: 固定，无实意
        :return: None
        """
        pygame.display.iconify()

    @staticmethod
    def _close(args):
        """
        内置关闭函数
        :param args:无实意
        :return: None
        """
        os._exit(0)

    def set_window_title(self, title):
        """
        设置窗口标题
        :param title: 标题str
        :return: None
        """
        self.title = title
        self.title_sur = self.font.render_text(text=self.title, color=self.title_color,
                                               background=self.title_background)

    def blit_border(self, window):
        """
        画出窗口框
        :param window:Window
        :return: None
        """
        window.get_window().blit(self.background, self.pos)
        screen = window.get_window()
        self.close_btn.blit(window)
        self.min_button.blit(window)
        self._blit_title(screen)
        self._blit_icon(screen)

    def _blit_title(self, screen):
        """
        内部函数，画出题目
        :param screen: pygame.surface
        :return: None
        """
        screen.blit(self.title_sur, (self.icon_size[0] + 3, 3))

    def _blit_icon(self, screen):
        """
        内部函数，画出图标图片
        :param screen: pygame.surface
        :return: None
        """
        screen.blit(self.icon_path, (1, 1))


class CustomizedWindowBorder:
    """
    自定义窗口边框
    """
    def __init__(self, theme,
                 border_size: list,
                 if_transparency=False):
        """
        参数
        :param theme:Theme
        :param border_size: [int,int]
        :param if_transparency: bool
        """
        self.pos = (0, 0)
        self.border_size = border_size

        self.background = pygame.transform.scale(theme.get_theme()["border"], self.border_size)

        self.widgets = []

        self.layout = None

        self.if_transparency = if_transparency

    def set_border_img(self, path):
        """
        设置边框的图片
        :param path: 图片路径
        :return: None
        """
        self.background = pygame.transform.scale(pygame.image.load(path), self.border_size)

    def bind_layout(self, layout):
        """
        绑定布局
        :param layout: Layout子类
        :return: None
        """
        self.layout = layout

    @staticmethod
    def _iconify_window(args):
        """
        最小化窗口
        :param args:固定
        :return: None
        """
        pygame.display.iconify()

    @staticmethod
    def _close(args):
        """
        内置关闭函数
        :param args:固定
        :return: None
        """
        os._exit(0)

    def blit_border(self, window):
        """
        画出窗口边框
        :param window:Window
        :return: None
        """
        if not self.if_transparency:
            window.get_window().blit(self.background, self.pos)
        else:
            window.get_window().fill(window.background_color)
        self.layout.blit_all(window)
