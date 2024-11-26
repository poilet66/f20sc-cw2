from tkinter import ttk
import tkinter as tk

class Controls(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.register_controls(self)
