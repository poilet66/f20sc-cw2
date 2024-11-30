import random
import time
import threading


from data_controller import DataController
from typing import TYPE_CHECKING, Optional, Callable
if TYPE_CHECKING:
    from viewer import Viewer 
    from controls import Controls

class Controller:
    def __init__(self):
        self.viewer: Optional["Viewer"] = None
        self.controls: Optional["Controls"] = None
        self.data_controller = DataController()


    def register_controls(self, controls: "Controls"):
        self.controls = controls

    def register_viewer(self, viewer: "Viewer"):
        self.viewer = viewer

    def register_data_controller(self, data_controller: "DataController"):
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
            self.viewer.plot_bargraph(df, df.columns[0], df.columns[1], title = "Viewage by Country")

    def plot_continents(self):
        if self.viewer:
            df = self.data_controller.top_continents()
            self.viewer.plot_bargraph(df, df.columns[0], df.columns[1], title="Viewage by Continent", tight=True)

    def on_file_change(self, new_file_path):
        self.data_controller.change_file(new_file_path)

    def toggle_global(self):
        self.data_controller.global_toggled = not self.data_controller.global_toggled

    def search_doc(self):
        inputted_doc_id = self.controls.textInput.get("1.0", "end").strip()
        if inputted_doc_id is not None and inputted_doc_id != "": # If doc id provided
            self.data_controller.set_document_filter(inputted_doc_id)

    def do_long_task(self, task: Callable):
        # disable controls
        if self.controls:
            self.controls.disable()
        
        # start task on separate thread
        thread = threading.Thread(target=task)
        thread.start()
        
        def check_completion():
            thread.join()  # Wait for task thread to finish
            # enable controls
            if self.controls:
                self.controls.enable()
        
        # Start the checker thread
        threading.Thread(target=check_completion).start()

    def long_task_example(self):
        print("starting")
        time.sleep(1)
        print("finishing")