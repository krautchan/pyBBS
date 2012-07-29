from termlib.canvas import Canvas, BBox, sub, add, div, mul
from termlib import Drawable
import math
from textwrap import wrap
class Widget(Drawable):
    pass
class Input(Widget):
    pass
            
class ImagePane(Widget):
    def __init__(self, image):
        Widget.__init__(self)
        self.image = image
        self.focusable = False
        self.pack()

    def setImage(self, image):
        self.image = image
        self.pack()
    def pack(self):
        self.size = self.image.getBBox().max
        
    def paint(self, canvas):
        Widget.paint(self, canvas)
        canvas.setCursorVisible(False)
        self.image.draw(canvas)

class Label(Widget):
    
    def __init__(self, label=''):
        Widget.__init__(self)
        self.label = label
        self.focusable = False
        self.maxWidth = 0
        self.maxHeight = 0
        self.warp = False
    
    def pack(self):
        lc = 0
        ls = 0
        for line in self.label.split('\n'):
            if self.warp:
                for wl in wrap(line,self.maxWidth):
                    if len(wl) > ls:
                        ls = len(wl)
                    lc +=1
            else:
                if len(line) > ls:
                    ls = len(line)
                lc += 1
        if lc > self.maxHeight and self.maxHeight > 0:
            lc = self.maxHeight
        if ls > self.maxWidth and self.maxWidth > 0:
            ls = self.maxWidth
        self.size = [ls,lc]
    
    def paint(self, canvas):
        Widget.paint(self, canvas)
        canvas.setForeground(Canvas.COLOR_WHITE)
        lc = 0
        for line in self.label.split('\n'):
            if self.warp:
                
                for wl in wrap(line,self.maxWidth):
                    self.putString(canvas, lc, wl)
                    lc +=1
            else:
                if self.maxWidth > 0:
                    self.putString(canvas, lc, line[0:self.maxWidth])
                else:
                    self.putString(canvas, lc, line)
                lc += 1

    def putString(self, canvas, line, string):
            canvas.printString((0,line),string.ljust(self.size[0]))

