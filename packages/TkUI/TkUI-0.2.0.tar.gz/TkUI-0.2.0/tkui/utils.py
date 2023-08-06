from hashlib import md5
from typing import Dict

from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

image_obj_dic: Dict[str, PhotoImage] = {}


def load_image(path, width, height):
    img = Image.open(path).resize((width, height))
    photo = ImageTk.PhotoImage(img)
    key = path + str(width) + str(height)
    key = md5(key.encode("utf-8")).hexdigest()
    if key in image_obj_dic.keys():
        return image_obj_dic[key]
    image_obj_dic.update({key: photo})
    return photo


def scrollbar_show(bar, widget):
    bar.lift(widget)


def scrollbar_hide(bar, widget):
    bar.lower(widget)


def scrollbar_autohide(bar, widget):
    scrollbar_hide(bar, widget)
    widget.bind("<Enter>", lambda e: scrollbar_show(bar, widget))
    bar.bind("<Enter>", lambda e: scrollbar_show(bar, widget))
    widget.bind("<Leave>", lambda e: scrollbar_hide(bar, widget))
    bar.bind("<Leave>", lambda e: scrollbar_hide(bar, widget))


def set_dpi():
    try:
        from ctypes import windll
        windll.user32.SetProcessDPIAware()
    except:
        pass
