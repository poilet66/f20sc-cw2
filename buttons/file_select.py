from .base_button import ButtonBase
from typing import Callable
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import Button

class Button_SelectFile(ButtonBase):
    def __init__(self, master: tk.Tk, change_file_callback: Callable[[str], None]) -> None:
        self.file_callback = change_file_callback
        super().__init__(master=master, label="Choose a file")

    def handle_click(self) -> None:
        self.path = askopenfilename()
        self.file_callback(self.path)
        

