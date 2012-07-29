'''
Created on Jul 15, 2012

@author: teddydestodes
'''
import atexit
import os
import chan.sql
from miniboa import TelnetServer
from ConfigParser import SafeConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
CLIENTS = []
conncount = 0
current_dir = os.path.dirname(os.path.abspath(__file__))
config = SafeConfigParser()
config.read(os.path.join(current_dir,'etc','config.cfg'))

engine = create_engine("%s://%s:%s@%s/%s?charset=utf8" % (config.get('database', 'engine'),
                                                          config.get('database', 'username'),
                                                          config.get('database', 'password'),
                                                          config.get('database', 'host'),
                                                          config.get('database', 'database')))
Session = sessionmaker(bind=engine)
session = Session()

chan.sql.Base.metadata.create_all(engine)

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
    #client.request_wont_line_mode()
    client.request_do_sga()
    client.request_will_sga()
    client.request_will_echo()
    client.request_dont_echo()
    client.request_naws()
    client.request_terminal_type()
    client.shouldQuit = False
    client.startup = True
    client.lineMode = False
    client.session = session
    CLIENTS.append(client)
    conncount = conncount + 1
    
def updateClient(client):
    if client.shouldQuit:
        client.deactivate()
        return

    if client.terminal_type == 'unknown client':
        client.send('waiting for terminfo\r\n');
        return
    
    if client.startup:
        client.startup = False
        import chan
        client.view = chan.Welcome(client)
    
    if client.view.size != [client.columns, client.rows]:
        client.view.size = [client.columns, client.rows]
        client.view.repaint()
    
    if client.cmd_ready:
        try:
            cmd = client.get_command()
            if cmd == client.terminfo.tigets('kf12'):
                client.shouldQuit = True
                clearScreen(client)
                reset(client)
                return
            client.view.onInput(cmd)
        except:
            clearScreen(client)
            reset(client)
            client.send('FEHLERFEHLERFEHLERFEHLERFEHLERFEHLERFEHLERFEHLERFEHLERFEHLERFEHLERFEHLER!!!!')
            import traceback
            traceback.print_exc()
            client.shouldQuit = True
    client.view.update()

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