#!/usr/bin/python

import serial

PORT = "/dev/ttyUSB0"
SPEED = 38400


class DSA:
    """ Connect to a Thurlby DSA524 and send data """
    status=""

    ser = serial.Serial("/dev/ttyUSB0", 38400, xonxoff=1, rtscts=0)

    def readln(self):
        buf = ""
        while True:
            ch = self.ser.read(1)
            if ch == '\r':
                return buf
            buf = buf + ch
    
    def command(self, cmd):
        self.ser.write(cmd + "\r")
        return self.readln()
        
    def connect(self):
        print self.command("IDENT")
        
    def beep(self):
        self.command("BEEP")
if __name__ == '__main__':
    d = DSA()
    d.connect()
    
    d.beep()
    

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
