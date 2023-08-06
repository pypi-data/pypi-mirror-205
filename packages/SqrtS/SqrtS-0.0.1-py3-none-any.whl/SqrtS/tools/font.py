import pygame

pygame.font.init()


def get_all_system_fonts():
    """
    返回所有可用的系统字体名称
    :return: list=[str,str,str...]
    """
    fonts = pygame.font.get_fonts()
    return fonts


class SqrtSFont:
    def __init__(self, font_size, font_name, font_theme):
        self.font_size = font_size
        self.font_name = font_name
        self.font = pygame.font.Font(font_theme.get_fonts()[font_name], font_size)

    def render_text(self, text, color, antialias=True, background=None):
        """
        渲染文字，返回文字
        :param text:文字str
        :param color:文字颜色
        :param antialias:是否抗锯齿
        :param background:背景颜色（int,int,int）
        :return:surface
        """
        return self.font.render(text, antialias, color, background)


class SystemFont:
    def __init__(self, font_size, font_name):
        self.font_size = font_size
        self.font_name = font_name
        self.font = pygame.font.SysFont(font_name, font_size)

    def render_text(self, text, color, antialias=True, background=None):
        """
        渲染文字，返回文字
        :param text:文字str
        :param color:文字颜色
        :param antialias:是否抗锯齿
        :param background:背景颜色（int,int,int）
        :return:surface
        """
        return self.font.render(text, antialias, color, background)
