from math import cos, sin, radians
from PIL import Image, ImageTk
from Tkinter import *
import serialcommu
import time
import sys




class App:
    def __init__(self, master, mega1):
        self.update_interval = 100 #ms

        self.master = master
        self.mega1 = mega1

        self.frame = frame = Frame(master)
        frame.pack()

        self.dial1 = dial(frame,"Azimuth")
        self.dial2 = dial(frame,"Elevation")

        self.online = 0
        self.draw_online_indicator()

        self.quit_button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.quit_button.pack(side=LEFT)

        self.connect_button = Button(frame, text="Connect", fg="black", command=self.mega1.connect)
        self.connect_button.pack(side=LEFT)

        self.stats = STATUS(frame,mega1)
        self.t1 = 0

        self.updating()

    def draw_online_indicator(self):
        self.w = Canvas(self.frame, width=50, height=50)
        self.w.pack()
        self.ind_rect = self.w.create_rectangle(2, 2, 48, 48, fill="red")

    def update_indicator(self):
        self.online = self.mega1.online

        if self.online: fill_colour = "green"
        else: fill_colour = "red"
        self.w.itemconfig(self.ind_rect, fill = fill_colour)

    def updating(self, ):
        #print "update is bing called"
        self.mega1.update()
        self.update_indicator()
        self.stats.update_stats()
        self.dial1.update_dial(self.mega1.sensor_az, 0, 0)
        self.dial2.update_dial(self.mega1.sensor_el, 0, 0)

        #print time.time()- self.t1
        #self.t1 = time.time()
        #sys.stdout.flush()
        #every 0.1 sec redraw UI

        self.frame.after(self.update_interval, self.updating)


class dial(object):

    def __init__(self, frame, name):
        self.master = frame
        self.dail_size = size = 250
        self.offs = offs = 30
        self.dial=Canvas(frame, width=self.dail_size, height=self.dail_size)
        self.dial.pack(side = LEFT)
        self.dial.create_rectangle(2, 2, self.dail_size-2, self.dail_size-2, fill="white")

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

        # draw texts at the bottom
        self.dial.create_rectangle( size/2-45, size-39, size/2+45, size-1,fill = "white" )
        self.text1 = self.dial.create_text( size/2-43, size-1,  text="Sensor", fill = "red",   anchor="sw")
        self.text2 = self.dial.create_text( size/2-43, size-12, text="Dead",   fill = "blue",  anchor="sw")
        self.text3 = self.dial.create_text( size/2-43, size-23, text="Target", fill = "green", anchor="sw")

        # label the dial
        self.dial.create_text( size/2, 20, text=name, fill = "Black", anchor="s")

    def update_dial(self, angle1, angle2, angle3):
        size = self.dail_size
        offs = self.offs
        length = (size-2*offs)/2

        # update the readings of the pointers

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
        update_pointer(angle1,self.ptr1, self.ptr1_txt, self.text1) # sensor
        update_pointer(angle2,self.ptr2, self.ptr2_txt, self.text2) # dead
        update_pointer(angle3,self.ptr3, self.ptr3_txt, self.text3) # Target

class CTRLS(object):
    def __init__(self, ):
        ctrl_frame = Frame(master)
        ctrl_frame.pack()

        self.quit_button = Button(frame, text="Up", fg="red", command=ctrl_frame.quit)
        self.quit_button.pack(side=LEFT)

class STATUS(object):
    def __init__(self, frame, mega):
        self.mega = mega
        self.canv = Canvas(frame, width=200, height=200)
        self.canv.pack(side = RIGHT)
        canvasheight = int(self.canv.config()['height'][-1])
        cavaswidth   = int(self.canv.config()['width'] [-1])
        self.canv.create_rectangle(2, 2, cavaswidth-2, canvasheight-2, fill="white")

        self.status_txt = self.canv.create_text( 4,4 , text='', anchor="nw")

    def update_stats(self):
        stats_str = "ONLINE: {} \nAZ: {} \nEL: {} \nGPS: \
{:.2f} {:.2f} {:.2f}\nMAG: {:.2f} {:.2f} {:.2f}\nACC: {:.2f} {:.2f} {:.2f}\n"
        x = [self.mega.online]+[self.mega.az]+\
        [self.mega.el]+self.mega.gps+self.mega.magno+self.mega.acc
        self.canv.itemconfig(self.status_txt, text=stats_str.format(*x) )


if __name__ == '__main__':
    try:
        mega1=serialcommu.mega()
    except Exception:
        mega1=serialcommu.dummy_mega()

    root = Tk()
    app = App(root,mega1)
    root.mainloop()

    mega1.stop()