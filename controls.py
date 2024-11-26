from tkinter import ttk
import tkinter as tk
from buttons.random_button import RandomButton
from buttons.file_select import Button_SelectFile

class Controls(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.register_controls(self)

        # button stuff
        self.rnd_btn = RandomButton(parent, plot_callback=self.plot)
        #self.rnd_btn = tk.Button(self.window, text="randoms", command=lambda: self.plot([random.randint(0, 100) for _ in range(101)]))
        self.sqr_btn = tk.Button(self.window, text="squares", command=lambda: self.plot([i**2 for i in range(101)]))
        self.file_btn = Button_SelectFile(self.window, change_file_callback=self.change_file)
        self.rnd_btn.pack()
        self.sqr_btn.pack()
        self.file_btn.pack()
