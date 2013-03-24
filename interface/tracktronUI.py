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

        self.dail_size = 250
        self.dial=Canvas(frame, width=self.dail_size, height=self.dail_size)
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
        size = self.dail_size
        offs = 15
        self.dial.create_oval(offs,offs,size-offs,size-offs)

        self.line = self.dial.create_line(size/2,size/2,size/2,size-offs, fill="red", width = 2)

        self.dial.create_line(offs,size/2,size-offs,size/2)
        self.dial.create_line(size/2,offs,size/2,size-offs)

        self.dial_text = self.dial.create_text( size/2, size-offs, fill="red", text = str(self.angle), anchor="sw" )

    def update_dial(self):
        size = self.dail_size
        offs = 15

        self.angle = self.angle + 5
        length = (size-2*offs)/2

        x = length* cos(radians(self.angle))
        y = length* sin(radians(self.angle))
        self.dial.coords(self.line, size/2, size/2, x+size/2, y+size/2)

        if (self.angle+90)%360 in range(90,270): anchor = "n"
        else: anchor = "s"

        if (self.angle+90)%360 in range(0,180): anchor += "w"
        else: anchor += "e"

        self.dial.itemconfig(self.dial_text, text = str((self.angle+90)%360), anchor = anchor)
        self.dial.coords(self.dial_text, x+size/2, y+size/2)

        self.master.after(100, self.update_dial)



if __name__ == '__main__':
    mega1=serialcommu.mega()
    root = Tk()
    app = App(root,mega1)
    root.mainloop()
    try: mega1.stop()
    except: pass