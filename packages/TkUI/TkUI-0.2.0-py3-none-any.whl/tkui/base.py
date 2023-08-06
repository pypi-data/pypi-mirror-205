import tkinter

from tkui.tkui import TkUI
from tkui.utils import load_image

DEFAULT_FONT = ("微软雅黑", 16)


class View:
    def __init__(self, cvs=None, width=0, height=0, bg=None, border_color="#000", border_width=0, x_expand=False,
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

    def zoom(self, size_old, size_new):
        if self.x_expand:
            self.width += size_new[0] - size_old[0]
        if self.y_expand:
            self.height += size_new[1] - size_old[1]
        self.draw()

    def draw(self):
        self.cvs.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.bg,
                                  width=self.border_width, outline=self.border_color)

    def place(self, x, y):
        self.x, self.y = x, y
        return self


class Text(View):
    def __init__(self, text, text_color="#000", font=DEFAULT_FONT, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.text_color = text_color
        self.font = font
        # 缺省值 未设置宽高时 根据像素自动计算出宽高
        if self.width <= 0:
            self.width = font[1] * (len(text) + 2)
        if self.height <= 0:
            self.height = font[1] * 3

    def draw(self):
        super(Text, self).draw()
        self.cvs.create_text(self.x + (self.width / 2), self.y + (self.height / 2), text=self.text,
                             fill=self.text_color, font=self.font, anchor="center")


class Button(Text):
    def __init__(self, text, **kwargs):
        super().__init__(text, **kwargs)


class Input(Text):
    def __init__(self, text="", **kwargs):
        super().__init__(text, **kwargs)

    def draw(self):
        super(Input, self).draw()
        val = tkinter.StringVar(value=self.text)
        entry = tkinter.Entry(font=DEFAULT_FONT, textvariable=val, fg=self.text_color, bg=self.bg,
                              borderwidth=0, highlightthickness=0)
        # 处理Entry边框问题
        offset = 0 if self.border_width == 0 else 1
        self.cvs.create_window(self.x + offset, self.y + offset, window=entry, width=self.width - offset,
                               height=self.height - offset, anchor="nw")


class Image(View):
    def __init__(self, path, width, height, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.width = width
        self.height = height

    def draw(self):
        super(Image, self).draw()
        # 处理边框
        offset = 0 if self.border_width == 0 else 1
        self.cvs.create_image(self.x + offset, self.y + offset,
                              image=load_image(self.path, self.width - offset, self.height - offset),
                              anchor="nw")
