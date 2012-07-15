'''
Created on Jul 15, 2012

@author: teddydestodes
'''
import bbs

class Window(bbs.Drawable):
    
    def __init__(self, client, parent = None, centered = True):
        '''
        Constructor
        '''
        bbs.Drawable.__init__(self, client, parent)
        self.centered = centered
    
    def repaint(self):
        if self.centered:
            hpad = (self.parent.size[0]-self.size[0])/2
            vpad = (self.parent.size[1]-self.size[1])/2
        cmd =       '\x1b[%d;%dH' % (vpad, hpad)
        cmd = cmd + '\x1b(0'
        cmd = cmd + 'l' + 'q'*(self.size[0]-2)+ 'k'
        for i in range(self.size[1]-1):
            cmd = cmd + '\x1b[%d;%dH' % (vpad+i+1, hpad)
            cmd = cmd + 'x' + ' '*(self.size[0]-2)+'x'
        cmd = cmd + '\x1b[%d;%dH' % (vpad+self.size[1], hpad)
        cmd = cmd + 'm' + 'q'*(self.size[0]-2)+ 'j'
        cmd = cmd + '\x1b(A'
        tpad = hpad + (self.size[0]-len(self.title))/2
        cmd = cmd + '\x1b[%d;%dH%s' % (vpad, tpad, self.title)
        self.buffer = self.buffer + cmd

class Help(bbs.Borg,Window):

    def __init__(self, client, parent = None):
        Window.__init__(self, client, parent, True)
        self.size = (30,24)
        self.title = 'Hilfe'
        
    def repaint(self):
        Window.repaint(self)
        length = 0
        for help in self.parent.help:
            if len(help) > length:
                length = len(help)
        if self.centered:
            hpad = (self.parent.size[0]-self.size[0])/2
            vpad = (self.parent.size[1]-self.size[1])/2
        
        cmd =       '\x1b[%d;%dH' % (vpad+2, hpad+2)
        line = 1
        for help in self.parent.help:
            cmd = cmd + '\x1b[%d;%dH' % (vpad+2+line, hpad+2) + help.ljust(length+2,' ')+self.parent.help[help]
            line = line + 1
        self.buffer = self.buffer + cmd