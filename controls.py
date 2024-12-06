from tkinter import ttk
import tkinter as tk
from components.file_select import SelectFile
from components.button import Button
from controller import Controller


class Controls(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller: Controller):
        super().__init__(parent)

        self.controller = controller
        self.controller.register_controls(self)

        self.q_buttons: list[Button] = []

        self.fileSelector = SelectFile(self, controller.on_file_change)
        self.file = tk.Text(self, height=1, width=20)

        self.randomBTN = Button(self, text="random button", command=lambda: controller.set_mode("Random"))
        self.squareBTN = Button(self, text="square button", command=lambda: controller.set_mode("Square"))
        self.q_buttons.append(self.randomBTN)
        self.q_buttons.append(self.squareBTN)

        #q2
        self.countryBTN = Button(self, text="country", command=lambda: self.controller.set_mode("country"))
        self.continentBTN = Button( self, text="continent", command=lambda: self.controller.set_mode("Continent"))
        self.q_buttons.append(self.countryBTN)
        self.q_buttons.append(self.continentBTN)

        #q3
        self.browsersVerboseBTN = Button(self, text="browser verbose", command=lambda: self.controller.set_mode("Browser-Verbose"))
        self.browsersBTN = Button(self, text="browser", command=lambda: self.controller.set_mode("Browser"))
        self.q_buttons.append(self.browsersBTN)
        self.q_buttons.append(self.browsersVerboseBTN)

        #q4
        self.readerProfileBTN = Button(self, text="reader profile", command=lambda: self.controller.set_mode("Top-Readers"))
        self.q_buttons.append(self.readerProfileBTN)

        #q5
        self.alsoLikesBTN = Button(self, text="Also likes", command=lambda: self.controller.set_mode("graphviz"))
        self.q_buttons.append(self.alsoLikesBTN)

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
        list(map(lambda x: x.set_enable(False), self.q_buttons))
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
        list(map(lambda x: x.set_enable(True), self.q_buttons))
        self.squareBTN.config(state=tk.NORMAL)
        self.globalUUID.config(state=tk.NORMAL)
        self.textInput.config(state=tk.NORMAL)
        self.searchBTN.config(state=tk.NORMAL)
