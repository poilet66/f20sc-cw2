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
        self.rnd_btn = RandomButton(self, plot_callback=self.controller.plot_random)

        #self.rnd_btn = tk.Button(self.window, text="randoms", command=lambda: self.plot([random.randint(0, 100) for _ in range(101)]))
        self.sqr_btn = tk.Button(self, text="squares", command=self.controller.plot_squares)
        self.file_btn = Button_SelectFile(self, change_file_callback=self.controller.on_file_change)

        self.rnd_btn.pack()
        self.sqr_btn.pack()
        self.file_btn.pack()
