import os
import pystray
import threading
from SqrtS.Errors.core_error import StrayHasBeenRunningError
from PIL import Image
from pystray import MenuItem


class SqrtStray:
    def __init__(self, icon_path):
        """
        系统托盘类
        :param icon_path:托盘图标路径
        """
        self.menu = []
        self.icon_image = Image.open(icon_path)
        self.icon = None

        self.name = "SqrtSGUI"
        self.show_text = "SqrtSGUI"
        self.running = False
        self.bind_move_on("SqrtGUI", "SqrtGUI-running")

    def append_menu(self, menu_name, call_func, enabled=True, visible=True, default=True):
        """
        添加单个项
        :param default: 是否是菜单按钮型的项
        :param visible: 是否可见
        :param enabled: 是否可用
        :param menu_name: 项名
        :param call_func: 回调函数
        :return: None
        """
        if not self.running:
            self.menu.append(
                MenuItem(text=menu_name, action=call_func, enabled=enabled, default=default, visible=visible))
        else:
            raise StrayHasBeenRunningError("系统托盘已经正在运行！无法动态添加菜单！")

    def bind_move_on(self, name, show_text):
        """
        绑定移动到上面的函数
        :param name: 图标名
        :param show_text: 展示的文字
        :return: None
        """
        self.icon = pystray.Icon(name, self.icon_image, show_text, self.menu)
        self.name = name
        self.show_text = show_text

    def notify(self, title, text):
        """
        显示一条消息
        :param title:标题
        :param text: 文字
        :return: None
        """
        if self.icon:
            self.icon.notify(title, text)

    def _run(self):
        """
        内部函数，调用icon的run
        :return:
        """
        self.icon.run()

    @staticmethod
    def close():
        """
        关闭函数
        :return:
        """
        os._exit(0)

    def run(self):
        """
        运行
        :return: None
        """
        self.running = True
        thread = threading.Thread(target=self._run)
        thread.start()


if __name__ == "__main__":
    st = SqrtStray("../tools/theme_root/theme/icon.png")
    st.append_menu("菜单一", lambda: st.notify("hello", "this is GUi"))
    st.bind_move_on("SqrtSGUI", "das")
    st.run()
    while True:
        print("hello")
