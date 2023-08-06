from tkinter import Canvas, BOTH, Event, ALL


class TkUI(Canvas):
    def __init__(self, master, size, x=0, y=0, bg="#fff", **kwargs):
        super().__init__(master, bg=bg, highlightthickness=0, **kwargs)
        self.widgets = list()
        self.x, self.y = x, y
        self.size = size
        self.pack(fill=BOTH, expand=True)

        self.bind("<Configure>", self.__reset)

    def add(self, widget):
        widget.cvs = self
        self.widgets.append(widget)
        return self

    def __reset(self, evt: Event):
        """
        窗口大小重置,更新子组件
        """
        w_rate = evt.width / self.size[0]
        h_rate = evt.height / self.size[1]
        self.size = (evt.width, evt.height)
        self.delete(ALL)
        for widget in self.widgets:
            widget.zoom(w_rate, h_rate)
