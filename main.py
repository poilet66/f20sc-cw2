import tkinter as tk
import threading

import time


if __name__ == "__main__":
    a = ""

    window = tk.Tk()
    window.geometry("400x400")
    greeting = tk.Label(text=str(a))
    greeting.pack()

    a = threading.Thread(target=mainloop)
    a.start()

    window.mainloop()
