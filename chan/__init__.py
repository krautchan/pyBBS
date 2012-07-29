# -*- coding: utf-8 -*-
from bbs import Screen
import sql
from termlib.widgets import Label, TextArea, TextField, ScrollPane, Panel, ImagePane, Button
from termlib.canvas import Canvas
from termlib import Image, ImgAttr
from chan.stuff import makeNyanFrames
import time
class Nyan(Screen):
    def __init__(self, client):
        Screen.__init__(self, client, 'Nyan')
        self.frames = makeNyanFrames()
        self.image = ImagePane(self.frames[0])
        self.addChild(self.image)
        self.fc = 0
    def update(self):
        self.image.setImage(self.frames[self.fc])
        self.fc += 1
        
        if self.fc >= len(self.frames):
            self.fc = 0
        self.image.repaint()

class Welcome(Screen):
    def __init__(self, client):
        Screen.__init__(self, client, 'Welcome')
        logo = Image()
        white = ImgAttr()
        white.background = Canvas.COLOR_WHITE
        white.foreground = Canvas.COLOR_WHITE
        black = ImgAttr()
        black.background = Canvas.COLOR_BLACK
        black.foreground = Canvas.COLOR_BLACK
        logo.put(white, (0,0), '                        ')
        logo.put(white, (0,1), '    ')
        logo.put(white, (20,1), '    ')
        logo.put(white, (18,2), '  ')
        logo.put(white, (4,2), '  ')
        logo.put(white, (16,3), '  ')
        logo.put(white, (6,3), '  ')
        logo.put(white, (14,4), '  ')
        logo.put(white, (8,4), '  ')
        logo.put(white, (14,7), '  ')
        logo.put(white, (8,7), '  ')
        logo.put(white, (18,9), '  ')
        logo.put(white, (4,9), '  ')
        logo.put(white, (16,8), '  ')
        logo.put(white, (6,8), '  ')
        logo.put(white, (0,10), '    ')
        logo.put(white, (20,10), '    ')
        logo.put(white, (22,1), '  ')
        logo.put(white, (22,2), '  ')
        logo.put(white, (22,3), '  ')
        logo.put(white, (22,4), '  ')
        logo.put(white, (22,5), '  ')
        logo.put(white, (22,6), '  ')
        logo.put(white, (22,7), '  ')
        logo.put(white, (22,8), '  ')
        logo.put(white, (22,9), '  ')
        logo.put(white, (0,1), '  ')
        logo.put(white, (0,2), '  ')
        logo.put(white, (0,3), '  ')
        logo.put(white, (0,4), '  ')
        logo.put(white, (0,5), '  ')
        logo.put(white, (0,6), '  ')
        logo.put(white, (0,7), '  ')
        logo.put(white, (0,8), '  ')
        logo.put(white, (0,9), '  ')
        logo.put(white, (0,11), '                        ')
        logo.put(black, (4,1),    '                ')
        logo.put(black, (6,2),      '            ')
        logo.put(black, (8,3),        '        ')
        logo.put(black, (10,4),          '    ')
        logo.put(black, (2,5), '                    ')
        logo.put(black, (2,6), '                    ')
        logo.put(black, (10,7),          '    ')
        logo.put(black, (8,8),        '        ')
        logo.put(black, (6,9),      '            ')
        logo.put(black, (4,10),    '                ')
        
        logo.put(black, (16,7),                '      ')
        logo.put(black, (18,8),                  '    ')
        logo.put(black, (20,9),                    '  ')
        logo.put(black, (2,7), '      ')
        logo.put(black, (2,8), '    ')
        logo.put(black, (2,9), '  ')
        logo.put(black, (20,2),                     '  ')
        logo.put(black, (18,3),                   '    ')
        logo.put(black, (16,4),                 '      ')
        logo.put(black, (2,2), '  ')
        logo.put(black, (2,3), '    ')
        logo.put(black, (2,4), '      ')
        
        self.logoimage = ImagePane(logo)
        self.position = [2,2]
        self.addChild(self.logoimage)
        
        self.title = Label()
        self.title.label = """   _            _____ _____ _____ 
 _| |___ ___   | __  | __  |   __|
| . | -_|  _|  | __ -| __ -|__   |
|___|___|_|    |_____|_____|_____|"""
        self.title.pack()
        self.title.position = [3,14]
        self.title.setBackground(Canvas.COLOR_BLUE)
        self.addChild(self.title)
        
        self.message = Label(u'Enter für weiter... :3')
        self.message.pack()
        self.message.position = [3,20]
        self.addChild(self.message)
        self.message.setBackground(Canvas.COLOR_BLUE)
        self.setBackground(Canvas.COLOR_BLUE)
        
    def paint(self, canvas):
        self.logoimage.position[0] = (self.size[0]-self.logoimage.size[0])/2
        self.title.position[0] = (self.size[0]-self.title.size[0])/2
        self.message.position[0] = (self.size[0]-self.message.size[0])/2
        Screen.paint(self, canvas)
        
    def onInput(self, command):
        Screen.onInput(self, command)
        if len(command) == 0:
            return
        if command == self.canvas.terminfo.tigets('kf2'):
            self.client.view = Nyan(self.client)
            return
        if command[0] == '\r' or command[0] == '\n':
            self.client.view = Board(self.client,'beh')

