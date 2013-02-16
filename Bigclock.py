'''
Created on 9 May 2012

@author: ajtag
'''

import socket
import time
#import sys

class BigClock():
    def __init__(self, host = ('192.168.0.99', 10001)):
        self.host = host
        self.connected = False 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        connectattempts = 5
        while not self.connected and connectattempts > 0:
            try:
                self.sock.connect(self.host)
                self.connected = True
                print 'connected'
            except:
                connectattempts -= 1 
                print 'failed to connect, waiting 1s before trying again'
                time.sleep(1)
        if not self.connected:
            raise 'NetworkError'
    
    def disconnect(self):
        self.connected = False
        self.sock.close()
        
    
    def display_wrapped(self, serialtask = 0, text =  '', center = 1, xx = 0, delay = 1):
        pass
    #command = 0#1#3#00#hello world#1,0,2#cc<
    
    def send(self, command):
        while not self.connected:
            self.connect()
        #print str(command)
        self.sock.sendall(str(command))
        
        
    def sendraw(self, command):
        self.sock.sendall(command)
        
        #msg = '>'+  command  +'#' 
        #msg = msg + self.checksum(msg) + '<'
        #print msg


    
class Command():
    inflags = '0'
    sendresponse = '0'
    cmdnum = '4'
    serialtask = '0' 
    inbuf = ''
    arglist = ['0'] 
    checksum_str = ''
    def __str__(self):
        return '>%s%s<'%(self.commandstring(), self.checksum(self.commandstring(), True))
        #return '>inflags#sendresponse#cmdnum#serialtask#inbuf#args,args,...#checksum<'
    
    def commandstring(self):
        return '#'.join( (self.inflags, self.sendresponse, self.cmdnum, self.serialtask, self.inbuf,','.join(self.arglist), self.checksum_str))

    def __init__(self, commandnum, inbuf, display=0, *args):
        '>inflags#sendresponse#cmdnum#serialtask#inbuf#args,args,...#checksum<'
        self.cmdnum = str(commandnum)
        self.inbuf = str(inbuf)
        self.serialtask = str(display)
        if len(args) > 0:
            self.arglist = [str(arg) for arg in args]
    def checksum(self, msg,  Ignore = False):
        if Ignore:
            checksum = 'cc'
        else:
            checksum = 0
            if not msg.startswith('>'):
                msg = '>' + msg 
            for char in msg:
                checksum = checksum ^ ord(char)
            checksum = str(hex(checksum)).upper()[-2:]
        return checksum 

class clockui():
    def __init__(self):
        self.clock = BigClock()
        pass
    
    def test(self):
        try: 
            self.clock.send(Command(2,'moo'))
            #self.clock.send('>0#1#2#00#Fuck Yeah#cc<')
            
            (command, arguments) = self.get_input('Enter a command:')
            while command != 'quit': 
                if command == 'wifi':
                    arguments = 'wootastringthisis'
                    self.clock.send(Command(0, arguments))
                else:
                    self.clock.send(Command(command, arguments))
                
                (command, arguments) = self.get_input('Enter a command:')
            i = 0
            for i in xrange(255):
    #            self.send('0#1#2#'+str(hex(i)).replace('0x', '').zfill(2)+'#'+str(time.time())[-5:]+'#2,0')#scroll text up
                self.clock.send(Command(i, 'knob'))
                #self.clock.send('0#0#'+str(hex(i))[-2:].replace('x','')+'#80#knob#0')
    #        self.send('PR#1#00#80,07,08#25,05,2012,2')
    #        self.send('0#1#0#80#ajjoijoojsd')
            #while True:
    #        self.send('0#1#3#80#Alert#1,0,1')# display wrapped text and clear 
    #        self.send('0#1#4#80##ff')# clear screen
    #        self.send('0#1#2#00#'+str(time.time())[-5:].replace('.','^.')+'#2,0')#scroll text up               
    #        self.send('0#1#5#80##1')#clearscreen
    #        self.send('0#1#6#80##0')#stop animation
    #        self.send('0#1#7#00##0#')#stop animation?
    #        self.send('0#1#8#00#hello world#0')#displaytext without clearing
    #        self.send('0#1#a#00#hi there#0,0,0')#display by /12 screens
    ##arg0   0 = ? 1 = ? (might crash it)
    ##arg1     0x10-0xbf = clear top half afterwards? wrapping height?
    ##arg2     1 = do top half, then bottom half
    #        self.send('0#1#F0####')#get serial task count
    #        self.send('0#1#F3###')#get time
    #        self.send('0#1#F4###')#get date
    #        self.send('0#1#F5###')#get version
    #        self.send('0#1#1#80#blah#2')#reboot
            #self.send('')
            #self.send('')
            
            
            #self.clock.send('0#1#2#00#Fuck Yeah#2,0#cc<')
        except KeyboardInterrupt:
            self.clock.disconnect()
            

    def get_input(self, prompt = ''):
        instr = raw_input(prompt)
        arg = instr.split(' ')
        command = arg[0]
        arglist= ' '.join(arg[1:])
        return (command, arglist)




if __name__ == '__main__':
    cui = clockui()
    while True:
        cui.test()
        time.sleep(5)

