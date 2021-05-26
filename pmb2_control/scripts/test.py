from Tkinter import *
from threading import Thread
import signal

class MyTkApp(Thread):
    def run(self):
        self.root = Tk()
        self.root.mainloop()

def sigint_handler(sig, frame):
    app.root.quit()
    app.root.update()

app = MyTkApp()

# Set signal before starting
signal.signal(signal.SIGINT, sigint_handler)

app.start()