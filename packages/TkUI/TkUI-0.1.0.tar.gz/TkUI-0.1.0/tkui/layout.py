from abc import ABCMeta
from typing import List

from tkui.base import View


class Cell:
    def __init__(self, span, widget, x_align, y_align):
        self.span = span
        self.widget: View = widget
        self.x_align = x_align
        self.y_align = y_align


class Grid(View, metaclass=ABCMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children: List[Cell] = []

    def cell(self, span, widget, x_align="center", y_align="center"):
        """
        向单元格放入组件,并指定每个格子的分片大小
        :param span: 每个格子占用的比例 所有span综合为24
        :param widget: 组件
        :param x_align: 水平排列
        :param y_align: 垂直排列
        :return:
        """
        self.__check_span_total()
        widget.cvs = self.cvs
        self.children.append(Cell(span, widget, x_align, y_align))

    def __check_span_total(self):
        total = 0
        for item in self.children:
            total += item.span
            if total > 24:
                raise Exception("span总和不能超过24")


def widget_align(w1, h1, w2, h2, x_align, y_align):
    """
    计算组件内小组件各种对齐方式,返回小组间左上角相对坐标
    :param w1:外层组件宽度
    :param h1:外层组件高度
    :param w2:内层组件宽度
    :param h2:内层组件高度
    :param x_align:水平对齐方式
    :param y_align:垂直对齐方式
    """
    x, y = 0, 0
    if x_align == "center":
        x = (w1 - w2) / 2
    if x_align == "left":
        x = 0
    if x_align == "right":
        x = w1 - w2

    if y_align == "center":
        y = (h1 - h2) / 2
    if y_align == "top":
        y = 0
    if y_align == "bottom":
        y = h1 - h2
    return x, y


class VGrid(Grid):
    """
    vertical grid
    垂直的网格系统
    """

    def draw(self):
        super(VGrid, self).draw()
        cell_h = self.height / 24
        cell_w = self.width
        x = self.x
        y = self.y
        for item in self.children:
            widget = item.widget
            if widget.height <= 0:
                widget.height = cell_h * item.span
            if widget.width <= 0:
                widget.width = cell_w
            _x, _y = widget_align(cell_w, cell_h * item.span, widget.width, widget.height, item.x_align, item.y_align)
            widget.place(x + _x, y + _y)
            widget.draw()
            y += cell_h * item.span
