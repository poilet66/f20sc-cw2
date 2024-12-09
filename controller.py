import argparse
from pathlib import Path
import time
import threading

from command_line.arg_types import ArgTypes

from data_controller import DataController
from typing import TYPE_CHECKING, Optional, Callable
if TYPE_CHECKING:
    from viewer import Viewer 
    from controls import Controls


class Modes:
    Q2A = "Q2A"
    Q2B = "Q2B"
    Q3A = "Q3A"
    Q3B = "Q3B"
    Q4 = "Q4"
    Q5 = "Q5"

class Controller:
    def __init__(self):
        self.viewer: Optional["Viewer"] = None
        self.controls: Optional["Controls"] = None
        self.data_controller = DataController()


    def register_controls(self, controls: "Controls"):
        self.controls = controls

    def register_viewer(self, viewer: "Viewer"):
        self.viewer = viewer

    
    ################################################################################
    #                              Question Functions                              #
    ################################################################################

    def search(self, ids: tuple[str, str]) -> None:

        if not (self.viewer and self.controls):
            return

        if not self.data_controller.has_file():
            self.controls.display_status("No data selected!")
            return

        # check for search params
        doc_id, user_id = ids

        if doc_id != "":
            try:
                self.data_controller.set_document_filter(ArgTypes.doc_uuid_type(doc_id))
            except argparse.ArgumentTypeError:
                self.controls.display_status("Wrong uuid format")
                

        if user_id != "":
            try:
                self.data_controller.set_user_filter(ArgTypes.user_uuid_type(doc_id))
            except argparse.ArgumentTypeError:
                self.controls.display_status("Wrong uuid format")


        match self.controls.mode.get():
            case Modes.Q2A:
                self.plot_countries()
            case Modes.Q2B:
                self.plot_continents()
            case Modes.Q3A:
                self.plot_browsers(verbose=True)
            case Modes.Q3B:
                self.plot_browsers(verbose=False)
            case Modes.Q4:
                self.plot_top_readers()
            case Modes.Q5:
                self.display_graph()
            case _:
                pass


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

    def on_file_change(self, new_file_path: str):
        self.controls.display_status("Loading file...")
        filename = Path(new_file_path).name
        self.do_long_task(lambda: self.data_controller.change_file(new_file_path), lambda: self.controls.display_status(f"File Loaded:\n{filename}"))


    ################################################################################
    #                               Helper Functions                               #
    ################################################################################

    def do_long_task(self, task: Callable[[], None], callback: Optional[Callable[[], None]] = None):
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
            if callback:
                callback()
        
        # Start the checker thread
        threading.Thread(target=check_completion).start()

    def long_task_example(self):
        print("starting")
        time.sleep(1)
        print("finishing")

    def display_graph(self):
        if self.viewer:
            user_id = '3e92caf3e56ad750'
            doc_id = '130824023411-ac90acabcb403cebc8024fa0c418f403'
            # get graph data
            graph_data = self.data_controller.also_likes_data(
                user_id=user_id, doc_id=doc_id
            )
            # get graph image
            graph = self.data_controller.graph_from_data(graph_data, user_id=user_id, doc_id=doc_id)
            # Check we have graphviz enabled
            if graph is None:
                self.controls.display_status('GraphViz not installed!')
                return
            graph_image = self.data_controller.image_from_graph(graph) # get image data from test graph
            self.viewer.plot_image(graph_image) # render graph image
