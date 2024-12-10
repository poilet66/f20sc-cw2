import tkinter as tk
from controller import Controller
from data_controller import DataController

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

class GraphWindow(tk.Tk):
    def __init__(self, data_controller):
        super().__init__()
        self.geometry("500x450")
        self.title("Also Likes Graph")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0)
        self.rowconfigure(1, weight=1)

        self.viewer: CmdViewer = CmdViewer(self)
        self.data_controller: DataController = data_controller
        self.viewer.grid(sticky="nsew")

        # individual axes for each type of plot
        self.line_plot_axes = self.viewer.fig.add_subplot(111)
        self.bar_plot_axes = self.viewer.fig.add_subplot(111)
        self.graph_axis = self.viewer.fig.add_subplot(111)

        self.active_axes = self.line_plot_axes

        self.lift()

        self.viewer.plot_image(
            self.data_controller.image_from_graph(
                self.data_controller.graph_from_data(self.data_controller.also_likes_data())
            )
        )

        self.mainloop()

class CmdViewer(ttk.Frame):

    def __init__(self, parent: tk.Misc):
        super().__init__(parent)

        self.parent = parent

        # set up canvas
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # add toolbars
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

    def change_axes(self, axes: Axes):
        """ Change and update the drawn axes (type of plot)"""
        for ax in [self.parent.line_plot_axes, self.parent.bar_plot_axes, self.parent.graph_axis]:
            ax.set_visible(ax == axes)
        self.active_axes = axes
        self.canvas.draw()
        self.toolbar.update()

    def plot_image(self, image: np.ndarray[Any, Any]) -> None:
        """Plot an image/graph visualisation"""
        self.change_axes(self.parent.graph_axis)
        self.active_axes.clear()
        self.active_axes.imshow(image)
        self.active_axes.axis('off')
        self.canvas.draw()

