from tkfly import *
from tkinter import *
from tkinter import ttk


if __name__ == '__main__':
    root = Tk()
    root.title("tkfly demos")

    try:
        from sv_ttk import toggle_theme
    except:
        pass
    else:
        toggle_theme()

    tooltip_panel = ttk.Labelframe(root, labelanchor=N, labelwidget=Label(text="tkFlyToolTip"))

    label = ttk.Label(tooltip_panel, text="Hover me", anchor=CENTER)
    label.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    tooltip = FlyToolTip(root)
    tooltip.tooltip(label, "I`m a tooltip widget")

    tooltip_panel.pack(fill="x", padx=10, pady=10, ipadx=10, ipady=10)

    root.mainloop()