class ThreadPane(Panel):
    
    def __init__(self, thread):
        Panel.__init__(self)
        self.thread = thread
        self.text = None
        self.username = None
        self.title = None
        self.postnum = None
        self.posts = []
        self.setBackground(Canvas.COLOR_BLUE)
        
    def update(self):
        dirty = False
        if not self.text:
            self.text = Label(self.thread.text)
            self.text.wrap = True
            self.text.position = [0,1]
            self.text.setBackground(Canvas.COLOR_BLUE)
            self.addChild(self.text)
            dirty = True
        
        if self.size[0] != self.parent.size[0]-3:
            self.size[0] = self.parent.size[0]-3
            dirty = True
        
        if self.text.maxWidth != self.size[0]:
            self.text.maxWidth = self.size[0]
            self.text.pack()
            self.text.size[0] = self.text.maxWidth
            dirty = True
        
        if not self.postnum:
            self.postnum = Button('#%d'%self.thread.postid)
            self.postnum.size = [8,1]
            self.postnum.position = [0, 0]
            self.postnum.setBackground(Canvas.COLOR_BLUE)
            self.addChild(self.postnum)

        if not self.username:
            self.username = Label(self.thread.username)
            self.username.maxWidth = 20
            self.username.pack()
            self.username.position = [self.postnum.size[0]+1,0]
            self.username.setBackground(Canvas.COLOR_BLUE)
            self.addChild(self.username)
        
        if not self.title:
            self.title = Label(self.thread.title)
            self.title.maxWidth = 20
            self.title.pack()
            self.title.position = [self.postnum.size[0]+self.username.size[0]+2, 0]
            self.title.setBackground(Canvas.COLOR_BLUE)
            
            self.addChild(self.title)
        
        self.pack()
        self.size[1] = self.contentSize.max[1]
        return dirty

class Thread(Screen):
    
    def __init__(self, client, post):
        Screen.__init__(self, client, 'bbs')
        self.size = [client.columns, client.rows]
        self.Thread = self.loadThread(post)
