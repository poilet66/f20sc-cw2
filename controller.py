import random

from viewer import Viewer
from controls import Controls
from data_controller import DataController
class Controller:
    def __init__(self):
        self.viewer: Viewer = None
        self.controls: Controls = None
        self.data_controller: DataController = None

    def register_controls(self, controls):
        self.controls = controls

    def register_viewer(self, viewer):
        self.viewer = viewer

    def register_data_controller(self, data_controller):
        self.data_controller = data_controller


    def plot_random(self):
        # set viewer to randoms
        if self.viewer:
            self.viewer.plot([random.random() for _ in range(121)])

    def plot_squares(self):
        if self.viewer:
            self.viewer.plot([i**2 for i in range(121)])

    def plot_countries(self):
        if self.viewer:
            df = self.data_controller.top_k_countries(10)
            self.viewer.plot_bargraph(df, df.columns[0], df.columns[1])

