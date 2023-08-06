import math
from SqrtS.Core.TaskSystem import TIMES


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        加法
        :param other:
        :return:
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        减法
        :param other:
        :return:
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        """
        输出
        :return:
        """
        return f"Vector({self.x},{self.y})"

    def __mul__(self, other):
        """
        乘法
        :param other:
        :return:
        """
        return self.x * other.x + self.y * other.y

    def __iadd__(self, other):
        """
        自增
        :param other:
        :return:
        """
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        """
        自减
        :param other:
        :return:
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __pos__(self):
        """
        当取+号时的操作
        :return:
        """
        return self

    def __neg__(self):
        """
        当取-号的时候
        :return:
        """
        return Vector(-self.x, -self.y)

    def __abs__(self):
        """
        取模长的操作
        :return:
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __int__(self):
        """
        int方法，返回模长的整数
        :return:
        """
        return int(self.__abs__())

    def __getitem__(self, item):
        """
        可选的[0],[1],返回x或者y
        :param item:
        :return:
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y

    def __setitem__(self, key, value):
        """
        设置x或y，[0],[1]
        :param key:
        :param value:
        :return:
        """
        if key == 0:
            self.x = int(value)
        elif key == 1:
            self.y = int(value)

    def __copy__(self):
        """
        获取列表格式的向量
        :return:list
        """
        return [self.x, self.y]


if __name__ == "__main__":
    v1 = Vector(1, 1)
    v2 = Vector(2, 2)
    for i in range(100):
        v2 -= v1
        print(v2)
