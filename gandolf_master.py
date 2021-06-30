from socket import socket
client=socket()
client.connect(('localhost',9069))
client.sendall(b'https://www.youtube.com/watch?v=G1IbRujko-A\n')
client.close()
