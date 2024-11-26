import tkinter as tk
from controller import Controller

import pandas as pd

import pandas as pd

from controls import Controls
from viewer import Viewer

from data_controller import DataController


class Application(tk.Tk):
    def __init__(self, data_controller: DataController):
        super().__init__()
        self.geometry("500x500")
        self.title("Data Visualiser")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0)
        self.rowconfigure(1, weight=1)

        self.controller = Controller()
        self.data_controller = data_controller


        self.controls = Controls(self, self.controller)
        self.controls.grid()

        self.viewer: Viewer = Viewer(self, self.controller)
        self.viewer.grid(sticky="nsew")



        self.mainloop()
