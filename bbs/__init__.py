'''
Created on Jul 15, 2012

@author: teddydestodes
'''
import termlib.screen

class Screen(termlib.screen.Screen):
    
    def __init__(self, client, title='Screen'):
        termlib.screen.Screen.__init__(self, title, terminfo=client.terminfo)
        self.client = client
    
    def update(self):
        pass
    
    def onRepaint(self, canvas):
        termlib.screen.Screen.onRepaint(self, canvas)
        self.client.send(canvas.buffer)
    
    def addChild(self,child):
        child.onRepaint = self.onRepaint
        termlib.screen.Screen.addChild(self, child)
    
    def onInput(self, command):
        #print command, self.canvas.terminfo.tigets('cuf1'), self.canvas.terminfo.term
        if command == '\t':
            self.cycleFocus()
        else:
            self.handleCommand(command)