#!/usr/bin/env python3
######################
# Cam, Lucas, Omar
# 11/7/19
######################
import socket
import pickle
from Arena import *

def main(argv):
    HOST = '127.0.0.1'
    PORT = 65432       
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        arena = pickle.loads(data)
        for t in arena.tiles:
            if t.is_obstacle:
                print(t.x, t.y, t.is_obstacle)
    
if __name__ == '__main__':
    main(sys.argv[1:])
