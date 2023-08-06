from SqrtS.Widgets.Widget import Widget


class Canvas(Widget):
    def __init__(self):
        super().__init__((0, 0), "canvas")
        self.drawings = []
        self.pos = []

    def bind_pos(self, new_pos: list):
        self.pos = new_pos

    def blit(self, window):
        screen = window.get_window()
        for i in self.drawings:
            i.blit(screen)

    def register_for_event(self, window):
        ...

    def append_drawing(self, drawing):
        self.drawings.append(drawing)

    def appends_drawings(self, drawings):
        for i in drawings:
            self.append_drawing(i)

    def clear(self):
        self.drawings = []
