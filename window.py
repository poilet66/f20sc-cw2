import tkinter as tk
from controller import Controller

from controls import Controls
from viewer import Viewer

from data_controller import DataController


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("Data Visualiser")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0)
        self.rowconfigure(1, weight=1)

        self.controller = Controller()


        self.controls = Controls(self, self.controller)
        self.controls.grid(sticky="ew")

        self.viewer: Viewer = Viewer(self, self.controller)
        self.viewer.grid(sticky="nsew")

        self.controller.register_viewer(self.viewer)

        self.mainloop()

class Window:
    def __init__(self, controller: Controller, data_controller: DataController):
        self.controller = controller
        self.data_controller = data_controller

        # window stuff
        self.window = tk.Tk()
        self.window.geometry("500x500")


        # plot stuff

        # run window
        self.window.mainloop()