class Pager:
    """
    分页器类
    """

    def __init__(self):
        # 布局字典
        self.layouts = {}

    def append_page(self, layout, window):
        """
        添加一个页面...
        :param layout: 布局
        :return: None
        """
        if not window.Layout:
            window.bind_layout(layout)
        self.layouts[layout.name] = layout

    def change_page(self, window, layout_name, reload_function):
        """
        重新更换页面
        :param window:
        :param layout_name:
        :param reload_function:
        :return:
        """
        window._reload_layout(self.layouts[layout_name], reload_function=reload_function)
