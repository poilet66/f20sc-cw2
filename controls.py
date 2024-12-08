from tkinter import StringVar, ttk

import tkinter as tk
from components.file_select import SelectFile
from components.button import Button
from components.radio_button import RadioButton
from components.text import Text
from controller import Controller, Modes


class Controls(ttk.Frame):

    def __init__(self, parent: tk.Misc, controller: Controller):
        super().__init__(parent)

        print(Modes.SQR)
        self.mode = StringVar(parent, Modes.SQR)

        self.controller = controller
        self.controller.register_controls(self)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.q_buttons: list[RadioButton] = []

        self.fileSelector = SelectFile(self, controller.on_file_change)
        self.status = tk.Label(self, text="Select File", height=3, width=20, wraplength=200, justify="center")

        self.center_frame = ttk.Frame(self)

        # test buttons
        self.randomBTN = RadioButton(self.center_frame, text="Random Button", variable=self.mode, value=Modes.RND)
        self.squareBTN = RadioButton(self.center_frame, text="Square Button", variable=self.mode, value=Modes.SQR)
        self.q_buttons.append(self.randomBTN)
        self.q_buttons.append(self.squareBTN)

        #q2
        self.countryBTN = RadioButton(self.center_frame, text="Country", variable=self.mode, value=Modes.Q2A)
        self.continentBTN = RadioButton(self.center_frame, text="Continent", variable=self.mode, value=Modes.Q2B)
        self.q_buttons.append(self.countryBTN)
        self.q_buttons.append(self.continentBTN)

        #q3
        self.browsersVerboseBTN = RadioButton(self.center_frame, text="Browser Verbose", variable=self.mode, value=Modes.Q3A)
        self.browsersBTN = RadioButton(self.center_frame, text="Browser", variable=self.mode, value=Modes.Q3B)
        self.q_buttons.append(self.browsersBTN)
        self.q_buttons.append(self.browsersVerboseBTN)

        #q4
        self.readerProfileBTN = RadioButton(self.center_frame, text="Reader Profile", variable=self.mode, value=Modes.Q4)
        self.q_buttons.append(self.readerProfileBTN)

        #q5
        self.alsoLikesBTN = RadioButton(self.center_frame, text="Also likes", variable=self.mode, value=Modes.Q5)
        self.q_buttons.append(self.alsoLikesBTN)

        self.docUUID = Text(self, placeholder="Documnet UUID")
        self.userUUID = Text(self, placeholder="User UUID")
        self.searchBTN = Button(
            self, 
            text="Search", 
            command=lambda: controller.do_long_task(lambda: controller.search(self.get_ids()))  # This is sorta scuffed, I'll DEFINITELY tidy it later.. /s
        )


        ### adding to display
        self.fileSelector.grid(row=0, column=0)
        self.status.grid(row=1, column=0, rowspan=2)

        self.center_frame.grid(row=0, column=1, rowspan=3)

        self.docUUID.grid(row=0, column=5, sticky="w")
        self.userUUID.grid(row=1, column=5, sticky="w")
        self.searchBTN.grid(row=2, column=5)

        # question buttons
        self.randomBTN.grid(row=0, column=0, sticky="w")
        self.squareBTN.grid(row=1, column=0, sticky="w")
        self.countryBTN.grid(row=0, column=1, sticky="w")
        self.continentBTN.grid(row=1, column=1, sticky="w")
        self.browsersVerboseBTN.grid(row=0, column=2, sticky="w")
        self.browsersBTN.grid(row=1, column=2, sticky="w")
        self.readerProfileBTN.grid(row=0, column=3, sticky="w")
        self.alsoLikesBTN.grid(row=2, column=0, sticky="w")

    def disable(self):
        self.fileSelector.config(state=tk.DISABLED)
        list(map(lambda x: x.set_enable(False), self.q_buttons)) # looks a bit jank ik
        self.userUUID.config(state=tk.DISABLED)
        self.docUUID.config(state=tk.DISABLED)
        self.searchBTN.config(state=tk.DISABLED)

    def disable_search(self):
        self.searchBTN.config(state=tk.DISABLED)

    def enable_search(self):
        self.searchBTN.config(state=tk.NORMAL)

    def enable(self):
        self.fileSelector.config(state=tk.NORMAL)
        list(map(lambda x: x.set_enable(True), self.q_buttons)) # looks a bit jank ik
        self.userUUID.config(state=tk.NORMAL)
        self.docUUID.config(state=tk.NORMAL)
        self.searchBTN.config(state=tk.NORMAL)

    def display_status(self, message: str):
        self.status.config(text=message)

    def get_ids(self) -> tuple[str, str]:
        return (self.docUUID.get(), self.userUUID.get())
