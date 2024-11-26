import random
import tkinter as tk
from controller import Controller

from viewer import Viewer

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title("Data Visualiser")

        self.controller = Controller()

        # init stuff
        # init stuff
        # init stuff
        self.viewer = Viewer(self, self.controller)
        self.viewer.grid()

        self.mainloop()

class Window:
    def __init__(self, controller: Controller):
        self.controller = controller

        # window stuff
        self.window = tk.Tk()
        self.window.geometry("500x500")

        # button stuff
        self.rnd_btn = tk.Button(self.window, text="randoms", command=lambda: self.plot([random.randint(0, 100) for _ in range(101)]))
        self.sqr_btn = tk.Button(self.window, text="squares", command=lambda: self.plot([i**2 for i in range(101)]))
        self.rnd_btn.pack()
        self.sqr_btn.pack()

        # plot stuff

        # run window
        self.window.mainloop()



if __name__ == "__main__":
    app = Application()
    app.mainloop()
