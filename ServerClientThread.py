import threading
import os


# The class in parentheses means that we are inheriting Thread class from threading module
# If you imported threading as 'from threading import *' you would type this as
# class ServerClientThread(Thread)
# though that is not the recommended way of importing modules and should generally use 'import <module>'
class ServerClientThread(threading.Thread):
    # Class constructor
    def __init__(self, client_socket, client_address):
        # Setting the class attributes
        self.socket = client_socket
        self.address = client_address  # We never actually use it here :o
        # Calling the constructor of super class (Thread class in this case)
        super().__init__()
        # Start the thread
        self.start()

    # We're redefining the Thread class' run() method
    def run(self):
        # Shared files relative path
        shared_dir = 'Shared Files'
        # Make a shareable directory if one does not exist
        if shared_dir not in os.listdir():
            os.mkdir(shared_dir)
        # Get files in the directory, returns a list
        files = os.listdir(shared_dir)
        # Join the list into a string for sending if list is not empty else send a "status message"
        send_data = '\n'.join(files) if files else 'EMPTY'
        # Send the data
        self.socket.send(send_data.encode())
        # You could also do something like this
        # self.socket.send( '\n'.join(os.listdir(shared_dir)).encode() )
        # but that's not quite as readable

        if files:
            # Active directory
            path = shared_dir

            # Loops until the user hits a file to download
            while True:
                # We're expecting a file or folder name from the user
                filename = self.socket.recv(4096).decode()
                print('User requested "{}"'.format(filename))
                # Path to dir or file gets updated (we add what the user input to the existing path)
                path += '/{}'.format(filename)

                if os.path.isfile(path):
                    # Send a status message indicating it's a file
                    self.socket.send('FILE'.encode())

                    # We check if it is a file and open it and send it's contents if it is
                    # Now, here you have two choices:
                    # The 'with open(filename) as file' route
                    # or the 'file = open(filename)' and the eventual 'file.close()' route
                    # We'll take the better one
                    # 'rb' represents the mode the file is opened in - read binary
                    # best to check out the docs, chapter 7.2 - https://docs.python.org/3/tutorial/inputoutput.html
                    with open(path, 'rb') as file:
                        # No need to encode() as it's being read as binary
                        self.socket.sendall(file.read())
                    print('File successfully sent')
                    break
                # If it is a directory instead, we send the contents of said dir to the user
                elif os.path.isdir(path):
                    # Send a status message indicating it's a directory
                    self.socket.send('DIR'.encode())
                    # Contents of the directory the user selected
                    current_dir = os.listdir(path)
                    # Prepare and send data
                    send_data = '\n'.join(current_dir) if files else 'EMPTY'
                    self.socket.send(send_data.encode())
        else:
            print('No shareable files available')
