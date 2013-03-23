# script to do serial communication using python
import serial
import sys
import time
import os
from serial.tools import list_ports

def list_serial_ports():
    # Windows
    if os.name == 'nt':
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append('COM'+str(i + 1))
                s.close()
            except serial.SerialException:
                pass
        return available
    else:
        # Mac / Linux
        return [port[0] for port in list_ports.comports()]


class mega(object):
    def __init__(self):
        self.connect()

    def connect(self):
        # destroy reference of previous port used
        try:
            self.ser.close()
        except Exception:
            pass
        available_ports = list_serial_ports()
        print "available ports: " + str(available_ports)
        if len(available_ports)==1:
            self.port_name = available_ports[0]
            self.ser = serial.Serial(self.port_name, timeout=3,baudrate=115200)
            print self.ser.portstr
            print self.ser.readline().strip()
        elif len(available_ports)==0:
            print "no available ports"
        else:
            print "more than one available"
        sys.stdout.flush()
        

    def online(self):
        return self.ser.isOpen()

    def ping(self):
        try:
            self.ser.write("ping")
            retval = self.ser.readline()
            if "pong" in retval: return 1
            else:                return 0
        except:
            return 0

    def magno_read(self):
        # sent the charactor 'c' to the arduino. I have programmed the arduino to lesten to the serial link and if it catches a 'c' it will return the 3 axis on one line.
        self.ser.write('comp_xyz')

        # read the returned line in the format: 'x int y int z int'
        line = self.ser.readline().split() # .split() splits the line by the space and puts the 6 segments into a list

        # check it is required length
        if len( line )!=6: return 1 # error

        # assign varyble x y z respectively
        x,y,z = int(line[1]),int(line[3]),int(line[5])

        # flush the output pipe because there was some delay in printing to the screen on my windows 7
        sys.stdout.flush()
        return x,y,z # success

    def stop(self):
        self.ser.close()


if __name__ == '__main__':
    mega1 = mega() # on port 3

    while(1):
        if mega1.ping(): print "ping successful"
        else:
            print "ping failed"
            break
        sys.stdout.flush()

    mega1.stop()# close port