'''
Created on Jul 26, 2012

@author: teddydestodes
'''

def max(x, y):
    return x ^ ((x ^ y) & -(x < y))

def min(x, y):
    return y ^ ((x ^ y) & -(x < y))

def sub(a,b):
    c = []
    for i in range(0,len(a)):
        c.append(a[i] - b[i])
    return c

def div(a,b):
    c = []
    for i in range(0,len(a)):
        c.append(a[i] / b[i])
    return c

def mul(a,b):
    c = []
    for i in range(0,len(a)):
        c.append(a[i] * b[i])
    return c

def add(a, b):
    c = []
    for i in range(0,len(a)):
        c.append(a[i] + b[i])
    return c

class BBox(object):
    
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def getIntersection(self, bbox):
        if self.intersect(bbox):
            return BBox((max(self.min[0],bbox.min[0]),max(self.min[1],bbox.min[1])),(min(self.max[0],bbox.max[0]),min(self.max[1],bbox.max[1])))
        else:
            return None
    
    def intersect(self, bbox):
        return (self.min[0] < bbox.max[0]) and (self.max[0] > bbox.min[0]) and (self.min[0] < bbox.max[0]) and (self.max[0] > bbox.min[0])
    
    def move(self, vector):
        self.min = add(self.min, vector)
        self.max = add(self.max, vector)
    
    def __repr__(self):
        return '<BBox (%d,%d), (%d,%d)>' % (self.min[0], self.min[1], self.max[0], self.max[1])
    
    def isInside(self, point):
        return (self.min[0] <= point[0] <= self.max[0]) and (self.min[1] <= point[1] <= self.max[1])

    def addPoint(self, point):
        if point[0] > self.max[0]:
            self.max[0] = point[0]
        if point[0] < self.min[0]:
            self.min[0] = point[0]
        if point[1] > self.max[1]:
            self.max[1] = point[1]
        if point[1] < self.min[1]:
            self.min[1] = point[1]


