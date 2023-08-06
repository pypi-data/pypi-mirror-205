class AnimationSystem:
    def __init__(self):
        self.animations = []
        self.dynamic_effects = []

    def update_blit_animations(self, window):
        """
        更新动画效果
        :param window:Window
        :return: None
        """
        for i in self.animations:
            i.blit_flip(window)
        self.update_dynamic_effects(window)

    def update_dynamic_effects(self, window):
        for i in self.dynamic_effects:
            i.update(window)

    def register_for_animation(self, animation):
        """
        注册动画，注册开始之日便是运行之时
        :param animation: 动画对象
        :return: None
        """
        self.animations.append(animation)

    def register_for_dynamic_effects(self, animation):
        """
        注册动态效果
        :param animation:效果
        :return:None
        """
        self.dynamic_effects.append(animation)

    def destroy_animation(self, animation):
        """

        :param animation: 动画对象
        :return: None
        """
        for i in self.animations:
            if i == animation:
                self.animations.remove(i)

    def destroy_dynamic_effects(self, animation):
        """

        :param animation: 动效对象
        :return: None
        """
        for i in self.dynamic_effects:
            if i == animation:
                self.dynamic_effects.remove(i)
