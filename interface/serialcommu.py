# script to do serial communication using python
from serial.tools import list_ports
import threading
import serial
import time
import math
import sys
import os

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
        self.az = 0
        self.el = 0
        self.gps = [0,0,0]
        self.magno = [0,0,0]
        self.sensor_az = 0
        self.sensor_el = 0
        self.acc = [0,0,0]
        self.online = 0
        self.update()

    def update(self):

        t1 = time.time()
        self.ser.write('update')

        line = self.ser.readline().rstrip('\r\n').split(',') # .split() splits the line by the space and puts the 6 segments into a list
        #print "received line:" + str(line)
        #print time.time()-t1
        #sys.stdout.flush()

        if len( line )!=11:
            self.online = 0
        else:
            self.online = 1
            self.gps   = [ int(x) for x in line[0:3] ]
            self.acc   = [ int(x) for x in line[3:6] ]
            self.magno = [ int(x) for x in line[6:9] ]
            self.az    = int(line[9] )
            self.el    = int(line[10])
            self.sensor_az = math.degrees(math.atan2(self.magno[1], self.magno[0]))
            self.sensor_el = math.degrees(math.atan2(self.acc[1],   self.acc[0]  ))

        return 0 # success

    def connect(self):
        # destroy reference of previous port used
        try:
            self.ser.close()
        except Exception:
            pass
        available_ports = list_serial_ports()

        if len(available_ports)==1:
            self.port_name = available_ports[0]
            self.ser = serial.Serial(self.port_name, timeout=3,baudrate=9600)
        elif len(available_ports)==0:
            print "no available ports"
        else:
            print "more than one available ports: " + str(available_ports)
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
        # sent the charactor 'comp_xyz' to the arduino. I have programmed the arduino to lesten
        # to the serial link and if it catches the command it will return the 3 axis on one line.
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
        self.timer.cancel()
        self.ser.close()

    def move_azel(self, az, el):
        self.ser.write( "move_azel %i %i" %(az, el) )

    def stop_antenna(self):
        self.ser.write( "move_stop" )

    def rqst_azel(self):
        self.ser.write( "reqst_azel" )
        retval = self.ser.readline()
        return [int(x) for x in retval.split()]

    def read_acc(self):
        # sent the charactor 'comp_xyz' to the arduino. I have programmed the arduino to lesten
        # to the serial link and if it catches the command it will return the 3 axis on one line.
        self.ser.write('acc_xyz')

        # read the returned line in the format: 'x int y int z int'
        line = self.ser.readline().split() # .split() splits the line by the space and puts the 6 segments into a list

        # check it is required length
        if len( line )!=6: return 1 # error

        # assign varyble x y z respectively
        x,y,z = int(line[1]),int(line[3]),int(line[5])

        return x,y,z # success

    def read_gps(self):
        # sent the charactor 'comp_xyz' to the arduino. I have programmed the arduino to lesten
        # to the serial link and if it catches the command it will return the 3 axis on one line.
        self.ser.write('rqst_gps')

        # read the returned line in the format: 'x int y int z int'
        line = self.ser.readline().split() # splits the line by the space and puts the 6 segments into a list

        # check it is required length
        if len( line )!=6: return 1 # error

        # assign varyble x y z respectively
        x,y,z = int(line[1]),int(line[3]),int(line[5])

        return x,y,z # success


if __name__ == '__main__':
    mega1 = mega() # on port 3
    i = 0

    while(1):
        #if mega1.ping(): print "ping successful"
        #else:
        #    print "ping failed"
        #    break
        print str(i) + ":" + str(mega1.magno)
        i += 1
        sys.stdout.flush()
        time.sleep(3)

    mega1.stop()# close port