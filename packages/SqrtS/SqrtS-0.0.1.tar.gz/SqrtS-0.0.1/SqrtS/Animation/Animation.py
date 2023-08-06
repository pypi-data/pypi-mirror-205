import os
from abc import abstractmethod
from SqrtS.Core.TaskSystem import TIMES
import pygame.image
from SqrtS.tools.load_theme import unzip_file, walk_one
from SqrtS.tools._json_control import JsonReader
from SqrtS.Errors.animation_err import NotAnimationFileError, UnpackSqsaError


class Animation:
    """
    动画基础类
    """

    def __init__(self, IDname):
        self.had_been_play = False
        self.IDname = IDname
        self.surfaces_dict = {}
        self.animation_path = ""
        self.animation_name = ""
        self.setting = {}

        self.img_index = 0
        self.now_img = None

        self.pos = []

        self.alive = True

    def times_blit_task(self):
        if self.img_index + 1 < len(self.surfaces_dict):
            self.img_index += 1
            self.now_img = self.surfaces_dict[str(self.img_index)]
        else:
            self.alive = False

    @abstractmethod
    def play(self, window, pos):
        self.pos = pos
        self.now_img = self.surfaces_dict[str(self.img_index)]
        if not self.had_been_play:
            window.register_for_task(TIMES,
                                     self.times_blit_task,
                                     time_interval=self.setting["speed"], times=len(self.surfaces_dict))
            window.register_for_animation(self)
        self.had_been_play = True

    def blit_flip(self, window):
        if self.alive:
            window.get_window().blit(self.now_img, self.pos)
        else:
            window.destroy_animation(animation=self)

    def load_animation(self, path):
        if "\\" in path:
            type_ = "\\"
        else:
            type_ = "/"

        if path.split(".")[-1] == "sqsa":
            new_path = "".join(path.split(".")[:-1]) + ".zip"
            os.rename(path, new_path)
            self.animation_path = path
            self.animation_name = self.animation_path.split(type_)[-1].split(".")[0]
        else:
            raise NotAnimationFileError("您传入的路径指向的并不是一个sqsa帧动画文件！")

        target_path = ""
        for i in path.split(type_)[0:-1]:
            target_path = target_path + i + type_

        result = unzip_file(new_path, target_path)
        os.rename(new_path, path)

        if not result:
            raise UnpackSqsaError("您传入的sqsa帧动画文件可能已经损坏或者路径错误！解压失败！")
        else:
            setting_path = "".join(path.split(".")[:-1]) + type_ + "setting.json"
            self.setting = JsonReader(json_path=setting_path).read_json()
            walk_path = "".join(path.split(".")[:-1]) + type_
            for filename in walk_one(walk_path):
                if filename.split(".")[-1] in ["png", "PNG", "jpg", "JPG", "JPEG", "jpeg"]:
                    flip_name = filename.split(".")[0]
                    self.surfaces_dict[flip_name] = pygame.image.load(walk_path + filename)


class LowerAnimation:
    """
    动画基础类，但是是更加底层的
    """

    def __init__(self, IDname):
        self.had_been_play = False
        self.IDname = IDname
        self.surfaces_dict = {}
        self.animation_path = ""
        self.animation_name = ""
        self.setting = {}

        self.img_index = 0
        self.now_img = None

        self.pos = []

        self.alive = True

        self.style = "\\"

    def times_blit_task(self):
        if self.img_index + 1 < len(self.surfaces_dict):
            self.img_index += 1
            self.now_img = self.surfaces_dict[str(self.img_index)]
        else:
            self.alive = False

    @abstractmethod
    def play(self, window, pos, speed):
        self.pos = pos
        self.now_img = self.surfaces_dict[str(self.img_index)]
        if not self.had_been_play:
            window.register_for_task(TIMES,
                                     self.times_blit_task,
                                     time_interval=speed, times=len(self.surfaces_dict))
            window.register_for_animation(self)
        self.had_been_play = True

    def blit_flip(self, window):
        if self.alive:
            window.get_window().blit(self.now_img, self.pos)
        else:
            window.destroy_animation(animation=self)

    def load_animation(self, path, size=None):
        if "/" in path:
            self.style = "/"
        if size:
            for filename in walk_one(path):
                if filename.split(".")[-1] in ["png", "PNG", "jpg", "JPG", "JPEG", "jpeg"]:
                    flip_name = filename.split(".")[0]
                    self.surfaces_dict[flip_name] = pygame.transform.scale(
                        pygame.image.load(path + self.style + filename), size)
        else:
            for filename in walk_one(path):
                if filename.split(".")[-1] in ["png", "PNG", "jpg", "JPG", "JPEG", "jpeg"]:
                    flip_name = filename.split(".")[0]
                    self.surfaces_dict[flip_name] = pygame.image.load(path + self.style + filename)


if __name__ == "__main__":
    ...
