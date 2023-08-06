# pygame.mixer.music.load()  ——  载入一个音乐文件用于播放
# pygame.mixer.music.play()  ——  开始播放音乐流
# pygame.mixer.music.rewind()  ——  重新开始播放音乐
# pygame.mixer.music.stop()  ——  结束音乐播放
# pygame.mixer.music.pause()  ——  暂停音乐播放
# pygame.mixer.music.unpause()  ——  恢复音乐播放
# pygame.mixer.music.fadeout()  ——  淡出的效果结束音乐播放
# pygame.mixer.music.set_volume()  ——  设置音量
# pygame.mixer.music.get_volume()  ——  获取音量
# pygame.mixer.music.get_busy()  ——  检查是否正在播放音乐
# pygame.mixer.music.set_pos()  ——  设置播放的位置
# pygame.mixer.music.get_pos()  ——  获取播放的位置
# pygame.mixer.music.queue()  ——  将一个音乐文件放入队列中，并排在当前播放的音乐之后
# pygame.mixer.music.set_endevent()  ——  当播放结束时发出一个事件
# pygame.mixer.music.get_endevent()  ——  获取播放结束时发送的事件
import pygame
import time
import threading
import sys


class Audio:

    def __init__(self,
                 path: str,
                 if_track_pos=False
                 ):
        """
        音乐播放器的构造函数
        """
        pygame.mixer.init()
        self.if_track_pos = if_track_pos
        self.path = path
        self.track = None
        self._load()
        self.pos = -1

    def _load(self):
        """导入MP3文件"""
        self.track = pygame.mixer.music.load(self.path)

    def play(self):
        """开始播放"""
        pygame.mixer.music.play()

    def stop_all(self):
        """停止播放"""
        pygame.mixer.music.stop()

    def unpause(self):
        """停止暂停"""
        pygame.mixer.music.unpause()

    def pause(self):
        """暂停"""
        pygame.mixer.music.pause()

    def set_volume(self, value):
        """设置音量"""
        pygame.mixer.music.set_volume(value)

    def get_busy(self):
        """获取是否正在播放音频"""
        pygame.mixer.music.get_busy()

    def queue(self, next_filename):
        """设置下一首播放什么"""
        pygame.mixer.music.queue(next_filename)

    def start_at(self, position):
        """设置开始播放的位置"""
        if self.get_busy():
            self.stop_all()
        pygame.mixer.music.play(start=position)

    def get_sound_pos(self):
        """获取当前声音的进度"""
        if self.if_track_pos:
            self.pos = int(pygame.mixer.music.get_pos() / 1000)

    def set_sound_pos(self, pos):
        """设置开始播放的位置"""
        pygame.mixer.music.set_pos(pos)


if __name__ == "__main__":
    ad = Audio(path="../../sources/target.mp3", if_track_pos=True)
    ad.play()
    ad.set_sound_pos(0)
    time.sleep(10)
    ad.stop_all()
    sys.exit(0)