class Board(Screen):
    
    def __init__(self, client, board):
        Screen.__init__(self, client, 'bbs')
        self.size = [client.columns, client.rows]
        self.board = self.loadBoard(board)
        self.header = Label()
        self.header.label = u"""     ___       __   _     
    / / |__   / /__| |__  
   / /| '_ \ / / _ \ '_ \ 
  / / | |_) / /  __/ | | |
 /_/  |_.__/_/ \___|_| |_|"""
        self.header.pack()
        self.header.position = [0,0]
        self.header.setBackground(Canvas.COLOR_BLUE)
        self.addChild(self.header)
        self.threads = {}
        self.dirty = False
        self.lastpoll = 0
        self.newthreadpane = Panel()
        self.newthreadpane.setBackground(Canvas.COLOR_BLUE)
        self.newthreadpane.position = [6,6]
        self.addChild(self.newthreadpane)
        t = Label('Name:')
        t.pack()
        t.position = [0,0]
        t.setBackground(Canvas.COLOR_BLUE)
        self.newthreadpane.addChild(t)
        
        self.name = TextField()
        self.name.size = [15,1]
        self.name.position = [5,0]
        self.newthreadpane.addChild(self.name)
        
        t = Label('Betreff:')
        t.pack()
        t.position = [21,0]
        t.setBackground(Canvas.COLOR_BLUE)
        self.newthreadpane.addChild(t)
        self.topic = TextField()
        self.topic.size = [15,1]
        self.topic.position = [29,0]
        self.newthreadpane.addChild(self.topic)
        
        t = Label('Text:')
        t.pack()
        t.position = [0,3]
        t.setBackground(Canvas.COLOR_BLUE)
        self.newthreadpane.addChild(t)
        self.text = TextArea()
        self.text.size = [40,10]
        self.text.position = [5,3]
        self.newthreadpane.addChild(self.text)
        
        self.sendbutton = Button('Senden')
        self.sendbutton.size = [10,1]
        self.sendbutton.position = [5,14]
        self.sendbutton.onPress = self.newThread
        self.sendbutton.setBackground(Canvas.COLOR_BLUE)
        self.newthreadpane.addChild(self.sendbutton)
        self.scrollpane = ScrollPane()
        self.scrollpane.size = [self.size[0],0]
        self.scrollpane.position = [0,18]
        self.scrollpane.setBackground(Canvas.COLOR_BLUE)
        self.addChild(self.scrollpane)
        self.setBackground(Canvas.COLOR_BLUE)
        self.repaint()
    
    def loadBoard(self, board):
        return self.client.session.query(sql.Board).filter(sql.Board.name==board).first()
    
    def update(self):
        if time.time()-self.lastpoll > 1:
            self.lastpoll = time.time()
        else:
            return
        self.updateBoard()
        x = 1
        self.scrollpane.size[0] = self.size[0]
        if len(self.threads) > 0:
            for threadid in reversed(sorted(self.threads.keys())):
                if self.threads[threadid].update():
                    self.dirty = True
                self.threads[threadid].position = (2,x)
                x += self.threads[threadid].size[1]+1
            
            if self.dirty:
                print self.dirty
                self.scrollpane.pack()
                self.scrollpane.repaint()
                self.dirty = False

    def updateBoard(self):
        threads = self.board.getThreads(self.client.session)
        for thread in threads:
            if thread.postid not in self.threads.keys():
                tp = ThreadPane(thread)
                self.scrollpane.addChild(tp)
                self.threads[thread.postid] = tp
                self.dirty = True
    
    def newThread(self):
        self.board.addThread(self.client.session, self.name.getValue(), self.topic.getValue(), self.text.getValue())
    
    def paint(self, canvas):
        self.header.position[0] = (self.size[0]-self.header.size[0])/2
        self.scrollpane.size[0] = self.size[0]
        
        if not self.newthreadpane.visible:
            self.scrollpane.size[1] = self.size[1]-6
            self.scrollpane.position[1] = 6
        else:
            self.scrollpane.size[1] = self.size[1]-22
            self.scrollpane.position[1] = 22
        
        Screen.paint(self, canvas)
        canvas.setBackground(self.background)
        canvas.fillBackground()
        
    def onInput(self, command):
        if command == self.canvas.terminfo.tigets('kf1'):
            self.newthreadpane.visible = not self.newthreadpane.visible
            if not self.newthreadpane.visible:
                self.newthreadpane.removeFocus()
            self.repaint()
        if command == self.canvas.terminfo.tigets('kf2'):
            self.name.giveFocus()
        Screen.onInput(self, command)