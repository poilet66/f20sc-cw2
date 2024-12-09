import tkinter as tk
from typing import Optional

class Text(tk.Entry):
    def __init__(self, master: tk.Misc, placeholder: Optional[str]):
        super().__init__(master, width=20)
        self.placeholder: str = placeholder or ""
        self.config(fg="grey")


        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, _: tk.Event[tk.Entry]):
        # hide placeholder
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg="black")

    def on_focus_out(self, _: tk.Event[tk.Entry]):
        # show placeholder
        if self.get() == "":
            self.insert(0, self.placeholder)
            self.config(fg="grey")

    def get_value(self) -> str:
        return self.get("1.0", "end").strip()
