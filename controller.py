import random
import time
import threading


from data_controller import DataController
from typing import TYPE_CHECKING, Optional, Callable
if TYPE_CHECKING:
    from viewer import Viewer 
    from controls import Controls


class Modes:
    RND = "RND"
    SQR = "SQR"
    Q2A = "Q2A"
    Q2B = "Q2B"
    Q3A = "Q3A"
    Q3B = "Q3B"
    Q4 = "Q4"
    Q5 = "Q5"
    Q6 = "Q6"

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


    def plot_countries(self):
        if self.viewer:
            df = self.data_controller.top_k_countries(10)
            self.viewer.plot_bargraph(df, df.columns[0], df.columns[1], title = "Viewage by Country")

    def plot_continents(self):
        if self.viewer:
            df = self.data_controller.top_continents()
            self.viewer.plot_bargraph(df, df.columns[0], df.columns[1], title="Viewage by Continent", tight=True)

    def plot_browsers(self, verbose = True):
        if self.viewer:
            df = self.data_controller.top_browsers(verbose)
            self.viewer.plot_bargraph(df, df.columns[0], df.columns[1], title="Viewage by Browser Agent")

    def plot_top_readers(self):
        if self.viewer:
            df = self.data_controller.top_k_readers(10)
            self.viewer.plot_bargraph(df, df.columns[0], df.columns[1], title="Top 10 Readers by Read Time")

    def on_file_change(self, new_file_path):
        self.data_controller.change_file(new_file_path)

    def toggle_global(self):
        self.data_controller.global_toggled = not self.data_controller.global_toggled
        print(f'global: {self.data_controller.global_toggled}')

    def search(self, inputted_doc_id: Optional[str]):
        # TODO remove
        time.sleep(1) # emulate long task

        if not (self.viewer and self.controls):
            return

        # TODO uncomment
        #if not self.data_controller.has_file():
            # TODO: popup
            print("no data selected")
            return
        
        # Set data_controller doc_id if necessary
        if inputted_doc_id is not None and inputted_doc_id != "": # If doc id provided
            self.data_controller.set_document_filter(inputted_doc_id)
            print(f'doc id set to: {inputted_doc_id}')

        # TODO: Enum
        match self.controls.mode.get():
            case Modes.RND:
                self.viewer.plot([random.random() for _ in range(121)])
            case Modes.SQR:
                self.viewer.plot([i**2 for i in range(121)])
            case Modes.Q2A:
                self.plot_countries()
            case Modes.Q2B:
                self.plot_continents()
            case Modes.Q3A:
                self.plot_browsers(verbose=False)
            case Modes.Q4:
                self.plot_browsers(verbose=True)
            case Modes.Q5:
                self.plot_top_readers()
            case Modes.Q6:
                self.display_graph()
            case _:
                return "Something's wrong with the internet"

    def do_long_task(self, task: Callable):
        print('doing long task')
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

    def display_graph(self):
        if self.viewer:
            graph_image = self.data_controller.image_from_graph(self.data_controller.get_test_graph()) # get image data from test graph
            self.viewer.plot_image(graph_image)
