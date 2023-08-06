import json

"""
这个文件是干什么的？
你好，我是SqrtSGUI的作者cemeye！我很鼓励你阅读源代码来提升自己的水平的行为！
呃......你说你是来找BUG的？那也没有关系！让我介绍一下这个文件是干什么的的吧！

这个文件内容这么点，我就随便说几句吧！
这个JSONReader没什么巨大的野心，他只是加载最外层的GLOBAL.json文件的。你不知道么？那个文件里面存着一些需要持久化保存的全局参数！

就这么多，祝你玩得开心！
"""


class JsonReader:
    def __init__(self, json_path):
        self.json_path = json_path

    def read_json(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            strs = f.read()
            dict_json = json.loads(strs)
        return dict_json


if __name__ == "__main__":
    jc = JsonReader()
    print(jc.read_json())
