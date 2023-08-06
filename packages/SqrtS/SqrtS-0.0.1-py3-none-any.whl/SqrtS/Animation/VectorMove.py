from SqrtS.Animation.Vector import Vector
from SqrtS.Animation.DynamicEffects import DynamicEffects
from SqrtS.Errors.animation_err import DidNotBindWidgetError


class VectorMove(DynamicEffects):
    def __init__(self, vector, time_interval, x_speed=1, y_speed=1):
        super().__init__()
        self.x_speed = x_speed
        self.y_speed = y_speed

        self.vector = vector

        if self.vector[0] != 0:
            self.forward_x = int(self.vector[0] / abs(self.vector[0]))
        else:
            self.forward_x = 0

        if self.vector[1] != 0:
            self.forward_y = int(self.vector[1] / abs(self.vector[1]))
        else:
            self.forward_y = 0

        self.times = max(abs(self.vector[0]), abs(self.vector[1]))
        self.time_interval = time_interval
        self.target_widget = None
        self.if_started = False

    def bind_widget(self, widget):
        self.target_widget = widget

    def _update_dynamic_effects(self):
        pos = self.target_widget.pos
        x = pos[0]
        y = pos[1]
        if self.vector[0] != 0:
            self.vector[0] -= self.forward_x
            x += self.forward_x * self.x_speed
        if self.vector[1] != 0:
            self.vector[1] -= self.forward_y
            y += self.forward_y * self.y_speed

        self.target_widget.bind_pos([x, y])

    def update(self, window):
        if not self.if_started:
            self.if_started = True
            self.times_call(self.time_interval, self.times, self._update_dynamic_effects)
        else:
            if self.if_finished:
                window.destroy_dynamic_effect(self)


class VectorMoveGroup:
    def __init__(self):
        self.group = []
        self.index = 0

    def bind_all_widget(self, widget):
        for i in self.group:
            i.bind_widget(widget)

    def bind_vectors(self, vectors):
        """

        :param vectors:[VectorMove, VectorMove......]
        :return:
        """
        self.group = vectors

    def update(self, window):
        for index, i in enumerate(self.group):
            if not i.if_finished and self.index == index:
                self.index = i
                i.update(window)
            elif not i.if_finished:
                self.index = i
                i.update(window)
