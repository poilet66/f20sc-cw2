class Controller:
    def __init__(self, ):
        self.viewer = None
        self.controls = None

    def register_controls(self, controls):
        self.controls = controls

    def register_viewer(self, viewer):
        self.viewer = viewer

