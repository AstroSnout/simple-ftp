import socket
import os


server_address = 'localhost'
server_port = 2222

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_address, server_port))
# We are expecting a list of files in the shared directory
files = sock.recv(4096).decode()

if files == 'EMPTY':
    print('There are no shared files on the server')
else:
    # Print out the files that were sent by the server
    print('These are the files available on the server:\n{}'.format(files))
    # Ask the user to choose a file
    while True:
        filename = input('Input the name of the file you want to download')
        # You have a choice of doing the validation server-side or client-side
        # I'm lazy, so I'll do it here, client-side

        # Check if input file/folder is in the received files
        if filename in files.split('\n'):
            # Send the file/folder name to the server
            sock.send(filename.encode())
            # We expect to receive a status code indicating whether it's a file or a dir
            status = sock.recv(4096).decode()
            # We expect to receive contents of the file if file or dir listing if dir
            files = sock.recv(4096).decode()
            if status == 'DIR':
                print('These are the files in the selected folder:\n{}'.format(files))
            elif status == 'FILE':
                break
        else:
            print('This file does not exist, try again')

    # make downloads folder if it does not exist in client root directory
    if 'Downloads' not in os.listdir():
        os.mkdir('Downloads')
    # Now to write this to a file
    with open('Downloads/{}'.format(filename), 'a+') as file:
        file.write(files)
    print('Successfully saved the file to Downloads/{}'.format(filename))