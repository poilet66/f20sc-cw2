from tkinter import Variable, ttk
import tkinter as tk
from typing import Any, Literal

class RadioButton(ttk.Radiobutton):
    def __init__(self, parent: tk.Misc, text: str, variable: Variable | Literal[''], value: Any):
        super().__init__(parent, text=text, variable=variable, value=value)

    def set_enable(self, s: bool):
        """ if the button can be clicked """
        if s:
            self.config(state=tk.NORMAL)
        else:
            self.config(state=tk.DISABLED)


