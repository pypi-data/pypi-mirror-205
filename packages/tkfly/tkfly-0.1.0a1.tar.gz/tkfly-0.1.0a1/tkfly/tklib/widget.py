from tkfly._tklib import _load_tklib
from tkfly._tcllib import _load_tcllib
from tkfly.core import fly_load4, fly_root, fly_local, fly_chdir
from tkinter import Widget


def load_menubar():
    _load_tklib()
    _load_tcllib()
    fly_load4("snit", fly_local()+"\\_tcllib\\snit")
    fly_load4("widget", fly_local()+"\\_tklib\\widget")


if __name__ == '__main__':
    from tkinter import Tk, Entry

    root = Tk()

    load_menubar()

    root.mainloop()