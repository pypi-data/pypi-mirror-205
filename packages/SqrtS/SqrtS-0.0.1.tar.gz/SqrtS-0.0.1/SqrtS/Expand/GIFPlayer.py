from PIL import Image
import os
from SqrtS.Animation.LoopAnimation import LowerLoopAnimation


class GIFSplit:

    def __init__(self, file_name):
        self.file_name = file_name  # 传入的文件名
        self.dir_name = self.file_name[:-4]  # 根据文件名创建存放分帧图片的文件夹
        self.gif_path = os.path.join(os.path.dirname(__file__), file_name)  # 拼接图片文件的完整路径（仅限同一文件夹内）
        self.make_dir()

        self.file_exist = False

    def make_dir(self):
        """用于创建存放分帧图片的文件夹"""
        try:
            os.mkdir(self.dir_name)
        except FileExistsError as e:
            self.file_exist = True

    def framing_test(self):
        """GIF图片分帧"""
        if not self.file_exist:
            img = Image.open(self.gif_path)
            try:
                while True:
                    curr = img.tell()
                    name = os.path.join(self.dir_name, '%s.png' % str(curr))
                    img.save(name)
                    img.seek(curr + 1)
            except Exception as e:
                pass

    def get_avg_fps(self):
        """
        获取PIL GIF的频率
        :return: None
        """
        pio = Image.open(self.file_name)
        pio.seek(0)
        frames = duration = 0
        while True:
            try:
                frames += 1
                duration += pio.info['duration']
                pio.seek(pio.tell() + 1)
            except EOFError:
                return int(frames / duration * 1000)


class GIFAnimation:
    def __init__(self, gif_path, IDname, size=None):
        self.gif_split = GIFSplit(gif_path)
        self.gif_split.framing_test()
        self.fps = 1 / self.gif_split.get_avg_fps()
        self.IDname = IDname
        self.animation = LowerLoopAnimation(IDname=IDname)
        self.animation.load_animation(self.gif_split.dir_name, size=size)

    def play(self, window, pos):
        self.animation.play(window, pos, self.fps)

    def stop(self, window):
        self.animation.stop(window)

    def pause(self, window):
        self.animation.pause(window)

    def unpause(self, window, pos):
        self.animation.unpause(window, pos, self.fps)


if __name__ == '__main__':
    gf = GIFSplit('C:\\Users\\aa\\PycharmProjects\\SqrtSGUI\\sources\\target2.gif')
    print(gf.get_avg_fps())
