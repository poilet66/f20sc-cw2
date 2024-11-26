import tkinter as tk
from abc import ABC, abstractmethod
from typing import Callable

class ButtonBase(ABC):
    def __init__(self, master: tk.Tk, label: str, callback: Callable = None):
        self.button = tk.Button(
            master,
            text=label,
            command=self.handle_click if callback is None else callback # Allow callback function to be passed , otherwise purely rely on independent functionality
        )

    @abstractmethod
    def handle_click(self) -> None:
        pass


    def pack(self, **kwargs) -> None:
        self.button.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        self.button.grid(**kwargs)

    def config(self, **kwargs) -> None:
        self.button.config(**kwargs)
