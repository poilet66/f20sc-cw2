import tkinter as tk
from tkinter import ttk

import pandas as pd

from controller import Controller

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk


import numpy as np

class Viewer(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller: Controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.register_viewer(self)



        fig = Figure(figsize=(5, 4), dpi=100)
        self.plot1 = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.plot([i**2 for i in range(101)])


    def plot(self, y: list[float|int]) -> None:
        """plot a function"""

        self.plot1.clear()
        self.plot1.plot(y)
        self.canvas.draw()

        self.toolbar.update()

    def plot_bargraph(self, df: pd.DataFrame, x_col: str, y_col: str, 
                      title: str = "Graph", tight = False) -> None:
                      
        self.plot1.clear()
        
        bars = self.plot1.bar(
            df[x_col],
            df[y_col]
        )

        if title:
            self.plot1.set_title(title)

        if tight:
            self.plot1.figure.tight_layout()
        
        self.canvas.draw()
        self.toolbar.update()

    def plot_image(self, image: np.ndarray) -> None:
        self.plot1.clear()
        self.plot1.imshow(image)
        self.plot1.axis('off')
        self.canvas.draw()
        self.toolbar.update()
        self.plot1.figure.clf()
