from tkinter import StringVar, ttk

import tkinter as tk
from components.file_select import SelectFile
from components.button import Button
from components.radio_button import RadioButton
from controller import Controller, Modes


class Controls(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller: Controller):
        super().__init__(parent)

        print(Modes.SQR)
        self.mode = StringVar(parent, Modes.SQR)

        self.controller = controller
        self.controller.register_controls(self)

        self.q_buttons: list[Button | RadioButton] = []

        self.fileSelector = SelectFile(self, controller.on_file_change)
        self.file = tk.Text(self, height=1, width=20)

        self.randomBTN = RadioButton(self, text="random button", variable=self.mode, value=Modes.RND)
        self.squareBTN = RadioButton(self, text="square button", variable=self.mode, value=Modes.SQR)
        self.q_buttons.append(self.randomBTN)
        self.q_buttons.append(self.squareBTN)

        #q2
        self.countryBTN = RadioButton(self, text="country", variable=self.mode, value=Modes.Q2A)
        self.continentBTN = RadioButton( self, text="continent", variable=self.mode, value=Modes.Q2B)
        self.q_buttons.append(self.countryBTN)
        self.q_buttons.append(self.continentBTN)

        #q3
        self.browsersVerboseBTN = RadioButton(self, text="browser verbose", variable=self.mode, value=Modes.Q3A)
        self.browsersBTN = RadioButton(self, text="browser", variable=self.mode, value=Modes.Q3B)
        self.q_buttons.append(self.browsersBTN)
        self.q_buttons.append(self.browsersVerboseBTN)

        #q4
        self.readerProfileBTN = RadioButton(self, text="reader profile", variable=self.mode, value=Modes.Q4)
        self.q_buttons.append(self.readerProfileBTN)

        #q5
        self.alsoLikesBTN = RadioButton(self, text="Also likes", variable=self.mode, value=Modes.Q5)
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
        self.randomBTN.grid(row=0, column=1, sticky="w")
        self.squareBTN.grid(row=1, column=1, sticky="w")
        self.countryBTN.grid(row=0, column=2, sticky="w")
        self.continentBTN.grid(row=1, column=2, sticky="w")
        self.browsersVerboseBTN.grid(row=0, column=3, sticky="w")
        self.browsersBTN.grid(row=1, column=3, sticky="w")
        self.readerProfileBTN.grid(row=0, column=4, sticky="w")
        self.alsoLikesBTN.grid(row=2, column=1, sticky="w")
        self.globalUUID.grid(row=0, column=5, sticky="w")
        self.textInput.grid(row=1, column=5, sticky="w")
        self.searchBTN.grid(row=2, column=5, sticky="w")

    def disable(self):
        self.file.config(state=tk.DISABLED)
        self.fileSelector.config(state=tk.DISABLED)
        list(map(lambda x: x.set_enable(False), self.q_buttons)) # looks a bit jank ik
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
        list(map(lambda x: x.set_enable(True), self.q_buttons)) # looks a bit jank ik
        self.globalUUID.config(state=tk.NORMAL)
        self.textInput.config(state=tk.NORMAL)
        self.searchBTN.config(state=tk.NORMAL)
