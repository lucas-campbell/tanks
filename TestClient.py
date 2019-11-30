#!/usr/bin/env python3
######################
# Cam, Lucas, Omar
# 11/7/19
######################
import socket
import pickle
import sys
from Arena import *

def main(argv, defaultHost):
    if defaultHost:
        HOST = '127.0.0.1'
    else:
        HOST = input('SERVER IP:')
    PORT = 47477      

    HEADERSIZE = 10 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        #while True:
        full_msg = b''
        new_msg = True
        while True:
            msg = s.recv(1024)
            if new_msg:
                print("new msg len:", msg[:HEADERSIZE])
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
                    
            full_msg += msg
        
            #print(len(full_msg))
            
            if len(full_msg)-HEADERSIZE == msglen:
                print("full msg received")
                print(pickle.loads(full_msg[HEADERSIZE:]))
                arena = pickle.loads(full_msg[HEADERSIZE:])
                for t in arena.tiles:
                    if t.is_obstacle:
                        print(t.x, t.y, t.is_obstacle)
                s.sendall("Finished".encode())
                s.close()
                break
                # REUSE SOCKET FORMAT #
                #new_msg = True
                #full_msg = b""
            

if __name__ == '__main__':
    defaultHost = False
    for arg in sys.argv[1:]:
        if arg == '-o':
            defaultHost = True
    main(sys.argv[1:], defaultHost)        
