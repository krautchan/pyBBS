'''
Created on Jul 15, 2012

@author: teddydestodes
'''

class Borg(object):
    """RESISTANCE IS FUTILE :3
    """
    _shared = {}
    def __new__(cls,*args,**kwargs):
        inst = object.__new__(cls)
        inst.__dict__ = cls._shared
        return inst

class Drawable(object):
    
    UNKNOWN = 0
    WINDOW  = 1
    DIALOG  = 2
    
    def __init__(self, client, parent = None):
        self.parent = parent
        self.size = ()
        self.hasFocus = False
        self.type = Drawable.UNKNOWN
        self.client = client
        self.children = []
        self.buffer = ''
        self.title = 'drawable'
        
        self.help = {'F11': 'Hilfe', 'ESC': 'schliesst Fenster','STRG+Q': 'beenden'}
        
        if parent == None:
            self.hasFocus = True
            self.size = (client.columns, client.rows)
    
    def addChild(self, child, focus = True):
        if focus:
            for child in self.children:
                if child.hasFocus:
                    child.hasFocus = False
                    child.paint() # HNG can't be right
            if self.hasFocus:
                self.hasFocus = False
            child.hasFocus = True
            child.paint()
        self.children.append(child)
    
    def removeChild(self, child):
        self.children.remove(child)
        if child.hasFocus:
            if len(self.children) > 0:
                self.children[-1].hasFocus = True
            else:
                self.hasFocus = True
        self.paint()
    
    def close(self):
        for child in self.children:
            child.close()
        if self.parent:
            self.parent.removeChild(self)
    
    def setSize(self, columns, rows):
        if self.size != (columns, rows):
            self.size = (columns, rows)
            self.paint()
            
    def paint(self):
        """
        this should not issued directly
        """
        self.buffer = ''
        self.repaint()
        for child in self.children:
            child.paint()
            self.buffer = self.buffer + child.buffer
        self.client.send(self.buffer)
    
    def clearScreen(self):
        self.buffer = self.buffer + '\x1b[37;44m\x1b[37,44mblah\x1b[2J\r\n'
    
    def repaint(self):
        """
        paint method
        """
        pass
    
    def handleInput(self, input):
        if self.hasFocus:
            self._handleInput(input)
        else: #just cycle though the children hopefully someone handles it
            for child in self.children:
                child.handleInput(input)

    def _handleInput(self,input):
        if input == '\x1b':
            self.close()
        pass