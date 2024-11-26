import random
from typing import Callable
from .base_button import ButtonBase
import tkinter as tk


class RandomButton(ButtonBase):
    def __init__(self, master: tk.Tk, plot_callback: Callable) -> None:
        self.plot_callback = plot_callback
        super().__init__(master=master, label="Random Button!")

    def handle_click(self) -> None:
        values = [random.randint(0, 100) for _ in range(101)]
        self.plot_callback(values)