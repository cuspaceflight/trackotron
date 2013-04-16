from Tkinter import *
from PIL import Image, ImageTk
import sys
import serialcommu
from math import cos, sin, radians
import threading
import random

class App:
    def __init__(self, master,mega1):
        self.master=master
        self.mega1=mega1

        self.frame = frame = Frame(master)
        frame.pack()

        dial1 = dial(frame,"Azimuth")
        dial1.update_dial()
        dial2 = dial(frame,"Elevation")
        dial2.update_dial()

        self.w = Canvas(frame, width=200, height=100)
        self.w.pack()

        self.quit_button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.quit_button.pack(side=LEFT)

        self.connect_button = Button(frame, text="Connect", fg="black", command=self.mega1.connect)
        self.connect_button.pack(side=LEFT)

        self.online = 0
        self.draw_online_indicator()
        self.update_online_variable()
        self.update_indicator()

    def draw_online_indicator(self):
        self.ind_rect = self.w.create_rectangle(50, 25, 150, 75, fill="red")

    def update_online_variable(self):
        def pinging(): self.online = self.mega1.ping()
        pinging_thread = threading.Thread( target = pinging )
        pinging_thread.start()
        self.frame.after(100, self.update_online_variable)

    def update_indicator(self):
        if self.online: fill_colour = "green"
        else: fill_colour = "red"

        self.w.itemconfig(self.ind_rect, fill = fill_colour)

        #every 2 sec redraw indicator
        self.frame.after(100, self.update_indicator)

class dial(object):
    def __init__(self, frame, name):
        self.master = frame
        self.dail_size = size = 250
        self.offs = offs = 50
        self.dial=Canvas(frame, width=self.dail_size, height=self.dail_size)
        self.dial.pack(side = LEFT)

        # draw the circle
        self.dial.create_oval(offs,offs,size-offs,size-offs)

        # draw the cross in the circle
        self.dial.create_line(offs,size/2,size-offs,size/2)
        self.dial.create_line(size/2,offs,size/2,size-offs)

        def draw_pointer( colour ):
            ptr     = self.dial.create_line(size/2,size/2,size/2,size-offs, fill=colour, width = 1)
            ptr_txt = self.dial.create_text(size/2, size-offs, fill=colour, text = str(0), anchor="sw")
            return ptr, ptr_txt

        # draw 3 pointers
        self.ptr1, self.ptr1_txt = draw_pointer("red")
        self.ptr2, self.ptr2_txt = draw_pointer("blue")
        self.ptr3, self.ptr3_txt = draw_pointer("green")
        self.angle1 = self.angle2 = self.angle3 = 0

        # draw texts at the bottom
        self.dial.create_rectangle( size/2-45, size-39, size/2+45, size-1,fill = "white" )
        self.text1 = self.dial.create_text( size/2-43, size-1,  text="Sensor", fill = "red", anchor="sw")
        self.text2 = self.dial.create_text( size/2-43, size-12, text="Dead",  fill = "blue", anchor="sw")
        self.text3 = self.dial.create_text( size/2-43, size-23, text="Target", fill = "green", anchor="sw")

        # label the dial
        self.dial.create_text( size/2, 20, text=name, fill = "Black", anchor="s")

    def update_dial(self):
        size = self.dail_size
        offs = self.offs
        length = (size-2*offs)/2

        # update the readings of the pointers
        self.angle1 = (self.angle1 + (random.random()-0.3)*5)%360
        self.angle2 = (self.angle2 + (random.random()-0.3)*5)%360
        self.angle3 = (self.angle3 + (random.random()-0.3)*5)%360

        def update_pointer(angle, ptr, ptr_txt, legend):
            x = length* cos(radians(angle-90))
            y = length* sin(radians(angle-90))
            self.dial.coords(ptr, size/2, size/2, x+size/2, y+size/2)

            if round(angle) in range(90,270): anchor = "n"
            else: anchor = "s"

            if round(angle) in range(0,180): anchor += "w"
            else: anchor += "e"

            self.dial.itemconfig(ptr_txt, text = str(round((angle)%360)), anchor = anchor)
            self.dial.coords(ptr_txt, x+size/2, y+size/2)
            update_text = self.dial.itemcget(legend, "text").split()[0].ljust(10)
            self.dial.itemconfig( legend, text = update_text + "%0.1f" %angle )

        # update the pointers
        update_pointer(self.angle1,self.ptr1, self.ptr1_txt, self.text1)
        update_pointer(self.angle2,self.ptr2, self.ptr2_txt, self.text2)
        update_pointer(self.angle3,self.ptr3, self.ptr3_txt, self.text3)

        self.master.after(100, self.update_dial)

if __name__ == '__main__':
    mega1=serialcommu.mega()
    root = Tk()
    app = App(root,mega1)
    root.mainloop()
    try: mega1.stop()
    except: pass