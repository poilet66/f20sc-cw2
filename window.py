import tkinter as tk
from controller import Controller

import pandas as pd

import pandas as pd

from controls import Controls
from viewer import Viewer

from data_controller import DataController


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Data Visualiser")

        self.controller = Controller()


        self.controls = Controls(self, self.controller)
        self.controls.grid()

        self.viewer: Viewer = Viewer(self, self.controller)
        self.viewer.grid()

        self.controller.register_viewer(self.viewer)

        self.mainloop()

class Window:
    def __init__(self, controller: Controller):
        self.controller = controller

        # window stuff
        self.window = tk.Tk()
        self.window.geometry("500x500")


        # plot stuff

        # run window
        self.window.mainloop()