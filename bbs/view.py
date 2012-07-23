'''
Created on Jul 15, 2012

@author: teddydestodes
'''
import bbs
import bbs.widgets
import aalib
import Image
import streetview
from datetime import datetime
import time
import math
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

class Streetview(View):
    
    def __init__(self, client):
        View.__init__(self, client)
        self.lastdraw = 0
        self.framepointer = 0
        self.maxframes = 1000
        self.lib = streetview.Streetview()
        self.help['0-9'] = 'In Richtung 0-9 bewegen'
    
    def drawWindrose(self):
        width = 20
        height = 10
        yaw = float(self.lib.getYaw())
        #yaw = 0
        cmd = '\x1b[H'
        cmd += '\x1b(0'
        cmd += 'l' + 'q'*(width)+ 'k\n'
        cmd += ('x' + ' '*(width)+ 'x\n')*height
        cmd += 'm' + 'q'*(width)+ 'j'
        cmd += '\x1b(A'
        
        
        # draw directions
        pos = self.yawToPos(0-yaw, width, height) #north
        cmd += self.client.terminfo.tigets('cup', pos[1]+2,pos[0]+2)
        cmd += 'N'
        pos = self.yawToPos(90-yaw, width, height) #east
        cmd += self.client.terminfo.tigets('cup', pos[1]+2,pos[0]+2)
        cmd += 'E'
        pos = self.yawToPos(180-yaw, width, height) #east
        cmd += self.client.terminfo.tigets('cup', pos[1]+2,pos[0]+2)
        cmd += 'S'
        pos = self.yawToPos(270-yaw, width, height) #east
        cmd += self.client.terminfo.tigets('cup', pos[1]+2,pos[0]+2)
        cmd += 'W'
        c = 0
        for i in self.lib.getLinks():
            pos = self.yawToPos(float(i['yawDeg'])-yaw, width, height)
            cmd += self.client.terminfo.tigets('cup', pos[1]+2,pos[0]+2)
            cmd += "%d" % (c+1)
            c += 1
        return cmd
    
    def yawToPos(self, yaw, width, height):
        yaw = yaw -90
        b = math.pi/180
        x = math.cos(yaw * b)*(width/2)
        y = math.sin(yaw * b)*(height/2)
        return (int(x+width/2), int(y+height/2))
    
    def repaint(self):
        View.repaint(self)
        self.buffer = '\x1b[H'
        self.buffer += self.client.terminfo.tigets('civis')
        self.buffer += self.client.terminfo.tigets('setb', 0)
        self.buffer += self.client.terminfo.tigets('setf', 7)
        screen = aalib.AnsiScreen(width=self.size[0], height=self.size[1])
        image = self.lib.makeViewport().convert('L').resize(screen.virtual_size)
        screen.put_image((0, 0), image)
        self.buffer += screen.render()
        links = self.lib.getLinks()
        self.buffer += self.client.terminfo.tigets('cup', self.size[1]-(len(links)+1),0)
        maxlen = 0
        for i in links:
            if len(i['description']) > maxlen:
                maxlen = len(i['description'])
        maxlen += 9
        self.buffer += '\x1b(0'
        self.buffer += 'l' + 'q'*(maxlen)+ 'k\n'
        self.buffer += ('x' + ' '*(maxlen)+ 'x\n')*len(links)
        self.buffer += 'm' + 'q'*(maxlen)+ 'j' 
        self.buffer += '\x1b(A'
        
        c = 0;
        for i in links:
            self.buffer += self.client.terminfo.tigets('cup', self.size[1]-(len(links)-c),0)
            self.buffer += self.client.terminfo.tigets('cuf1')+"%d " % (c+1) + i['yawDeg'].ljust(7) +i['description'].center(maxlen-9)
            c += 1
        self.buffer += self.drawWindrose()
        self.buffer = self.buffer.decode('utf8')
    
    def _handleInput(self, command):
        if command in '0123456789':
            if int(command)-1 < len(self.lib.getLinks()):
                self.lib.setPanoId(self.lib.getLinks()[int(command)-1]['panoId'])
                self.paint()

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
        c = bbs.widgets.TextField(self.client, self)
        c.position = (31,20)
        self.addChild(c)
        
    def repaint(self):
        View.repaint(self)
        self.drawColors()
        self.drawMessage()
        self.client.lineMode = False
        
    def drawColors(self):
        mc = self.client.terminfo.tigeti('colors')
        ox = oy = 2
        cmd = ''
        c = 0
        for x in range(0,mc/8):
            for y in range(0,8):
                cmd = cmd +'\x1b[%d;%df' % (ox+x, oy+y) + self.client.terminfo.tigets('setb', c) + ' '
                c += 1
        self.buffer += cmd
        
    def drawMessage(self):
        msg = 'Hier ist nichts :( "strg+q" um Verbindung zu beenden'
        pad = pad = (self.size[0]-len(msg))/2;
        cmd = '\x1b[%d;%df' % (self.size[1]/2, pad) + msg 
        self.buffer = self.buffer + cmd
        
    def _handleInput(self, command):
        if command == self.client.terminfo.tigets('key_f12'):
            self.client.view = InputTest(self.client)
            self.client.view.paint()