import random
class Controller:
    def __init__(self):
        self.viewer = None
        self.controls = None

    def register_controls(self, controls):
        self.controls = controls

    def register_viewer(self, viewer):
        self.viewer = viewer


    def plot_random(self):
        # set viewer to randoms
        if self.viewer:
            self.viewer.plot([random.random() for _ in range(121)])

    def plot_squares(self):
        if self.viewer:
            self.viewer.plot([i**2 for i in range(121)])

    def change_file(self):
        # 
        pass

