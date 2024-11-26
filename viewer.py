import tkinter as tk
from tkinter import ttk
from controller import Controller, Event

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk


class Viewer(ttk.Frame):
    def __init__(self, parent: tk.Misc, controller: Controller):
        super().__init__(parent)
        self.controller = controller



        fig = Figure(figsize=(5, 5), dpi=100)
        self.plot1 = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.get_tk_widget().pack()
        self.toolbar.update()

        self.plot([i**2 for i in range(101)])

        self.controller.add_listener(Event.A, self.plot)


    def plot(self, y) -> None:
        """plot a function"""

        self.plot1.clear()
        self.plot1.plot(y)
        self.canvas.draw()

        self.toolbar.update()

