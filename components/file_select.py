from typing import Callable
import tkinter as tk
from tkinter.filedialog import askopenfilename

from components.button import Button

class SelectFile(Button):
    def __init__(self, master: tk.Misc, change_file_callback: Callable[[str], None]) -> None:
        self.file_callback = change_file_callback
        super().__init__(master=master, text="Choose a file", command=self.handle_click)

    def handle_click(self) -> None:
        self.path = askopenfilename()
        self.file_callback(self.path)
        

