from socket import *
from ServerClientThread import *


# Port number we are binding our socket to
server_port = 2222
server_address = 'localhost'
# We create a socket
server_socket = socket(AF_INET, SOCK_STREAM)
try:
    # We try to bind the socket to specified address and port
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print('Listening for connections')
    while True:
        # We accept a connection
        client_socket, client_address = server_socket.accept()
        print("A user connected...")
        # We open a thread for the newly connected client
        ServerClientThread(client_socket, client_address)
except:
    # Prints out in case of a thrown exception
    print('An error has occurred')