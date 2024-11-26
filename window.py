import tkinter as tk
from controller import Controller

import pandas as pd

import pandas as pd

from controls import Controls
from viewer import Viewer

from data_controller import DataController


class Application(tk.Tk):
    def __init__(self, data_controller: DataController):
        super().__init__()
        self.geometry("500x500")
        self.title("Data Visualiser")

        self.controller = Controller()
        self.data_controller = data_controller


        self.controls = Controls(self, self.controller)
        self.controls.grid()

        self.viewer = Viewer(self, self.controller)
        self.viewer.grid()



        self.mainloop()

class Window:
    def __init__(self, controller: Controller, data_controller: DataController):
        self.controller = controller
        self.data_controller = data_controller

        # window stuff
        self.window = tk.Tk()
        self.window.geometry("500x500")


        # plot stuff

        # run window
        self.window.mainloop()

    def plot(self, y: list[int]) -> None:
        """plot a function"""

        self.plot1.clear()
        self.plot1.plot(y)
        self.canvas.draw()

        self.toolbar.update()

    def plot_bargraph(self, df: pd.DataFrame, x_col: str, y_col: str, title: str = "Graph") -> None:
        self.plot1.clear()
        
        bars = self.plot1.bar(
            df[x_col],
            df[y_col]
        )

        if title:
            self.plot1.set_title(title)
        
        self.canvas.draw()
        self.toolbar.update()

    def change_file(self, new_file_path: str) -> None:
        """ Change selected data file and instantiate new data controller for it """
        self.data_controller.change_file(new_file_path)

        df = self.data_controller.top_k_countries(10)

        self.plot_bargraph(df, df.columns[0], df.columns[1])


if __name__ == "__main__":
    app = Application(DataController())
    app.mainloop()
