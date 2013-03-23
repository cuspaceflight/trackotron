from Tkinter import *
from PIL import Image, ImageTk
import sys
import serialcommu

class App:

    def __init__(self, master,mega1):
        self.master=master
        self.mega1=mega1

        frame = Frame(master)
        frame.pack()
        
        self.w = Canvas(master, width=200, height=100)
        self.w.pack()

        self.quit = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.quit.pack(side=LEFT)
        
        self.connect_button = Button(frame, text="Connect", fg="black", command=self.connect)
        self.connect_button.pack(side=LEFT)
        
        self.online = 0;
        self.poll()
    
    def poll(self):
        self.draw_online_indicator()
        self.master.after(1000, self.poll)

    def draw_online_indicator(self):
        self.online = self.mega1.ping()
        if self.online: fill_colour = "green"
        else: fill_colour = "red"
        self.w.create_rectangle(50, 25, 150, 75, fill=fill_colour)
        
    def connect(self):
        self.mega1.connect()

if __name__ == '__main__':
    mega1=serialcommu.mega()
    root = Tk()
    app = App(root,mega1)
    root.mainloop()
    mega1.stop()