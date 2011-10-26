#!/usr/bin/python

import serial

PORT = "/dev/ttyUSB0"
SPEED = 38400


class Channel():
    vrange = "1V"
    coupling = "AC"
    ena = "ON"
    mode = "ZERO"
    offset = "0000"

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
        self.ser.write(cmd + " \r")
        return self.readln()
        
    def connect(self):
        print self.command("IDENT")
        
    def beep(self):
        self.command("BEEP")
        
    def getchannel(self, ch):
        if ch == 1:
            res = self.command("CH1?")
        elif ch == 2:
            res = self.command("CH2?")
        else: return
        
        res = res.split(",")
        ch = Channel()
        print res
        ch.ena=res[1]
        ch.vrange=res[2]
        ch.coupling=res[3]
        ch.mode=res[4]
        ch.offset = res[5]
        return ch

    def setchannel(self, ch, ena = None, vrange = None, coupling = None, mode = None, offset = None):
        if ena:
            self.command("CH1,"+ena)
        if vrange:
            print self.command("CH1,"+vrange)
        """ needs the rest """

    def getmem(self, ch):
        print self.command("MODE,HEX")
        if ch == 1:
            res = self.command("MEM?,AQU1")
        elif ch == 2:
            res = self.command("MEM?,AQU2")
        else: return
        return res
        
     
        
if __name__ == '__main__':
    d = DSA()

    ch1 = d.getchannel(1)    
    print ch1.vrange

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
