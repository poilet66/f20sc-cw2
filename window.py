import tkinter as tk
from controller import Controller

from controls import Controls
from viewer import Viewer

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
