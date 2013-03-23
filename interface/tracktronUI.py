from Tkinter import *
from PIL import Image, ImageTk
import sys
import serialcommu
from math import cos, sin, radians

class App:

    def __init__(self, master,mega1):
        self.master=master
        self.mega1=mega1

        frame = Frame(master)
        frame.pack()

        self.w = Canvas(frame, width=200, height=100)
        self.w.pack()

        self.dial=Canvas(frame, width=100, height=100)
        self.dial.pack()

        self.quit_button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.quit_button.pack(side=LEFT)

        self.connect_button = Button(frame, text="Connect", fg="black", command=self.mega1.connect())
        self.connect_button.pack(side=LEFT)

        self.online = 0
        self.draw_online_indicator()
        self.update_indicator()
        self.angle = 0
        self.draw_dial()
        self.update_dial()

    def draw_online_indicator(self):
        self.ind_rect = self.w.create_rectangle(50, 25, 150, 75, fill="red")

    def update_indicator(self):
        self.online = self.mega1.ping()

        if self.online: fill_colour = "green"
        else: fill_colour = "red"

        self.w.itemconfig(self.ind_rect, fill = fill_colour)

        #every 1 sec redraw indicator
        self.master.after(1000, self.draw_online_indicator)

    def draw_dial(self):
        print"drawing oval"
        self.dial.create_oval(2,2,98,98)
        self.line = self.dial.create_line(50,50,50,50, fill="red", width = 2)
        self.dial.create_line(2,50,98,50)
        self.dial.create_line(50,2,50,98)

    def update_dial(self):
        self.angle = self.angle + 20
        length = 50
        x = length* cos(radians(self.angle))
        y = length* sin(radians(self.angle))
        self.dial.coords(self.line, 50, 50, x+50, y+50)
        self.master.after(10, self.update_dial)



if __name__ == '__main__':
    mega1=serialcommu.mega()
    root = Tk()
    app = App(root,mega1)
    root.mainloop()
    mega1.stop()