import pygame


class ImageSurface:
    def __init__(self, img_path):
        """
        图片类，近似于数据类，功能较少
        :param img_path:
        """
        self.img_surface = pygame.image.load(img_path)

    def resize(self, new_size):
        """
        对当前图片进行重新设置大小
        :param new_size: 大小列表
        :return: None
        """
        return pygame.transform.scale(self.img_surface, new_size)

    def return_surface(self):
        """
        返回图片对象
        :return: None
        """
        return self.img_surface

    def reload(self, new_img_path):
        """
        重新导入图片，更新刷新图片
        :param new_img_path:
        :return:
        """
        self.img_surface = pygame.image.load(new_img_path)


class SurfaceImage:
    def __init__(self, surface):
        """
        图片类，近似于数据类，功能较少
        :param img_path:
        """
        self.img_surface = surface

    def resize(self, new_size):
        """
        对当前图片进行重新设置大小
        :param new_size: 大小列表
        :return: None
        """
        return pygame.transform.scale(self.img_surface, new_size)

    def return_surface(self):
        """
        返回图片对象
        :return: None
        """
        return self.img_surface

    def reload(self, new_img_path):
        """
        重新导入图片，更新刷新图片
        :param new_img_path:
        :return:
        """
        self.img_surface = pygame.image.load(new_img_path)