class Panel(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.focusable = False
        self.contentSize = BBox([0,0],[0,0])

    def addChild(self, child):
        child.onRepaint = self.onRepaint
        Widget.addChild(self, child)
        self.pack()
    
    def pack(self):
        bbox = BBox([0,0],[0,0])
        for child in self.children:
            bbox.addPoint(add(child.position, child.size))
        self.contentSize = bbox

    def paint(self, canvas):
        self.size = self.contentSize.max
        Widget.paint(self, canvas)
        #canvas.fillBackground()

class ScrollPane(Widget):
    
    def __init__(self, label=''):
        Widget.__init__(self)
        self.label = label
        self.offset = [0,0]
        self.contentSize = BBox([0,0],[0,0])
        
    def addChild(self, child):
        child.onRepaint = self.onRepaint
        Widget.addChild(self, child)
        self.pack()
        
    def pack(self):
        bbox = BBox([0,0],[0,0])
        for child in self.children:
            bbox.addPoint(add(child.position, child.size))
        self.contentSize = bbox
    
    def onCommand(self, command):
        offset = mul(self.offset, (-1,-1))
        print command
        if command == self.canvas.terminfo.tigets('kcuu1'):#up
            print 'u'
            if offset[1] > self.contentSize.min[1]:
                self.offset[1] += 1
        elif command == self.canvas.terminfo.tigets('kcud1'):#down
            print 'd'
            if offset[1]+self.size[1]-1 < self.contentSize.max[1]:
                self.offset[1] -= 1
        elif command == self.canvas.terminfo.tigets('kcub1'):#left
            print 'l'
            if offset[0] > self.contentSize.min[0]:
                self.offset[0] += 1
        elif command == self.canvas.terminfo.tigets('kcuf1'):#right
            print 'r'
            if offset[0]+self.size[0]-1 < self.contentSize.max[0]:
                self.offset[0] -= 1
        self.repaint()
    
    def paint(self, canvas):
        canvas.offset = self.offset
        Widget.paint(self, canvas)
        canvas.size = sub(self.size, (1,1))
        canvas.fillBackground()
        if self.hasFocus:
            canvas.setForeground(Canvas.COLOR_YELLOW)
        else:
            canvas.setForeground(Canvas.COLOR_WHITE)
        self.paintBars(canvas)
        
    def paintBars(self,canvas):
        if self.size[0]-1 > 0 and self.size[1] -1 > 0:
            canvas.drawLine((self.size[0]-1,0), height=self.size[1]-1, char='a')
            canvas.drawLine((0,self.size[1]-1), width=self.size[0]-1, char='a')
            offset = mul(self.offset, (-1,-1))
            hs = (self.contentSize.min[0]+offset[0])/float(self.size[0]-1)
            he = ((offset[0]+(self.size[0]-1))-self.contentSize.max[0])/float(self.size[0]-1)
            vs = (self.contentSize.min[1]+offset[1])/float(self.size[1]-1)
            ve = ((offset[1]+(self.size[1]-1))-self.contentSize.max[1])/float(self.size[1]-1)
            if ve <= 0:
                canvas.drawLine((self.size[0]-1,int(vs)), height=int(math.ceil(ve-vs+(self.size[1]-1))), char='{')
            if he <= 0:
                canvas.drawLine((int(hs),self.size[1]-1), width=int(math.ceil(he-hs+(self.size[0]-1))), char='{')

class TextField(Input):
    
    def __init__(self):
        Input.__init__(self)
        self.insertbuffer = ''
        self.insertbufferpos = 0
    
    def getValue(self):
        return self.insertbuffer
    
    def paint(self, canvas):
        Input.paint(self, canvas)
        canvas.size=self.size
        canvas.fillBackground()
        if self.hasFocus:
            canvas.setForeground(Canvas.COLOR_YELLOW)
        else:
            canvas.setForeground(Canvas.COLOR_WHITE)
        
        offset = 0
        if len(self.insertbuffer) > self.size[0] - 1:
            offset = self.insertbufferpos - self.size[0] / 2
            if offset + self.size[0] / 2 > len(self.insertbuffer):
                offset = len(self.insertbuffer) - self.size[0] / 2
            elif offset < 0:
                offset = 0
        canvas.printString((0,0),self.insertbuffer[offset:offset + self.size[0]].ljust(self.size[0]))
        
        if self.hasFocus:
            canvas.moveCursor((self.insertbufferpos - offset,0))
            canvas.setCursorVisible(True)
        else:
            canvas.setCursorVisible(False)


    def onCommand(self, command):
        if command in ('\x1b[A', '\x1b[B', '\x1b[C', '\x1b[D'):
            if command[2] == 'A':
                self.insertbufferpos = len(self.insertbuffer)
            elif command[2] == 'B':
                self.insertbufferpos = 0
            elif command[2] == 'C':
                if self.insertbufferpos < len(self.insertbuffer) :self.insertbufferpos += 1
            elif command[2] == 'D':
                if self.insertbufferpos > 0 :self.insertbufferpos -= 1
        elif command == '\x7f' and self.insertbufferpos > 0: #backspace
            self.insertbuffer = self.insertbuffer[:self.insertbufferpos-1] + self.insertbuffer[self.insertbufferpos:]
            self.insertbufferpos -= 1
        elif command == '\x1b[3~' and self.insertbufferpos < len(self.insertbuffer): #del
            self.insertbuffer = self.insertbuffer[:self.insertbufferpos] + self.insertbuffer[self.insertbufferpos+1:]
        elif len(command) > 0 and command[0] != '\x1b' and command[0] != '\0' and command != '\x7f':
            command = command.decode('utf8')
            command = command.replace('\r', '')
            command = command.replace('\n', '')
            self.insertbuffer = self.insertbuffer[:self.insertbufferpos] + command + self.insertbuffer[self.insertbufferpos:]
            self.insertbufferpos = self.insertbufferpos + len(command)
        self.repaint()
            
class TextArea(Input):
    def __init__(self):
        Input.__init__(self)
        self.insertbuffer = ['']
        self.insertbufferpos = [0,0]
    
    def getValue(self):
        return '\n'.join(self.insertbuffer)
    
    def paint(self, canvas):
        Input.paint(self, canvas)
        canvas.size=self.size
        canvas.fillBackground()
        if self.hasFocus:
            canvas.setForeground(Canvas.COLOR_YELLOW)
        else:
            canvas.setForeground(Canvas.COLOR_WHITE)

        lineoffset = 0
        rowoffset = 0
        maxlines = len(self.insertbuffer)
        if self.insertbufferpos[0] >= self.size[1]:
            lineoffset = (self.insertbufferpos[0]+1) -self.size[1]
        if self.insertbufferpos[1] > self.size[0]-1:
            rowoffset = (self.insertbufferpos[1]) - (self.size[0]-1)
        if maxlines >= self.size[1]:
            maxlines = self.size[1]
        
        for l in range(0, maxlines):
            strbeg = rowoffset
            strend = self.size[0]+rowoffset
            
            if len(self.insertbuffer[lineoffset+l]) <= strend:
                strend = len(self.insertbuffer[lineoffset+l])
            canvas.printString((0,l),self.insertbuffer[lineoffset+l][strbeg:strend].ljust(self.size[0]))
        if self.hasFocus:
            canvas.moveCursor((self.insertbufferpos[1]-rowoffset, self.insertbufferpos[0]-lineoffset))
            canvas.setCursorVisible(True)
        else:
            canvas.setCursorVisible(False)

        
    def onCommand(self, command):
        if command in ('\x1b[A', '\x1b[B', '\x1b[C', '\x1b[D'):
            if command[2] == 'A': #up
                if self.insertbufferpos[0] > 0:
                    self.insertbufferpos[0] -= 1
                    if self.insertbufferpos[1] > len(self.insertbuffer[self.insertbufferpos[0]]):
                        self.insertbufferpos[1] = len(self.insertbuffer[self.insertbufferpos[0]])
            elif command[2] == 'B': #down
                if self.insertbufferpos[0]+1 < len(self.insertbuffer):
                    self.insertbufferpos[0] += 1
            elif command[2] == 'C': #right
                if self.insertbufferpos[1] < len(self.insertbuffer[self.insertbufferpos[0]]):
                    self.insertbufferpos[1] += 1
                elif self.insertbufferpos[0]+1 < len(self.insertbuffer):
                    self.insertbufferpos[0] += 1
                    self.insertbufferpos[1] = 0
            elif command[2] == 'D': #left
                if self.insertbufferpos[1] > 0:
                    self.insertbufferpos[1] -=1
                elif self.insertbufferpos[0] > 0:
                    self.insertbufferpos[0] -=1
                    self.insertbufferpos[1] = len(self.insertbuffer[self.insertbufferpos[0]])
        elif command == '\x7f' and self.insertbufferpos > 0: #backspace
            if self.insertbufferpos[1] > 0:
                self.insertbuffer[self.insertbufferpos[0]] = self.insertbuffer[self.insertbufferpos[0]][:self.insertbufferpos[1]-1] + self.insertbuffer[self.insertbufferpos[0]][self.insertbufferpos[1]:]
                self.insertbufferpos[1] -= 1
            elif self.insertbufferpos[0] > 0:
                self.insertbufferpos[1] = len(self.insertbuffer[self.insertbufferpos[0]-1])
                self.insertbuffer[self.insertbufferpos[0]-1] += self.insertbuffer[self.insertbufferpos[0]]
                self.insertbuffer.pop(self.insertbufferpos[0])
                self.insertbufferpos[0] -= 1
        elif command == '\x1b[3~' and self.insertbufferpos < len(self.insertbuffer): #del
            pass#self.insertbuffer = self.insertbuffer[:self.insertbufferpos] + self.insertbuffer[self.insertbufferpos+1:]
        elif len(command) > 0 and command[0] != '\x1b' and command[0] != '\0' and command != '\x7f':
            command = command.replace('\r', '\n').replace('\n\n', '\n').replace('\x00', '')
            command = command.decode('utf8')
            lines = command.split('\n')
            if len(lines) > 1:
                end = self.insertbuffer[self.insertbufferpos[0]][self.insertbufferpos[1]:]
                self.insertbuffer[self.insertbufferpos[0]] = self.insertbuffer[self.insertbufferpos[0]][:self.insertbufferpos[1]] + lines[0]
                for l in range(1,len(lines)):
                    self.insertbuffer.insert(self.insertbufferpos[0]+l, lines[l])
                self.insertbuffer[self.insertbufferpos[0]+(len(lines)-1)] = lines[len(lines)-1] + end
                self.insertbufferpos[0] += len(lines)-1
                self.insertbufferpos[1] = len(lines[len(lines)-1])
            else:
                self.insertbuffer[self.insertbufferpos[0]] = self.insertbuffer[self.insertbufferpos[0]][:self.insertbufferpos[1]] + lines[0] + self.insertbuffer[self.insertbufferpos[0]][self.insertbufferpos[1]:]
                self.insertbufferpos[1] += len(lines[0])
        self.repaint()
        
class Button(Input):
    
    def __init__(self, label=''):
        Input.__init__(self)
        self.label = label
    
    def paint(self, canvas):
        Input.paint(self, canvas)
        if self.hasFocus:
            canvas.setForeground(Canvas.COLOR_YELLOW)
        else:
            canvas.setForeground(Canvas.COLOR_WHITE)
        canvas.setCursorVisible(False)
        canvas.printString((0,0), '['+ self.label.center(self.size[0]-2)+']')
        
    def onPress(self):
        pass

    def onCommand(self, command):
        if command[0] == '\r' or command[0] == '\n':
            self.onPress()