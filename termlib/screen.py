'''
Created on Jul 26, 2012

@author: teddydestodes
'''
from termlib.canvas import Canvas
from termlib.terminfo import TermInfo
from termlib import Drawable
class Screen(Drawable):
    '''
    classdocs
    '''

    def __init__(self, title='Screen', terminfo=TermInfo('vt100')):
        Drawable.__init__(self)
        self.title = title
        self.drawTitle = False
        self.drawBorder = False
        self.children = []
        self.focus = None
        self.focusable = False
        self.size = [80,24]
        self.setTermInfo(terminfo)

    def setTermInfo(self, terminfo):
        self.canvas.setTermInfo(terminfo)

    def paint(self, canvas):
        Drawable.paint(self, canvas)
        canvas.setForeground(self.foreground)
        canvas.setBackground(self.background)
        canvas.clear()
        if self.drawBorder:
            canvas.drawBox((0,0),self.size)