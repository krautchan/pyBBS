'''
Created on Jul 15, 2012

@author: teddydestodes
'''
from bbs import view, window
import atexit, sys
from miniboa import TelnetServer
CLIENTS = []
conncount = 0
def on_exit():
        print "shutting down"
        for client in CLIENTS:
            reset(client)


def clearScreen(client):
    client.send('\x1b[37;44m\x1b[37,44mblah\x1b[2J\r\n')

def reset(client):
    client.send('\x1bc\x1b[2JDankefein\r\n')

def my_on_connect(client):
    global conncount

    client.request_terminal_type()

    #client.request_wont_line_mode()
    client.request_do_sga()
    client.request_will_sga()
    client.request_will_echo()
    client.request_naws()
    client.shouldQuit = False
    client.startup = True
    client.lineMode = True
    CLIENTS.append(client)
    conncount = conncount + 1
    client.view = view.Title(client)
    client.view.setClientCount(len(CLIENTS))
    client.view.setConnectionCount(conncount)
    #client.view.paint()
    
    
def updateClient(client):
    if client.shouldQuit:
        client.deactivate()
        return
    if client.terminal_type == 'unknown client':
        client.send('waiting for terminfo\r\n');
        return
    client.view.setSize(client.columns, client.rows)
    client.view.update()

    if client.cmd_ready :
        try:
            cmd = client.get_command()
            print len(cmd)
            if cmd == '\x11': # CTRL+Q
                clearScreen(client)
                reset(client)
                client.shouldQuit = True
            elif cmd == client.terminfo.tigets('kf1'): #F1
                client.view.showHelp()
            elif cmd == client.terminfo.tigets('kf2'): #F1
                client.view = view.Streetview(client)
                client.view.setSize(client.columns, client.rows)
                client.view.paint()
                client.view.update()
            else:
                client.view.handleInput(cmd)
        except:
            clearScreen(client)
            reset(client)
            client.send(sys.exc_info()[1])
            client.shouldQuit = True

def my_on_disconnect(client):
    CLIENTS.remove(client)
    
if __name__ == '__main__':
    
    atexit.register(on_exit)
    
    server = TelnetServer()
    server.on_connect=my_on_connect
    server.on_disconnect=my_on_disconnect
    print "BBS listening on port %s" % (server.port,)
    while True:
        server.poll()
        for client in CLIENTS:
            updateClient(client)