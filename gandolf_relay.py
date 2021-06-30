from time import sleep
from socket import socket
from threading import Thread
from queue import Queue
#--Global State
connections=[]
msg_queue=Queue()
output_queue=Queue()
#--Printing
def print_out(*arg):
    output_queue.put(arg)
def print_loop():
    while True:
        print(*(output_queue.get()))
#--Server        
def deploy():
    while True:
        payload=msg_queue.get()
        interm=connections.copy()
        for client in interm:
            try:
                client[0].sendall(payload)
            except:
                continue
def dispatch(client):
    global connections; buffer=b''
    while True:
        try:
            data=client[0].recv(1024)
        except:
            connections.remove(client)
            print_out(client[1][0]+':%s'%client[1][1],
                'disconnected, total:',len(connections))
            client[0].close(); break
        buffer+=data
        if b'\n' in data:
            msg_queue.put(buffer)
            print_out('data received:',buffer[:-1].decode())
            buffer=b'' 
def establish(*params):
    global connections
    server = socket()
    server.bind(params)
    server.listen(5)
    while True:
        client=server.accept()
        connections.append(client)
        print_out(client[1][0]+':%s'%client[1][1],
            'connected, total:',len(connections))
        init(dispatch,client)
#--Wrapper
def init(f,*args):
    Thread(target=f,args=args).start()
#--Logic
init(establish,'localhost',9069)
init(establish,'0.0.0.0',9069)
init(deploy); print_out('server started...')
print_loop()
