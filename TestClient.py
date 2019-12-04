#!/usr/bin/env python3
######################
# Cam, Lucas, Omar
# 11/7/19
######################
import socket
import pickle
import sys
#from Message import *
from Arena import *

HEADERSIZE = 16

def main(argv, defaultHost):
    if defaultHost:
        HOST = '127.0.0.1'
    else:
        HOST = input('SERVER IP:')
    PORT = 47477      


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.setblocking(0)
    client.connect((HOST, PORT))

    is_connected = False

    #Client connection loop
    while True:
        if not is_connected:
            #msg = client.recv(64)
            #print(msg.decode())
            print("Connected")
            is_connected = True
        else:
            #send information here
            try:
                #data = Message()
                data = pickle.dumps('hi')
                msg_len = str(len(data))
                pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
                data = bytes(pack_header, 'utf-8')+data
                client.sendall(data)
                
                #wait for update here
                #print("Updating")
                full_msg = b''
                new_msg = True
                end_msg = True
                
                while end_msg:
                    msg = client.recv(HEADERSIZE)

                    if not len(msg):
                        continue
                        #print('Connection closed by the server')
                        #exit()

                    if new_msg:
                        msg_header = msg[:HEADERSIZE]
                        msg_length = int(msg_header)
                        new_msg = False

                    full_msg += msg

                    print(len(full_msg))

                    if len(full_msg) - HEADERSIZE == msg_length:
                        data = pickle.loads(full_msg[HEADERSIZE:])
                        ### DATA MANIP/SCREEN UPDATES HERE ###
                        print(data)
                        
                        end_msg = False
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue

    print("Game Over")

if __name__ == '__main__':
    defaultHost = False
    for arg in sys.argv[1:]:
        if arg == '-o':
            defaultHost = True
    main(sys.argv[1:], defaultHost)        
