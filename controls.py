from tkinter import ttk
import tkinter as tk
from buttons.random_button import RandomButton
from buttons.file_select import Button_SelectFile
from controller import Controller

class Controls(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller: Controller):
        super().__init__(parent)

        self.controller = controller
        self.controller.register_controls(self)

        # file select button
        self.fileBTN = Button_SelectFile(self, change_file_callback=self.controller.on_file_change)

        #q2
        self.countryBTN = ttk.Button(self, text="country", command=self.controller.plot_countries)
        self.continentBTN = ttk.Button(self, text="continent")

        #q3
        self.browsersVerboseBTN = tk.Button(self, text="browser verbose")
        self.browsersBTN = tk.Button(self, text="browser")

        #q4
        self.readerProfileBTN = tk.Button(self, text="reader profile")

        #q5
        self.alsoLikesBTN = tk.Button(self, text="Also likes")

        self.globalUUID = tk.Checkbutton(self, text="global", command=controller.toggle_global) # select to toggle by default
        self.globalUUID.select()
        self.textInput = tk.Text(self, height=1, width=20)

        self.countryBTN.pack(side=tk.LEFT)
        self.continentBTN.pack(side=tk.LEFT)
        self.browsersVerboseBTN.pack(side=tk.LEFT)
        self.browsersBTN.pack(side=tk.LEFT)
        self.readerProfileBTN.pack(side=tk.LEFT)
        self.globalUUID.pack(side=tk.RIGHT)
        self.textInput.pack(side=tk.RIGHT)
        self.fileBTN.pack(side=tk.RIGHT)

    def disable(self):
        self.countryBTN.config(state=tk.DISABLED)
        self.continentBTN.config(state=tk.DISABLED)
        self.browsersVerboseBTN.config(state=tk.DISABLED)
        self.browsersBTN.config(state=tk.DISABLED)
        self.readerProfileBTN.config(state=tk.DISABLED)
        self.globalUUID.config(state=tk.DISABLED)
        self.textInput.config(state=tk.DISABLED)

    def enable(self):
        self.countryBTN.config(state=tk.NORMAL)
        self.continentBTN.config(state=tk.NORMAL)
        self.browsersVerboseBTN.config(state=tk.NORMAL)
        self.browsersBTN.config(state=tk.NORMAL)
        self.readerProfileBTN.config(state=tk.NORMAL)
        self.globalUUID.config(state=tk.NORMAL)
        self.textInput.config(state=tk.NORMAL)
