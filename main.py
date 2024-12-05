from command_line.cmdline import CommandLineHandler
from window import Application

if __name__ == "__main__":

    cmdline = CommandLineHandler()

    if cmdline.has_args():
        cmdline.run()
    else:
        app = Application()
        app.mainloop()
