from termlib.canvas import Canvas, BBox, add
from struct import pack, unpack

class ImgAttr(object):
    def __init__(self, attr=None, foreground=0, background=0):
        if attr == None:
            self.bold = False
            self.italic = False
            self.foreground = foreground
            self.background = background
        else:
            self.foreground = attr/256
            self.background = attr%256

    def hash(self):
        return self.foreground*256+self.background

    def __repr__(self):
        return '<ImgAttr %d, %d >' %(self.foreground, self.background)

class Image(object):
    
    def __init__(self):
        self.data = {}

    def put(self, attrs, position, string):
        try:
            self.data[attrs.hash()].append((position, string))
        except KeyError:
            self.data[attrs.hash()] = [(position, string)]

    def draw(self, canvas):
        for key in self.data.keys():
            attr = ImgAttr(key)
            canvas.setBackground(attr.background)
            canvas.setForeground(attr.foreground)
            for val in self.data[key]:
                canvas.printString(val[0],val[1])

    def getBBox(self):
        bbox = BBox([0,0],[0,0])
        for key in self.data.keys():
            for val in self.data[key]:
                bbox.addPoint(add(val[0],(len(val[1]),0)))
        return bbox

class Drawable(object):
    
    def __init__(self):
        self.canvas = Canvas()
        self.children = []
        self.size = [0,0]
        self.position = [0,0]
        self.focusable = True
        self.hasFocus = False
        self.childWithFocus = None
        self.parent = None
        self.visible = True
        self.foreground = Canvas.COLOR_WHITE
        self.background = Canvas.COLOR_BLACK
        
    def addChild(self,child):
        child.parent = self
        self.canvas.addChild(child.canvas)
        self.children.append(child)
        
        
    def onRepaint(self, canvas):
        pass
    
    def onFocus(self):
        self.repaint()
        pass
    
    def onCommand(self,command):
        print "implement me", self
    
    def setBackground(self, color):
        self.background = color
    
    def setForeground(self, color):
        self.foreground = color
    
    def paint(self, canvas):
        canvas.size = self.size
        canvas.position = self.position
        canvas.clearBuffer()
        canvas.setForeground(self.foreground)
        canvas.setBackground(self.background)
        
    
    def repaint(self):
        self.paint(self.canvas)
        self.onRepaint(self.canvas)
        for child in self.children:
            if child.visible:
                child.repaint()

    def handleCommand(self,command):
        if self.visible:
            if self.hasFocus:
                self.onCommand(command)
            else:
                for child in self.children:
                    child.handleCommand(command)
    
    def removeFocus(self):
        if self.hasFocus:
            self.hasFocus = False
            self.onFocus()
        for child in self.children:
            child.removeFocus()
        self.childWithFocus = None

    def giveFocus(self):
        print 'p'
        if not self.isVisible():
            return
        self.getRoot().removeFocus()
        self.hasFocus = True
        da = self
        while da:
            if not da.parent:
                break;
            print da
            da.parent.childWithFocus = da
            da = da.parent

    def isVisible(self):
        if self.parent:
            if self.parent.visible:
                return self.parent.isVisible()
            else:
                return False
        else:
            return self.visible

    def getRoot(self):
        if self.parent:
            return self.parent.getRoot()
        else:
            return self

    def cycleFocus(self):
        if not self.visible:
            self.removeFocus()
            return False
        if self.focusable:
            if self.childWithFocus == None and not self.hasFocus:
                self.hasFocus = True
                self.onFocus()
                return True
            else:
                self.hasFocus = False
                self.onFocus()
        if len(self.children) > 0:
            if self.childWithFocus == None:
                self.childWithFocus = self.children[0]
            while not self.childWithFocus.cycleFocus():
                ci = self.children.index(self.childWithFocus)
                
                if ci + 1 >= len(self.children):
                    self.childWithFocus = None
                    return
                else:
                    self.childWithFocus = self.children[ci+1]
        return self.childWithFocus != None