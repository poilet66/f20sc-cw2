import tkinter as tk
from time import strftime

class DigitalClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Digital Clock")
        
        # Create and configure the label
        self.clock_label = tk.Label(
            self.root,
            font=('Helvetica', 40),
            background='black',
            foreground='cyan',
            pady=20,
            padx=20
        )
        self.clock_label.pack()
        
        # Start the clock update
        self.update_time()

        print('test')
        
    def update_time(self):
        # Get current time and update label
        time_string = strftime('%H:%M:%S')
        self.clock_label.config(text=time_string)
        # Schedule the next update after 1000ms (1 second)
        self.root.after(1000, self.update_time)

        print(strftime('%H:%M:%S'))
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    clock = DigitalClock()
    clock.run()