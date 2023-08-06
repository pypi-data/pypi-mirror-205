from SqrtS.Layouts.Layout import Layout
from SqrtS.Widgets.Widget import Widget


class LinearLayout(Layout):
    """
    线性布局，全部一个一个罗列下来的布局
    """

    def __init__(self, window_size, name, weight_spacing=3, direction="lengthwise"):
        super().__init__(name=name)
        self.window_size = window_size
        self.weights = []

        self.weight_spacing = weight_spacing

        self.y_limit = 0

        self.direction = direction

    def append(self, weight: Widget):
        """
        添加新的控件
        :param weight:控件
        :return:None
        """
        self.weights.append(weight)

    def compute_poses(self):
        """
        线性布局的坐标更新计算方式
        :return: None
        """
        # 纵向布局的坐标更新方法
        if self.direction == "lengthwise":
            for index, i in enumerate(self.weights):
                if i.many_weight:
                    i.process_many_weight_poses()
                    # i.size = [i.size[0], (i.size[1] + i.padding) * i.button_numbers]
                size_i = i.size
                half_length = int(size_i[0] / 2)
                window_x_center = int(self.window_size[0] / 2)
                i_pos_x = window_x_center - half_length
                i_pos_y = self.y_limit
                self.y_limit += size_i[1]
                i_pos = [i_pos_x, i_pos_y + int(self.weight_spacing) * index]
                i.bind_pos(i_pos)

        # 横向布局的坐标更新方法
        elif self.direction == "broadwise":
            for index, i in enumerate(self.weights):
                if i.many_weight:
                    i.process_many_weight_poses()
                    # i.size = [i.size[0], (i.size[1] + i.padding) * i.button_numbers]
                size_i = i.size
                half_width = int(size_i[1] / 2)
                window_y_center = int(self.window_size[1] / 2)
                i_pos_x = self.y_limit
                i_pos_y = window_y_center - half_width
                self.y_limit += size_i[0]
                i_pos = [i_pos_x + int(self.weight_spacing) * index, i_pos_y]
                i.bind_pos(i_pos)

    def blit_all(self, window):
        """
        在屏幕上画出所有的控件，通过隔代调用控件的绘图方法
        |这个方法会在Window类中被调用|
        :param window: Window类对象
        :return: None
        """
        for i in self.weights:
            i.blit(window)

    def appends(self, weights: list):
        """
        批量添加控件
        :param weights: 控件列表
        :return:
        """
        for i in weights:
            self.append(i)
        self.compute_poses()


if __name__ == "__main__":
    ...
