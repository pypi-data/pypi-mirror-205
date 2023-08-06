from SqrtS.Core.core import Window, InferiorWindow
from SqrtS.tools.image import ImageSurface, SurfaceImage
from SqrtS.tools.load_theme import Theme
from SqrtS.Widgets.Button import ImageButton, Button
from SqrtS.Widgets.Text import Texts, LineTexts
from SqrtS.Layouts.FloatingLayout import FloatingLayout


OK_CANCEL = 1
OK = 2
TRUE_FALSE = 3


class PopupWindow:
    """
    弹窗基类
    """

    def __init__(self, popup_size,
                 theme: Theme,
                 title,
                 text,
                 text_line_length,
                 font,
                 popup_image_path=False,
                 close_button_size=None,
                 style=OK_CANCEL,
                 title_style=None,
                 texts_style=None):
        """

        :param popup_size: [int,int]
        :param theme: Theme
        :param title: str
        :param text: str
        :param text_line_length:int
        :param font: Font
        :param popup_image_path:str
        :param close_button_size: [int,int]
        :param style: [(),()]
        :param title_style: [(),()]
        :param texts_style: [(),()]
        """
        if texts_style is None:
            texts_style = [[0, 0, 0], None]
        if title_style is None:
            title_style = [[0, 0, 0], None]
        # 定义文字和标题对象
        self.title_sur = Texts(title, title_style[0], font, "title", True, title_style[1])
        self.texts = LineTexts(text, texts_style[0], font, text_line_length, "texts", True, texts_style[1])
        self.title_pos = []
        self.texts_pos = []
        # 定义按钮样式
        self.style = style
        # 按钮大小
        if close_button_size is None:
            close_button_size = [20, 20]
        # 弹窗大小
        self.popup_size = popup_size
        # 窗口状态
        self.alive = False
        # 窗口固定坐标
        self.popup_back_pos = [0, 0]
        # 关闭按钮参数
        self.close_button_size = close_button_size
        self.image_close_list = [
            theme.get_theme()["kill"],
            theme.get_theme()["kill_click"],
            theme.get_theme()["kill_chosen"]
        ]
        self.close_button = ImageButton(self.close_button_size, self.image_close_list, IDname="popup_close_button")
        self.close_button_pos = [0, 0]
        # 定义布局
        self.root_layout = FloatingLayout(name="root_popup")
        # 弹窗背景图片
        if not popup_image_path:
            self.popup_back_image = SurfaceImage(theme.get_theme()["popup"]).resize(self.popup_size)
        else:
            self.popup_back_image = ImageSurface(popup_image_path).resize(popup_size)
        # 弹窗返回值
        self.return_value = ""

    def develop_other_widgets(self, theme, font, window, popup_window):
        """

        :param theme: Theme
        :param font: Font
        :param window: Window
        :param popup_window: PopupWindow
        :return: None
        """
        self._compute_popup_pos(window_size=window.get_window_size())
        self.root_layout.append(self.close_button)
        self.root_layout.bind_widgets_poses({"popup_close_button": self.close_button_pos})
        self.root_layout.append(self.title_sur)
        self.root_layout.append(self.texts)

        if self.style == OK_CANCEL:
            def call_ok(args):
                self.return_value = "ok"
                self.alive = False
                popup_window.alive = False

            def call_cancel(args):
                self.return_value = "cancel"
                self.alive = False
                popup_window.alive = False

            ok_btn = Button(
                [100, 40], "OK", theme, font, "ok_btn"
            )
            self.root_layout.append(ok_btn)
            ok_btn.register_for_event(popup_window)
            ok_btn.bind_call_func(call_ok)
            # --------
            cancel_btn = Button(
                [100, 40], "Cancel", theme, font, "cancel_btn"
            )
            self.root_layout.append(cancel_btn)
            cancel_btn.register_for_event(popup_window)
            cancel_btn.bind_call_func(call_cancel)
            # --------
            self.root_layout.bind_widgets_poses(widgets_pos_dict={
                "ok_btn": [
                    self.popup_back_pos[0] + self.popup_size[0] - 220, self.popup_back_pos[1] + self.popup_size[1] - 50
                ], "cancel_btn": [
                    self.popup_back_pos[0] + self.popup_size[0] - 110, self.popup_back_pos[1] + self.popup_size[1] - 50
                ]
            })
        elif self.style == OK:
            def call_ok(args):
                self.return_value = "ok"
                self.alive = False
                popup_window.alive = False

            ok_btn = Button(
                [100, 40], "OK", theme, font, "ok_btn"
            )
            self.root_layout.append(ok_btn)
            ok_btn.register_for_event(popup_window)
            ok_btn.bind_call_func(call_ok)
            # --------
            self.root_layout.bind_widgets_poses(widgets_pos_dict={
                "ok_btn": [
                    self.popup_back_pos[0] + self.popup_size[0] - 110, self.popup_back_pos[1] + self.popup_size[1] - 50
                ],
            })

        elif self.style == TRUE_FALSE:
            def call_true(args):
                self.return_value = "True"
                self.alive = False
                popup_window.alive = False

            def call_false(args):
                self.return_value = "False"
                self.alive = False
                popup_window.alive = False

            true_btn = Button(
                [100, 40], "是", theme, font, "true_btn"
            )
            self.root_layout.append(true_btn)
            true_btn.register_for_event(popup_window)
            true_btn.bind_call_func(call_true)
            # --------
            false_btn = Button(
                [100, 40], "否", theme, font, "false_btn"
            )
            self.root_layout.append(false_btn)
            false_btn.register_for_event(popup_window)
            false_btn.bind_call_func(call_false)
            # --------
            self.root_layout.bind_widgets_poses(widgets_pos_dict={
                "true_btn": [
                    self.popup_back_pos[0] + self.popup_size[0] - 220, self.popup_back_pos[1] + self.popup_size[1] - 50
                ], "false_btn": [
                    self.popup_back_pos[0] + self.popup_size[0] - 110, self.popup_back_pos[1] + self.popup_size[1] - 50
                ]
            })

    def _compute_popup_pos(self, window_size):
        """
        重新计算背景图片的位置
        :param window_size:
        :return:
        """
        self.popup_back_pos = [
            int((window_size[0] - self.popup_size[0]) / 2),
            int((window_size[1] - self.popup_size[1]) / 2)

        ]
        self.close_button_pos = [
            self.popup_back_pos[0] + self.popup_size[0] - self.close_button_size[0],
            self.popup_back_pos[1],
        ]

        self.title_pos = [self.popup_back_pos[0] + 10, self.popup_back_pos[1] + 10]
        self.texts_pos = [
            self.popup_back_pos[0] + 30, self.popup_back_pos[1] + 50
        ]

        self.title_sur.bind_pos(self.title_pos)
        self.texts.bind_pos(self.texts_pos)
        self.close_button.bind_pos(self.close_button_pos)

    def start(self, window: Window, theme, font):
        """
        运行弹窗（注意！该控件（也许不是控件）是另开了一个循环！元循环中的所有GUI将被暂停！）
        :return: None
        """

        def close(args):
            self.alive = False
            popup_window.alive = False

        self.close_button.bind_call_func(close)

        self.alive = True

        popup_window = InferiorWindow(window)
        self.develop_other_widgets(theme, font, window, popup_window)
        popup_window.append_draw_thing(["popup_back", self.popup_back_image, self.popup_back_pos])
        popup_window.bind_layout(self.root_layout)

        self.close_button.register_for_event(popup_window)

        popup_window.run()
