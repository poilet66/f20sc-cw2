from tkinter import ttk
import tkinter as tk
from typing import Callable


class Button(ttk.Button):
    def __init__(self, master: tk.Misc, text: str, command: Callable[[], None]):
        super().__init__(master, text=text, command=command)

    def set_enable(self, s: bool):
        """ if the button can be clicked """
        if s:
            self.config(state=tk.NORMAL)
        else:
            self.config(state=tk.DISABLED)

    def set_active(self, s: bool):
        """ active is the current mode """
        if s:
            self.config(style=tk.ACTIVE)
        else:
            self.config(style=tk.ACTIVE)

