import random


from data_controller import DataController
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from viewer import Viewer 
    from controls import Controls

class Controller:
    def __init__(self):
        self.viewer: Optional["Viewer"] = None
        self.controls: Optional["Controls"] = None
        self.data_controller = DataController()

        # Default functionality, NOTE: this is just for testing
        self.plot_countries()


    def register_controls(self, controls: "Controls"):
        self.controls = controls

    def register_viewer(self, viewer: "Viewer"):
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

    def on_file_change(self, new_file_path):
        self.data_controller.change_file(new_file_path)

