import random
import tkinter as tk
from controller import Controller

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk


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
        fig = Figure(figsize=(5, 5), dpi=100)
        self.plot1 = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.canvas.get_tk_widget().pack()

        self.plot([i**2 for i in range(101)])

        # run window
        self.window.mainloop()

    def plot(self, y: list[int]) -> None:
        """plot a function"""

        self.plot1.clear()
        self.plot1.plot(y)
        self.canvas.draw()

        self.toolbar.update()


if __name__ == "__main__":
    w = Window(Controller())
