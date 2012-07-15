'''
Created on Jul 15, 2012

@author: teddydestodes
'''
import bbs
import bbs.widgets


class View(bbs.Drawable):

    buffer = ''
    size = (80,24)
    
    def __init__(self, client):
        bbs.Drawable.__init__(self, client, None)
        self.helpVisible = False
    
    def drawBorder(self):
        cmd =       '\x1b[H'
        cmd = cmd + '\x1b(0'
        cmd = cmd + '\x1b[?25l'
        cmd = cmd + 'l' + 'q'*(self.size[0]-2)+ 'k'
        cmd = cmd + '\x1b[Bx'*(self.size[1]-2)
        cmd = cmd + '\x1b[H' + '\x1b[B\x1b[Dx'*(self.size[1]-2)
        cmd = cmd + '\x1b[B\x1b[Dm' + 'q'*(self.size[0]-2)+ 'j'
        cmd = cmd + '\x1b(A'
        
        self.buffer = self.buffer + cmd

    def repaint(self):
        self.clearScreen()
        self.drawBorder()
    
    def showHelp(self):
        if not self.helpVisible:
            self.helpVisible = True
            self.addChild(bbs.window.Help(self.client, self))
        
class Title(View):
    
    
    def __init__(self, client):
        View.__init__(self, client)
        self.clientcount = 0
        self.connectioncount = 0
        
    def setClientCount(self, clients):
        self.clientcount = clients
        
    def setConnectionCount(self, count):
        self.connectioncount = count
    
    def _handleInput(self, command):
        self.client.view = EmptyPage(self.client)
        self.client.view.paint()
    
    def repaint(self):
        View.repaint(self)
        self.drawHeader()
    
    def drawHeader(self):
        pad = (self.size[0]-18)/2;
        #white = '\x1b[47m'
        cmd =       '\x1b[%d;%df' % (2, pad) + '\x1b[47m                    '
        cmd = cmd + '\x1b[%d;%df' % (3, pad) + '\x1b[47m    \x1b[40m            \x1b[47m    '
        cmd = cmd + '\x1b[%d;%df' % (4, pad) + '\x1b[47m  \x1b[40m  \x1b[47m  \x1b[40m        \x1b[47m  \x1b[40m  \x1b[47m  '
        cmd = cmd + '\x1b[%d;%df' % (5, pad) + '\x1b[47m  \x1b[40m    \x1b[47m  \x1b[40m    \x1b[47m  \x1b[40m    \x1b[47m  '
        cmd = cmd + '\x1b[%d;%df' % (6, pad) + '\x1b[47m  \x1b[40m                \x1b[47m  '
        cmd = cmd + '\x1b[%d;%df' % (7, pad) + '\x1b[47m  \x1b[40m                \x1b[47m  '
        cmd = cmd + '\x1b[%d;%df' % (8, pad) + '\x1b[47m  \x1b[40m    \x1b[47m  \x1b[40m    \x1b[47m  \x1b[40m    \x1b[47m  '
        cmd = cmd + '\x1b[%d;%df' % (9, pad) + '\x1b[47m  \x1b[40m  \x1b[47m  \x1b[40m        \x1b[47m  \x1b[40m  \x1b[47m  '
        cmd = cmd + '\x1b[%d;%df' % (10, pad) + '\x1b[47m    \x1b[40m            \x1b[47m    '
        cmd = cmd + '\x1b[%d;%df' % (11, pad) + '\x1b[47m                    '
        
        pad = pad = (self.size[0]-56)/2;
        cmd = cmd + '\x1b[%d;%df' % (13, pad) + "\x1b[37;44m _        _      _               _            _  _    _ "
        cmd = cmd + '\x1b[%d;%df' % (14, pad) + "| |  ___ (_)  __| |  ___  _ __  | |__    ___ (_)| |  / \\"
        cmd = cmd + '\x1b[%d;%df' % (15, pad) + "| | / _ \| | / _` | / _ \| '__| | '_ \  / _ \| || | /  /"
        cmd = cmd + '\x1b[%d;%df' % (16, pad) + "| ||  __/| || (_| ||  __/| |    | | | ||  __/| || |/\_/ "
        cmd = cmd + '\x1b[%d;%df' % (17, pad) + "|_| \___||_| \__,_| \___||_|    |_| |_| \___||_||_|\/   "
        
        msg = 'Tja BBS und so... Momentan sind %d Verbindungen aktiv' % (self.clientcount,)
        pad = pad = (self.size[0]-len(msg))/2;
        cmd = cmd + '\x1b[%d;%df' % (19, pad) + msg
        msg = 'Verbindungszaehler sagt: %d' % (self.connectioncount,)
        pad = pad = (self.size[0]-len(msg))/2;
        cmd = cmd + '\x1b[%d;%df' % (20, pad) + msg
        msg = 'Enter fuer weiter...'
        pad = pad = (self.size[0]-len(msg))/2;
        cmd = cmd + '\x1b[%d;%df' % (21, pad) + msg
        
        self.buffer = self.buffer + cmd

chatdb = []

class InputTest(View):
    def __init__(self, client):
        View.__init__(self, client)
    
    def repaint(self):
        View.repaint(self)
    
    def update(self):
        pass
    
    def _handleInput(self, Input):
        pass

class EmptyPage(View):
    
    def __init__(self, client):
        View.__init__(self, client)
        p = bbs.widgets.TextField(self.client, self)
        p.position = (20,20)
        p.hasFocus = True
        self.addChild(p)
        c = bbs.widgets.TextField(self.client, self)
        c.position = (30,20)
        self.addChild(c)
        
    def repaint(self):
        View.repaint(self)
        self.drawMessage()
        self.client.lineMode = False
        
    def drawMessage(self):
        msg = 'Hier ist nichts :( "quit" um Verbindung zu beenden'
        pad = pad = (self.size[0]-len(msg))/2;
        cmd = '\x1b[%d;%df' % (self.size[1]/2, pad) + msg 
        self.buffer = self.buffer + cmd
        
    def _handleInput(self, command):
        if command == '\x1b[24~': #F12
            self.client.view = InputTest(self.client)
            self.client.view.paint()