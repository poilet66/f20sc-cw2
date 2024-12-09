import tkinter as tk
from tkinter import ttk
from typing import Any

from matplotlib.axes import Axes
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

        # set up canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # add toolbars
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        # individual axes for each type of plot
        self.line_plot_axes = self.fig.add_subplot(111)
        self.bar_plot_axes = self.fig.add_subplot(111)
        self.graph_axis = self.fig.add_subplot(111)

        self.active_axes = self.line_plot_axes

        # default plot
        self.plot([i**2 for i in range(101)])


    def change_axes(self, axes: Axes):
        """ Change and update the drawn axes (type of plot)"""
        for ax in [self.line_plot_axes, self.bar_plot_axes, self.graph_axis]:
            ax.set_visible(ax == axes)
        self.active_axes = axes
        self.canvas.draw()
        self.toolbar.update()

    def plot(self, y: list[float|int]) -> None:
        """plot a linear function"""
        self.change_axes(self.line_plot_axes)
        self.active_axes.clear()
        self.active_axes.plot(y)
        self.active_axes.autoscale()
        self.canvas.draw()

    def plot_bargraph(self, df: pd.DataFrame, x_col: str, y_col: str, title: str="Graph", tight: bool=False) -> None:
        """Plot a histogram"""
                      
        self.change_axes(self.bar_plot_axes)
        self.active_axes.clear()
        self.active_axes.bar(df[x_col], df[y_col])

        if title:
            self.active_axes.set_title(title)

        if tight:
            self.active_axes.figure.tight_layout()

        self.active_axes.autoscale()
        self.canvas.draw()
        

    def plot_image(self, image: np.ndarray[Any, Any]) -> None:
        """Plot an image/graph visualisation"""
        self.change_axes(self.graph_axis)
        self.active_axes.clear()
        self.active_axes.imshow(image)
        self.active_axes.axis('off')
        self.canvas.draw()
