'''
Created on Jul 15, 2012

@author: teddydestodes
'''
import bbs

class Input(bbs.Drawable):

    def __init__(self, client, parent = None):
        '''
        Constructor
        '''
        bbs.Drawable.__init__(self, client, parent)
        self.position = (0,0)
        
    def _handleInput(self, command):
        if command == '':
            self.parent.cycleFocus(self)
            return True
        else :
            return False

            
    def repaint(self):
        cmd =       '\x1b[%d;%dH' % (self.position[0], self.position[1])
        cmd = cmd + '\x1b[40m'+ ' '*self.size[0]
        cmd = cmd*self.size[1]
        self.buffer = self.buffer + cmd
        

class TextField(Input):
    
    def __init__(self, client, parent = None):
        Input.__init__(self, client, parent)
        self.size = (20,1)
        self.insertbuffer = ''
        self.insertbufferpos = 0
        
    def repaint(self):
        Input.repaint(self)
        cmd = ''
        cmd = cmd + '\x1b[%d;%dH' % (self.position[0], self.position[1])
        offset = 0
        if len(self.insertbuffer) > self.size[0]:
            offset = self.insertbufferpos-self.size[0]/2
            if offset+self.size[0] > len(self.insertbuffer):
                offset = len(self.insertbuffer) - self.size[0]
            elif offset < 0:
                offset = 0
            cmd = cmd + self.insertbuffer[offset:offset+self.size[0]]
        else:
            cmd = cmd + self.insertbuffer
        if self.hasFocus:
            cmd = cmd + '\x1b[%d;%dH\x1b[33m' % (self.position[0], self.position[1]+self.insertbufferpos-offset)
            cmd = cmd + '\x1b[?25h'
        self.buffer = self.buffer + cmd
        
    def _handleInput(self, command):
        if Input._handleInput(self, command):
            return True
        else:
            command = command.strip()
            if command in ('\x1b[A', '\x1b[B', '\x1b[C', '\x1b[D'):
                if command[2] == 'A':
                    self.insertbufferpos = len(self.insertbuffer)
                elif command[2] == 'B':
                    self.insertbufferpos = 0
                elif command[2] == 'C':
                    if self.insertbufferpos < len(self.insertbuffer) :self.insertbufferpos += 1
                elif command[2] == 'D':
                    if self.insertbufferpos > 0 :self.insertbufferpos -= 1
            elif len(command) > 0 and command[0] != '\x1b' and command[0] != '\0' :
                self.insertbuffer = self.insertbuffer[:self.insertbufferpos] + command + self.insertbuffer[self.insertbufferpos:]
                self.insertbufferpos = self.insertbufferpos + len(command)
            self.paint()