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

        self.fileSelector = Button_SelectFile(self, controller.on_file_change)
        self.file = tk.Text(self, height=1, width=20)

        self.randomBTN = ttk.Button(self, text="random button", command=lambda: controller.set_mode("Random"))
        self.squareBTN = ttk.Button(self, text="square button", command=lambda: controller.set_mode("Square"))

        #q2
        self.countryBTN = ttk.Button(self, text="country", command=lambda: self.controller.set_mode("country"))
        self.continentBTN = ttk.Button( self, text="continent", command=lambda: self.controller.set_mode("Continent")
        )

        #q3
        self.browsersVerboseBTN = tk.Button(self, text="browser verbose", command=lambda: self.controller.set_mode("Browser-Verbose"))
        self.browsersBTN = tk.Button(self, text="browser", command=lambda: self.controller.set_mode("Browser"))

        #q4
        self.readerProfileBTN = tk.Button(self, text="reader profile", command=lambda: self.controller.set_mode("Top-Readers"))

        #q5
        self.alsoLikesBTN = tk.Button(self, text="Also likes", command=lambda: self.controller.set_mode("graphviz"))

        self.globalUUID = tk.Checkbutton(self, text="global", command=controller.toggle_global) # select to toggle by default
        self.globalUUID.select()
        self.textInput = tk.Text(self, height=1, width=20)
        self.searchBTN = tk.Button(
            self, 
            text="Search", 
            command=lambda: controller.do_long_task(lambda: controller.search(self.textInput.get("1.0", "end").strip()))  # This is sorta scuffed, I'll DEFINITELY tidy it later.. /s
        )

        self.file.grid(row=1, column=0)
        self.fileSelector.grid(row=0, column=0)
        self.randomBTN.grid(row=0, column=1)
        self.squareBTN.grid(row=1, column=1)
        self.countryBTN.grid(row=0, column=2)
        self.continentBTN.grid(row=1, column=2)
        self.browsersVerboseBTN.grid(row=0, column=3)
        self.browsersBTN.grid(row=1, column=3)
        self.readerProfileBTN.grid(row=0, column=4)
        self.alsoLikesBTN.grid(row=2, column=1)
        self.globalUUID.grid(row=0, column=5)
        self.textInput.grid(row=1, column=5)
        self.searchBTN.grid(row=2, column=5)

    def disable(self):
        self.file.config(state=tk.DISABLED)
        self.fileSelector.config(state=tk.DISABLED)
        self.randomBTN.config(state=tk.DISABLED)
        self.squareBTN.config(state=tk.DISABLED)
        self.countryBTN.config(state=tk.DISABLED)
        self.continentBTN.config(state=tk.DISABLED)
        self.browsersVerboseBTN.config(state=tk.DISABLED)
        self.browsersBTN.config(state=tk.DISABLED)
        self.readerProfileBTN.config(state=tk.DISABLED)
        self.globalUUID.config(state=tk.DISABLED)
        self.textInput.config(state=tk.DISABLED)
        self.searchBTN.config(state=tk.DISABLED)

    def disable_search(self):
        self.searchBTN.config(state=tk.DISABLED)

    def enable_search(self):
        self.searchBTN.config(state=tk.NORMAL)

    def enable(self):
        self.file.config(state=tk.NORMAL)
        self.fileSelector.config(state=tk.NORMAL)
        self.randomBTN.config(state=tk.NORMAL)
        self.countryBTN.config(state=tk.NORMAL)
        self.squareBTN.config(state=tk.NORMAL)
        self.continentBTN.config(state=tk.NORMAL)
        self.browsersVerboseBTN.config(state=tk.NORMAL)
        self.browsersBTN.config(state=tk.NORMAL)
        self.readerProfileBTN.config(state=tk.NORMAL)
        self.globalUUID.config(state=tk.NORMAL)
        self.textInput.config(state=tk.NORMAL)
        self.searchBTN.config(state=tk.NORMAL)
