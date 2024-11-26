from window import Application
from data_controller import DataController

if __name__ == "__main__":
    app = Application(DataController())
    app.mainloop()
