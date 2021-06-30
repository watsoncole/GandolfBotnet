from socket import socket
import webbrowser as web
client = socket(); buffer=b''
client.connect(('localhost', 9069))
while True:
    try:
        data=client.recv(1024)
    except:
        client.close(); break
    buffer+=data
    if b'\n' in data:
        web.open(buffer[:-1].decode())
        buffer=b''