class Canvas(object):
    
    CHARACTERS = 1
    ALTERNATE = 2
    
    COLOR_BLACK = 0
    COLOR_RED = 1
    COLOR_GREEN = 2
    COLOR_YELLOW = 3
    COLOR_BLUE = 4
    COLOR_MAGENTA = 5
    COLOR_CYAN = 6
    COLOR_WHITE = 7
    COLOR_GREY = 8
    COLOR_LIGHTRED = 9
    COLOR_LIGHTGREEN = 10
    COLOR_LIGHTYELLOW = 11
    COLOR_LIGHTBLUE = 12
    COLOR_LIGHTMAGENTA = 13
    COLOR_LIGHTLIGHTCYAN = 14
    COLOR_LIGHTGREY = 15
    
    
    def __init__(self, size=None, parent=None, terminfo=None):
        self.buffer = ''
        self.charset = Canvas.CHARACTERS
        self.bbox = None
        if size:
            self.size = size
        else:
            self.size = [0,0]
        self.parent = parent
        if self.parent:
            self.parent.addChild(self)
        self.position = [0,0]
        self.offset = [0,0]
        self.children = []
        if terminfo == None and parent != None:
            self.terminfo = parent.terminfo
        else:
            self.terminfo = terminfo
            
        self.background = Canvas.COLOR_BLACK
        self.foreground = Canvas.COLOR_WHITE
        self.cursorVisible = True

    def fillBackground(self):
        for i in range(0,self.size[1]):
            self.printString((0,i),' '*self.size[0])

    def addChild(self, child):
        child.parent = self
        child.terminfo = self.terminfo
        self.children.append(child)
    
    def setTermInfo(self, terminfo):
        self.terminfo = terminfo
        for child in self.children:
            child.setTermInfo(terminfo)
    
    def getBuffer(self):
        buffer = self.buffer
        for child in self.children:
            buffer += child.getBuffer()
        return buffer
    
    def clearBuffer(self):
        """Clears the buffer"""
        self.buffer = ''
    
    def clear(self):
        #self.clearBuffer()
        self.buffer += self.terminfo.tigets('clear')
        self.buffer += self.terminfo.tigets('sgr0')
    
    def moveCursor(self, position):
        """Moves cursor to relative position
        returns True if cursor will be moved
        
        """
        pos = self.getPosition()
        if self.parent:
            pos = add(pos,self.parent.getOffset())
        position = add(pos,position)
        self.buffer += self.terminfo.tigets('cup', position[1], position[0])
        return True
    
    def getMask(self):
        self.bbox = BBox(self.getPosition(), add(self.getPosition(),self.size))
        if self.parent:
            self.bbox.move(self.parent.getOffset())
            parentMask = self.parent.getMask()
            if parentMask:
                return self.bbox.getIntersection(parentMask)
            else:
                return None
        else:
            return self.bbox

    def getOffset(self):
        if self.parent:
            return add(self.parent.getOffset(),self.offset)
        else:
            return self.offset
        
    def getPosition(self):
        if self.parent:
            return add(self.parent.getPosition(),self.position)
        else:
            return self.position
    
    def printString(self, position, string, charset=CHARACTERS):
        """Prints string at given position
        """
        if self.parent:
            mask = self.parent.getMask()
        else:
            mask = self.getMask()
        pos = self.getPosition()
        if self.parent:
            pos = add(pos, self.parent.getOffset())
        lc = 0
        self.setCharset(charset)
        if not mask:
            return False
        
        for line in string.split('\n'):
            lpos = add(pos,position)
            sbeg = 0
            send = len(line)
            if lpos[0] < mask.min[0]: 
                sbeg = mask.min[0]-lpos[0]
            if lpos[0]+send > mask.max[0]:
                send = sbeg + (mask.max[0]-lpos[0])-sbeg
            if sbeg < send and lpos[1] < mask.max[1] and lpos[1] >= mask.min[1]:
                self.moveCursor((position[0]+sbeg, position[1]))
                self.buffer+= line[sbeg:send]
            lc+=1
    
    def drawLine(self, position, width=None, height=None, char=None):
        if width != None:
            if not char:
                char = 'q'
            self.printString(position,self.terminfo.getAlternateChar(char)*width, charset=Canvas.ALTERNATE)
        elif height != None:
            if not char:
                char = 'x'
            for h in range(0,height):
                self.printString((position[0], position[1]+h),self.terminfo.getAlternateChar(char), charset=Canvas.ALTERNATE)
    
    def drawBox(self, position, size):
        self.drawLine((position[0]+1,position[1]),width=size[0]-2)
        self.drawLine((position[0]+1,position[1]+size[1]-1),width=size[0]-2)
        self.drawLine((position[0],position[1]+1),height=size[1]-2)
        self.drawLine((position[0]+size[0]-1,position[1]+1),height=size[1]-2)
        self.printString(position,'l', charset=Canvas.ALTERNATE)
        self.printString((position[0], position[1]+size[1]-1),'m', charset=Canvas.ALTERNATE)
        self.printString((position[0]+size[0]-1, position[1]),'k', charset=Canvas.ALTERNATE)
        self.printString((position[0]+size[0]-1, position[1]+size[1]-1),'j', charset=Canvas.ALTERNATE)
    
    def setForeground(self, color):
        """Sets Foreground to color"""
       # if self.getForeground() != color:
       #     self._propagateForeground(color)
        self.buffer += self.terminfo.tigets('setaf', color)
    
    def _propagateForeground(self, color):
        if self.parent:
            self.parent._propagateForeground(color)
        else:
            self.foreground = color
    
    def getForeground(self):
        if self.parent:
            return self.parent.getForeground()
        else:
            return self.foreground
    
    def setBackground(self, color):
        """Sets Background to color"""
        #if self.getBackground() != color:
        #   self._propagateBackground(color)
        self.buffer += self.terminfo.tigets('setab', color)
    
    def _propagateBackground(self, color):
        if self.parent:
            self.parent._propagateBackground(color)
        else:
            self.background = color
    
    def getBackground(self):
        if self.parent:
            return self.parent.getBackground()
        else:
            return self.background

    def setCharset(self, charset):
        """Sets character mode"""
        if self.getCharset() != charset:
            self._propagateCharset(charset)
            if charset == Canvas.ALTERNATE:
                self.buffer += self.terminfo.tigets('smacs')
            else:
                self.buffer += self.terminfo.tigets('rmacs')
    
    def _propagateCharset(self, charset):
        if self.parent:
            self.parent._propagateCharset(charset)
        else:
            self.charset = charset

    def getCharset(self):
        if self.parent:
            return self.parent.getCharset()
        else:
            return self.charset
        
    def setCursorVisible(self, visible):
        if self.getCursorVisible() != visible:
            self._propagateCursorVisible(visible)
            if visible:
                self.buffer += self.terminfo.tigets('cvvis')
            else:
                self.buffer += self.terminfo.tigets('civis')

    def _propagateCursorVisible(self, visible):
        if self.parent:
            self.parent._propagateCursorVisible(visible)
        else:
            self.cursorVisible = visible
    
    def getCursorVisible(self):
        if self.parent:
            return self.parent.getCursorVisible()
        else:
            return self.cursorVisible