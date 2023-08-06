import os
import zipfile
import pygame

"""
这个文件是干什么的？
你好，我是SqrtSGUI的作者cemeye！我很鼓励你阅读源代码来提升自己的水平的行为！
呃......你说你是来找BUG的？那也没有关系！让我介绍一下这个文件是干什么的的吧！

首先定义了一个主题类，这个类的参数会有另一个函数自动创建，所以不用担心~它里面有一个get_theme方法，使用来获取主题的

walk_one函数是用来遍历单层目录的，你可以不用管它

unzip_file，用来解压zip文件。什么？你不知道zip在这个GUI库里有什么用？他其实是用来压缩主题文件的~

load_theme方法，用来加载主题文件，这个是这个文件的核心函数，调用就调用它。他会返回一个主题类，当然你直接输出他的返回值，你会看到一个字典，但他的返回值
可不是字典哦！这是类Theme的魔术方法“__str__(self),所以返回值是一个类！”

就这么多，祝你玩得开心！
"""


class Theme:
    """
    主题类
    """

    def __init__(self, theme_path):
        pygame.font.init()
        """
        初始化主题
        :param theme_path:主题文件路径
        """
        self.theme_path = theme_path

        self.img_dict = {}

        self.fonts = {}

        self.load()

        self.abs_path = ""

    def __str__(self):
        """
        魔术方法，print输出时会输出当前图片字典
        :return: self.img_dict
        """
        return str(self.img_dict)

    def load(self):
        """
        导入主题文件，原理是扫描目标文件夹后缀为一般图片文件的图片并转换为Surface对象
        :return: None
        """
        sport_imgs = [
            "png", "jpg", "jpeg", "PNG", "JPG", "JPEG"]

        for filename in walk_one(self.theme_path):
            # 检测当前文件是否是主题文件
            if filename.split(".")[-1] in sport_imgs:
                image_name = filename.split(".")[0]
                self.img_dict[image_name] = pygame.image.load(self.theme_path + "\\" + filename)
            else:
                if filename == "fonts":
                    for ii in walk_one(self.theme_path + "\\fonts\\"):
                        if ii.split(".")[-1] in ["ttf", "otf"]:
                            self.fonts[ii.split(".")[0]] = self.theme_path + "fonts\\" + ii

    def get_theme(self):
        """
        获取主题文件，请在load方法后使用！
        :return: self.img_dict / None
        """
        if self.img_dict:
            return self.img_dict
        else:
            print("<#>错误！获取主题失败！")
            return None

    def get_fonts(self):
        """
        获取字体文件
        :return: FONT
        """
        return self.fonts


def walk_one(path):  # 便利单层文件夹
    file_names = []
    for filename in os.listdir(path):
        file_names.append(filename)
    return file_names


def unzip_file(zip_src, dst_dir) -> bool:
    """
    解压zip文件
    :param zip_src: 是zip文件的路径
    :param dst_dir: 是要解压到的目的文件夹
    :return: None
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        return True
    else:
        return False


def load_theme(theme_path):
    """
    导入主题文件
    注意，文件路径请用\\划分，不要用/划分
    :param theme_path: 主题文件
    :return: Theme类
    """
    theme_name = theme_path.split("\\")[-1].split(".")[0]
    theme_length = len(theme_name)
    if not os.path.exists(theme_path.split(".")[0]):
        unzip_file(theme_path, "\\".join(theme_path.split("\\")[0:-1]))

    theme_path_new = theme_path.split("\\")[:-1]
    last_path = ""
    for i in theme_path_new:
        last_path = last_path + i + "\\"
    theme = Theme(last_path + theme_name)
    return theme

