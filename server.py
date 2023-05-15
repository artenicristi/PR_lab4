from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_connections():
    while True:
        client_socket, client_address = server.accept()
        print('%s:%s is now connected.' % client_address)
        client_socket.send(bytes('Type your name and press enter to connect to the chat', 'utf8'))
        addresses[client_socket] = client_address
        Thread(target=client_communication, args=(client_socket,)).start()


def client_communication(client_socket):
    name = client_socket.recv(size).decode('utf8')
    if name not in allowed_clients:
        client_socket.send(bytes('Connection refused', 'utf8'))
        return
    welcome = 'Welcome %s! To leave, type !q' % name
    client_socket.send(bytes(welcome, 'utf8'))
    msg = '%s has joined the chat!' % name
    broadcast(bytes(msg, 'utf8'))
    clients[client_socket] = name

    while True:
        msg = client_socket.recv(size)
        if msg != bytes('!q', 'utf8'):
            broadcast(msg, name + ': ')
        else:
            client_socket.send(bytes('!q', 'utf8'))
            client_socket.close()
            del clients[client_socket]
            broadcast(bytes('%s has left the chat.' % name, 'utf8'))
            break


def broadcast(msg, prefix=''):
    for sock in clients:
        sock.send(bytes(prefix, 'utf-8') + msg)


host = 'localhost'
port = 9999
size = 512
addr = (host, port)
clients = {}
addresses = {}
allowed_clients = ['tester', 'admin', 'guest']


server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

orderNr = open('order', 'w')
orderNr.write(str(1))
orderNr.close()

server.listen(5)
print('The chat is open ...')
handle_connections = Thread(target=accept_connections())
handle_connections.start()
handle_connections.join()
server.close()