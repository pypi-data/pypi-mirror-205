from SqrtS.Widgets.Widget import Widget
import pygame


class Image(Widget):
    """
    图片控件
    """

    def __init__(self, size,
                 IDname,
                 image_path):
        """

        :param size: [int,int]
        :param IDname: str
        :param image_path: str
        """
        super().__init__(size, IDname)
        self.image_path = image_path
        self.image_sur = pygame.transform.smoothscale(pygame.image.load(image_path), self.size)
        self.pos = []

    def bind_pos(self, new_pos: list):
        """
        绑定坐标
        :param new_pos: [int,int]
        :return: None
        """
        self.pos = new_pos

    def blit(self, window):
        """
        画图
        :param window:
        :return: None
        """
        window.get_window().blit(self.image_sur, self.pos)

    def register_for_event(self, window):
        """
        None
        :param window: None
        :return: None
        """
        ...

    def reload_image(self, path):
        """
        重新导入图片
        :param path: str
        :return: None
        """
        self.image_sur = pygame.image.load(path)

    def resize_image(self, new_size):
        """
        重新更改图片大小
        :param new_size:
        :return:
        """
        self.image_sur = pygame.transform.scale(self.image_sur, new_size)


class SVGImage(Widget):
    def __init__(self, size, IDname, svg_path):
        super().__init__(size, IDname)
        self.image_path = svg_path
        self.image_sur = pygame.image.load(svg_path)
        self.pos = []

    def bind_pos(self, new_pos: list):
        self.pos = new_pos

    def blit(self, window):
        """
        画图
        :param window:
        :return: None
        """
        window.get_window().blit(self.image_sur, self.pos)

    def register_for_event(self, window):
        ...


if __name__ == "__main__":
    svg = SVGImage([100, 100], "C:\\Users\\aa\\Desktop\\svgs\\")
