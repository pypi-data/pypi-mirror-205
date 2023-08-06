from SqrtS.Animation.Animation import Animation, LowerAnimation
from SqrtS.Core.TaskSystem import TERMINABLE_INFINITE


class LoopAnimation(Animation):
    """
    动画基础类
    """

    def __init__(self, IDname):
        super().__init__(IDname)

    def times_blit_task(self):
        if self.img_index + 1 < len(self.surfaces_dict):
            self.img_index += 1
            self.now_img = self.surfaces_dict[str(self.img_index)]
        else:
            self.img_index = 0
            self.now_img = self.surfaces_dict[str(self.img_index)]

    def play(self, window, pos):
        self.pos = pos
        self.now_img = self.surfaces_dict[str(self.img_index)]
        if not self.had_been_play:
            window.register_for_task(TERMINABLE_INFINITE,
                                     self.times_blit_task,
                                     time_interval=self.setting["speed"],
                                     task_name=self.IDname)
            window.register_for_animation(self)
        self.had_been_play = True

    def stop(self, window):
        self.alive = False
        window.task_system.destroy_terminable_infinite_task(self.IDname)

    def pause(self, window):
        window.task_system.destroy_terminable_infinite_task(self.IDname)

    def unpause(self, window, pos):
        self.had_been_play = False
        self.play(window, pos)

    def blit_flip(self, window):
        if self.alive:
            window.get_window().blit(self.now_img, self.pos)
        else:
            window.destroy_animation(animation=self)


class LowerLoopAnimation(LowerAnimation):
    def __init__(self, IDname):
        super().__init__(IDname)

    def times_blit_task(self):
        if self.img_index + 1 < len(self.surfaces_dict):
            self.img_index += 1
            self.now_img = self.surfaces_dict[str(self.img_index)]
        else:
            self.img_index = 0
            self.now_img = self.surfaces_dict[str(self.img_index)]

    def play(self, window, pos, speed):
        self.pos = pos
        self.now_img = self.surfaces_dict[str(self.img_index)]
        if not self.had_been_play:
            window.register_for_task(TERMINABLE_INFINITE,
                                     self.times_blit_task,
                                     time_interval=speed,
                                     task_name=self.IDname)
            window.register_for_animation(self)
        self.had_been_play = True

    def stop(self, window):
        self.alive = False
        window.task_system.destroy_terminable_infinite_task(self.IDname)

    def pause(self, window):
        window.task_system.destroy_terminable_infinite_task(self.IDname)

    def unpause(self, window, pos, speed):
        self.had_been_play = False
        self.play(window, pos, speed)

    def blit_flip(self, window):
        if self.alive:
            window.get_window().blit(self.now_img, self.pos)
        else:
            window.destroy_animation(animation=self)
