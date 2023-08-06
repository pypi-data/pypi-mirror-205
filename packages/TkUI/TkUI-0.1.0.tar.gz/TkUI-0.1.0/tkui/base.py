from tkui.tkui import TkUI
from tkui.utils import load_image


class View:
    def __init__(self, cvs=None, width=0, height=0, bg="#fff", border_color="#000", border_width=0, x_expand=False,
                 y_expand=False, **kwargs):
        self.cvs: TkUI = cvs
        self.x, self.y = 0, 0
        self.width = width
        self.height = height
        self.bg = bg
        self.border_color = border_color
        self.border_width = border_width
        self.x_expand = x_expand
        self.y_expand = y_expand

    def zoom(self, w_rate, h_rate):
        if self.x_expand:
            self.width *= w_rate
        if self.y_expand:
            self.height *= h_rate

        self.draw()

    def draw(self):
        self.cvs.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.bg,
                                  width=self.border_width, outline=self.border_color)

    def place(self, x, y):
        self.x, self.y = x, y
        return self


class Image(View):
    def __init__(self, path, width, height, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.width = width
        self.height = height

    def draw(self):
        self.cvs.create_image(self.x, self.y, image=load_image(self.path, self.width, self.height), anchor="nw")
