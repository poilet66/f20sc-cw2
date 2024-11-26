import random
import tkinter as tk
from controller import Controller

from controls import Controls
from viewer import Viewer
from buttons.random_button import RandomButton
from buttons.file_select import Button_SelectFile

from data_controller import DataController


class Application(tk.Tk):
    def __init__(self, data_controller: DataController):
        super().__init__()
        self.geometry("500x500")
        self.title("Data Visualiser")

        self.controller = Controller()
        self.data_controller = data_controller

        self.viewer = Viewer(self, self.controller)
        self.viewer.grid()

        self.controls = Controls(self, self.controller)
        self.controls.grid()



        self.mainloop()

class Window:
    def __init__(self, controller: Controller, data_controller: DataController):
        self.controller = controller
        self.data_controller = data_controller

        # window stuff
        self.window = tk.Tk()
        self.window.geometry("500x500")

        # button stuff
        self.rnd_btn = RandomButton(self.window, plot_callback=self.plot)
        #self.rnd_btn = tk.Button(self.window, text="randoms", command=lambda: self.plot([random.randint(0, 100) for _ in range(101)]))
        self.sqr_btn = tk.Button(self.window, text="squares", command=lambda: self.plot([i**2 for i in range(101)]))
        self.file_btn = Button_SelectFile(self.window, change_file_callback=self.change_file)
        self.rnd_btn.pack()
        self.sqr_btn.pack()
        self.file_btn.pack()

        # plot stuff

        # run window
        self.window.mainloop()


    def change_file(self, new_file_path: str) -> None:
        """ Change selected data file and instantiate new data controller for it """
        self.data_controller.change_file(new_file_path)


if __name__ == "__main__":
    app = Application(DataController())
    app.mainloop()
