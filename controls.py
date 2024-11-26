from tkinter import ttk
import tkinter as tk
from buttons.random_button import RandomButton
from buttons.file_select import Button_SelectFile
from controller import Controller

class Controls(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller: Controller):
        super().__init__(parent)

        self.controller = controller
        self.controller.register_controls(self)

        # button stuff
        self.rnd_btn = RandomButton(self, plot_callback=self.controller.plot_random)

        #self.rnd_btn = tk.Button(self.window, text="randoms", command=lambda: self.plot([random.randint(0, 100) for _ in range(101)]))
        self.sqr_btn = tk.Button(self, text="squares", command=self.controller.plot_squares)
        self.file_btn = Button_SelectFile(self, change_file_callback=self.controller.on_file_change)

        self.input = tk.Text(self, height=1, width=20)

        self.rnd_btn.pack(side=tk.LEFT)
        self.sqr_btn.pack(side=tk.LEFT)
        self.file_btn.pack(side=tk.LEFT)
        self.input.pack(side=tk.LEFT)
