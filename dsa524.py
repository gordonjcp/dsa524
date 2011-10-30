#!/usr/bin/python

import serial
import time

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
        self.ser.write(cmd + "\r")
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
        """
        if ch == 1:
            res = self.command("MEM?,AQU1")
        elif ch == 2:
            res = self.command("MEM?,AQU2")
        else: return"""
        res = self.command("MEM?,"+ch)
        return res
        
def getbinary(d,mem):
    out = d.getmem(mem)
    print out
    
    out = out.split(",")
    f = open("temp.bin", "w")
        
    while out[0] != " OK":
        d = "%d" % eval("0x"+out[0])
        print d
        f.write("%c" % int(d))
        
        
        out = out[1:]
    f.close()

def putbinary(d):
    print d.command("MODE,HEX")

    print d.command("MEM,AQU1")
    f = open("klick.bin","r")
    i=0
    while i<4096:
        k = f.read(1)
        j = "%02x," % ord(k)
        d.ser.write(j)
        #f.write(j)
        print i,
        i = i + 1
        time.sleep(0.005)   # doesn't respect xon/xoff!
    #f.write(" \r")
    f.close()
    print i
            

if __name__ == '__main__':
    d = DSA()

    d.connect()
    putbinary(d)
    #getbinary(d,"2")
    #ch1 = d.getchannel(1)    
    #print ch1.vrange
    
    #getbinary(d)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
