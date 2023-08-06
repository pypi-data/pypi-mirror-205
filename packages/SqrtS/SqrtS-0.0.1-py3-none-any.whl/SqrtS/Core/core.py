import os
import pyautogui
import pygame
from SqrtS.Expand.WindowTransparency import window_transparency
from SqrtS.Errors.core_error import WidgetNotFound
from SqrtS.Expand.WindowBorder import WindowBorder
from SqrtS.Expand.DraggingBoard import GlobalDraggingBoard
from SqrtS.Core.event_process import EventProcessor
from SqrtS.Core.paging import Pager
from SqrtS.Core.AnimationSystem import AnimationSystem
from SqrtS.tools.image import ImageSurface
from SqrtS.Expand.WindowMove import WindowMover
from SqrtS.Core.TaskSystem import TaskSystem, ONCE, INFINITE, TIMES, TERMINABLE_INFINITE
import win32api

LEFT = 1
MID = 2
RIGHT = 3
WHEEL_DOWN = 5
WHEEL_UP = 4


def get_screen_pixel():
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    return [screen_width, screen_height]


def os_close():
    os._exit(0)


class Window:
    def __init__(self,
                 window_size: tuple,
                 fps=100,
                 noframe=False,
                 _no_screen=False
                 ):
        """
        窗口类的构造函数
        :param window_size:窗口大小，传入元组（int，int）
        :param fps:帧率
        :param noframe:是否有边框？
        :param _no_screen:不用管！如果为True，证明是用于提示框的窗口，不具备自己的屏幕
        """
        os.environ["SDL_IME_SHOW_UI"] = "1"  # 显示输入候选框UI
        # 窗口大小
        self.window_size = window_size
        self._no_screen = _no_screen
        self.noframe = noframe
        # 设置窗口大小
        if not _no_screen:
            if not noframe:
                self.screen = pygame.display.set_mode(self.window_size)
            else:
                self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME)
        # 设置窗存在状态
        self.alive = True

        # 窗口布局文件
        self.Layout = None

        # FPS
        self.fps = fps

        # 定义FPS调控时钟
        self.clock = pygame.time.Clock()

        # 定义事件管理器
        self.event_processor = EventProcessor()

        # 定义任务系统
        self.task_system = TaskSystem()

        # 定义分页器
        self.pager = Pager()

        # background_image
        self.background_image = None

        self.background_color = (25, 25, 25)

        self.title = "SqrtS GUI window"
        pygame.display.set_caption(self.title)

        # 动画刷新系统
        self.animation_system = AnimationSystem()

        # 是否正在暂停？
        self.is_pausing = False

    def __str__(self):
        """
        魔术方法，返回对象的基本信息属性
        :return:
        """
        return f"[对象基本信息]：<SqrtS.Core.Window>=[alive:{self.alive},window_size{self.window_size}]"

    def bind_background_color(self, new_color):
        """
        绑定背景颜色（其实内部也会调用，设置窗口透明就是用这种方法）
        :param new_color: (int,int,int)
        :return: None
        """
        self.background_color = new_color

    def get_widget_by_IDname(self, IDname):
        """
        通控件的IDname获取控件
        :param IDname: str
        :return: None
        """
        for i in self.Layout.widgets:
            if i.IDname == IDname:
                return i
        raise WidgetNotFound(f"没有IDname为{IDname}的控件！")

    def set_window_name(self, name):
        """
        设置窗口名称
        :param name: str
        :return: None
        """
        self.title = name
        pygame.display.set_caption(name)

    @staticmethod
    def set_window_icon(icon_path):
        """
        设置窗口图标
        :param icon_path:图片路径
        :return: None
        """
        icon_surface = pygame.image.load(icon_path)
        pygame.display.set_icon(icon_surface)

    def bind_background_image(self, background_surface: ImageSurface, resize=False | True):
        """
        设置背景图片
        :param background_surface: 背景图片！ImageSurface类型！
        :param resize: 要么False，表示不用重新调整大小；要么True,表示背景图片全部显示，会被重设大小
        :return: None
        """
        if not resize:
            self.background_image = background_surface.return_surface()
        else:
            self.background_image = background_surface.resize(self.get_window_size())

    def get_window_size(self):
        """
        获得窗口大小（并没有什么用的方法，可能是用来凑数的）
        :return: 窗口大小元组
        """
        return self.window_size

    def get_window(self):
        """
        获得窗口
        :return: pygame.Screen
        """
        return self.screen

    def bind_layout(self, layout):
        """
        绑定当前窗口的布局类，可以重复绑定更新
        :param layout: 布局类
        :return: None
        """
        self.Layout = layout

    def register_for_animation(self, animation):
        """

        :param animation: 动画对象
        :return: None
        """
        self.animation_system.register_for_animation(animation)

    def register_for_dynamic_effect(self, animation):
        """

        :param animation: 动画对象
        :return: None
        """
        self.animation_system.register_for_dynamic_effects(animation)

    def destroy_animation(self, animation):
        """

        :param animation: 动画对象
        :return: None
        """
        self.animation_system.destroy_animation(animation)

    def destroy_dynamic_effect(self, animation):
        """

        :param animation: 动画对象
        :return: None
        """
        self.animation_system.destroy_dynamic_effects(animation)

    def register_for_task(self, type_, func, time_interval, times=None, args=None, task_name=None):
        """
        注册任务
        :param task_name: 在注册可停止的无限任务时需要你用到
        :param args: 参数，在注册多次任务时需要用到
        :param type_: 类型，可选地有INFINITE(永久任务，虽然我不知道为什么取无限这个明细),ONCE(只运行一次的),TIMES(多次的，自己指定次数)
        :param func: 目标任务函数
        :param time_interval: 时间间隔
        :param times: 次数，仅当你选择TIMES为type_时的必填参数
        :return:None
        """
        if type_ == INFINITE:
            self.task_system.register_for_infinite_task(task_func=func, time_interval=time_interval)
        elif type_ == TIMES:
            self.task_system.register_for_times_task(task_func=func, times=times, time_interval=time_interval,
                                                     args=args)
        elif type_ == ONCE:
            self.task_system.register_fot_once_task(task_func=func, time_interval=time_interval, args=args)
        elif type_ == TERMINABLE_INFINITE:
            self.task_system.register_for_terminable_infinite_task(task_func=func, time_interval=time_interval,
                                                                   task_name=task_name)

    def destroy_terminable_task(self, task_name):
        self.task_system.destroy_terminable_infinite_task(task_name)

    def append_page(self, layout):
        """
        向窗口的分页器添加一个页面
        :param layout: 布局类
        :return: NOne
        """
        self.pager.append_page(layout, self)

    def change_page(self, layout_name, reload_function):
        """
        改变一个页面
        :param reload_function: 注册函数，需要在新的事件管理中注册事件
        :param layout_name:str
        :return: None
        """
        self.pager.change_page(self, layout_name, reload_function)

    def _reload_layout(self, new_layout, reload_function):
        """
        更换页面，实现切换页面的功能~
        :param reload_function: 注册函数，需要在新的事件管理中注册事件
        :param new_layout: 新的布局文件
        :return: 你猜一猜有没有？
        """
        self.event_processor = EventProcessor()
        self.Layout = new_layout
        reload_function()

    def close(self):
        """
        关闭窗口
        :return:
        """
        self.alive = False
        os_close()
        exit()

    def run(self):
        """
        主运行函数，所有的操作和刷新最终都汇聚到这个方法
        :return: 你猜有没有？
        """
        pygame.init()
        while self.alive:

            # 控制FPS
            self.screen.fill(self.background_color)
            self.animation_system.update_blit_animations(self)
            if self.background_image:
                # 如果有背景图片，则绘制
                self.screen.blit(self.background_image, (0, 0))
            self.clock.tick(self.fps)
            # 布局的全局绘图功能调用
            if self.Layout:
                self.Layout.blit_all(self)
            try:
                # 循环检测事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os_close()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        self.event_processor.key_down_process(event, self)
                    elif event.type == pygame.KEYUP:
                        self.event_processor.key_up_process(event, self)
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_down(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_down(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_down(event, self)
                        elif event.button == WHEEL_DOWN:
                            self.event_processor.mouse_wheel_down(event, self)
                        elif event.button == WHEEL_UP:
                            self.event_processor.mouse_wheel_up(event, self)

                        self.event_processor.mouse_down(event, self)

                    elif event.type == pygame.MOUSEBUTTONUP:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_up(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_up(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_up(event, self)

                        self.event_processor.mouse_up(event, self)

                    elif event.type == pygame.DROPFILE:
                        self.event_processor.drop_file_event(event, self)
                    elif event.type == pygame.TEXTINPUT:
                        self.event_processor.text_input_event(event, self)
                self.event_processor.everytime_event(self)
                self.task_system.task_system_update()
            except pygame.error as e:
                continue
            except ValueError as e:
                continue
            # 画图更新
            pygame.display.flip()

    @staticmethod
    def iconify():
        pygame.display.iconify()


class InferiorWindow(Window):
    def __init__(self, window):
        super().__init__(window_size=window.get_window_size(), fps=50, _no_screen=True)
        self.screen = window.screen

        # {"name":[surface,pos]}
        self.draw_things = {}

    def bind_background_image(self, background_surface: ImageSurface, resize=False | True):
        """
        设置背景图片(重写为空函数)
        """
        ...

    def append_draw_thing(self, new_thing):
        """
        添加需要被画出的新东西
        :param new_thing: [name, surface, pos]
        :return: None
        """
        self.draw_things[new_thing[0]] = new_thing[1:]

    def run(self):
        """
        主运行函数，所有的操作和刷新最终都汇聚到这个方法
        :return: 你猜有没有？
        """
        while self.alive:
            # 控制FPS
            if self.draw_things:
                for i in self.draw_things.keys():
                    self.screen.blit(self.draw_things[i][0], self.draw_things[i][1])
            self.animation_system.update_blit_animations(self)

            self.clock.tick(self.fps)
            # 布局的全局绘图功能调用
            self.Layout.blit_all(self)

            # 循环检测事件
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os_close()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        self.event_processor.key_down_process(event, self)
                    elif event.type == pygame.KEYUP:
                        self.event_processor.key_up_process(event, self)
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_down(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_down(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_down(event, self)
                        elif event.button == WHEEL_DOWN:
                            self.event_processor.mouse_wheel_down(event, self)
                        elif event.button == WHEEL_UP:
                            self.event_processor.mouse_wheel_up(event, self)

                        self.event_processor.mouse_down(event, self)

                    elif event.type == pygame.MOUSEBUTTONUP:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_up(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_up(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_up(event, self)

                        self.event_processor.mouse_up(event, self)

                    elif event.type == pygame.DROPFILE:
                        self.event_processor.drop_file_event(event, self)
                    elif event.type == pygame.TEXTINPUT:
                        self.event_processor.text_input_event(event, self)
                self.event_processor.everytime_event(self)
                self.task_system.task_system_update()
            except pygame.error:
                continue
            except ValueError:
                continue
            # 画图更新
            pygame.display.flip()


class CustomizedFrameWindow(Window):
    """
    自定义窗口边框的窗口
    """

    def __init__(self, window_size: tuple,
                 window_frame_size: int,
                 theme,
                 font,
                 enable_customized_border=False,
                 customised_border=None):
        super().__init__(window_size, noframe=True)
        self.real_window_size = [window_size[0], window_size[1] + window_frame_size]
        self.window_size = window_size
        self.screen = pygame.display.set_mode([window_size[0], window_size[1] + window_frame_size], pygame.NOFRAME)
        self.offset_address = window_frame_size

        if not enable_customized_border:
            self.window_border = WindowBorder(theme, border_size=[window_size[0], window_frame_size], window=self,
                                              font=font)
        else:
            if customised_border:
                self.window_border = customised_border

        self.dragging_board = GlobalDraggingBoard([self.window_size[0], self.offset_address], "_slide_board")
        self.dragging_board.register_for_event(self)
        self.dragging_board.bind_pos([0, 0])
        self.dragging_board.bind_call_slide(self._drag)

        self.window_mover = WindowMover()

    def _drag(self):
        """
        拖拽函数，内部函数
        :return: None
        """
        abs_mouse_pos = pyautogui.position()
        pygame_pos = self.dragging_board.last_mouse_pos
        self.window_mover.moveto([abs_mouse_pos[0] - pygame_pos[0], abs_mouse_pos[1] - pygame_pos[1]])

    def get_real_window_size(self):
        """
        获得窗口大小（并没有什么用的方法，可能是用来凑数的）
        :return: 窗口大小元组
        """
        return self.real_window_size

    def get_frame_offset(self):
        """
        获取边框的高度
        :return: 高度int
        """
        return self.offset_address

    def bind_layout(self, layout):
        """
        绑定当前窗口的布局类，可以重复绑定更新
        :param layout: 布局类
        :return: None
        """

        for i in layout.widgets:
            i.bind_pos([i.pos[0], i.pos[1] + self.offset_address])

        self.Layout = layout

    def append_page(self, layout):
        """
        向窗口的分页器添加一个页面
        :param layout: 布局类
        :return: NOne
        """
        self.pager.append_page(layout, self)

    def run(self):
        self.window_mover.update(self)
        self.dragging_board.update_info(self)
        """
        主运行函数，所有的操作和刷新最终都汇聚到这个方法
        :return: 你猜有没有？
        """
        while self.alive:
            # 控制FPS
            self.screen.fill(self.background_color)
            self.window_border.blit_border(self)
            if self.background_image:
                self.screen.blit(self.background_image, (0, self.offset_address))
            self.clock.tick(self.fps)
            # 布局的全局绘图功能调用
            self.Layout.blit_all(self)
            # 循环检测事件
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os_close()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        self.event_processor.key_down_process(event, self)
                    elif event.type == pygame.KEYUP:
                        self.event_processor.key_up_process(event, self)
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_down(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_down(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_down(event, self)
                        elif event.button == WHEEL_DOWN:
                            self.event_processor.mouse_wheel_down(event, self)
                        elif event.button == WHEEL_UP:
                            self.event_processor.mouse_wheel_up(event, self)

                        self.event_processor.mouse_down(event, self)

                    elif event.type == pygame.MOUSEBUTTONUP:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_up(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_up(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_up(event, self)

                        self.event_processor.mouse_up(event, self)

                    elif event.type == pygame.DROPFILE:
                        self.event_processor.drop_file_event(event, self)
                    elif event.type == pygame.TEXTINPUT:
                        self.event_processor.text_input_event(event, self)
                self.event_processor.everytime_event(self)
                self.task_system.task_system_update()
            except pygame.error:
                continue
            except ValueError:
                continue
            # 画图更新
            pygame.display.flip()
        if self.is_pausing:
            self.pausing_run()
            if self.alive:
                self.run()


class FullScreenWindow(Window):
    def __init__(self, if_transparency=False):
        super().__init__((500, 500))
        self.window_size = get_screen_pixel()
        self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME | pygame.FULLSCREEN)
        self.if_transparency = if_transparency

    def run(self):
        """
        主运行函数，所有的操作和刷新最终都汇聚到这个方法
        :return: 你猜有没有？
        """
        if self.if_transparency:
            window_transparency(self)
        while self.alive:
            # 控制FPS
            self.screen.fill(self.background_color)
            if self.background_image:
                # 如果有背景图片，则绘制
                self.screen.blit(self.background_image, (0, 0))
            self.clock.tick(self.fps)
            self.animation_system.update_blit_animations(self)
            # 布局的全局绘图功能调用
            self.Layout.blit_all(self)
            # 循环检测事件
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os_close()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        self.event_processor.key_down_process(event, self)
                    elif event.type == pygame.KEYUP:
                        self.event_processor.key_up_process(event, self)
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_down(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_down(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_down(event, self)
                        elif event.button == WHEEL_DOWN:
                            self.event_processor.mouse_wheel_down(event, self)
                        elif event.button == WHEEL_UP:
                            self.event_processor.mouse_wheel_up(event, self)

                        self.event_processor.mouse_down(event, self)

                    elif event.type == pygame.MOUSEBUTTONUP:

                        if event.button == LEFT:
                            self.event_processor.mouse_left_up(event, self)
                        elif event.button == RIGHT:
                            self.event_processor.mouse_right_up(event, self)
                        elif event.button == MID:
                            self.event_processor.mouse_mid_up(event, self)

                        self.event_processor.mouse_up(event, self)

                    elif event.type == pygame.DROPFILE:
                        self.event_processor.drop_file_event(event, self)
                    elif event.type == pygame.TEXTINPUT:
                        self.event_processor.text_input_event(event, self)
                self.event_processor.everytime_event(self)
                self.task_system.task_system_update()
            except pygame.error:
                continue
            except ValueError:
                continue
            # 画图更新
            pygame.display.flip()


if __name__ == "__main__":
    print(get_screen_pixel())
