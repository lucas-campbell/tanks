#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# 11/5/19
# Sample Server Class
##########################
import socket, select
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
    
    # TEST ARENA #
    obstacleTiles = [Tile(2,4), Tile(3,3), Tile(0,0), Tile(1,7)]
    testArena = Arena(obstacleTiles = obstacleTiles)
    for t in testArena.tiles:
        if t.is_obstacle:
            print(t.x, t.y, t.is_obstacle)
    
    #print(sys.getsizeof(data))
    # CONNECTION SETUP W/ SOCKETS #
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server.setblocking(0)
    server.bind((HOST, PORT))
    print('Bound to Socket')
    server.listen(5)
    # SETUP UNBLOCKED CONNECTIONS #
    inputs = [server]
    outputs = []
    messages = []

    while True:
        conn, addr = server.accept()
        print('Connected to:', addr)
        data = pickle.dumps(testArena)
        header = str(len(data))
        
        # MSG IDENTIFIER/UPDATE MANAGER #
        if header == '':
        elif header == '':
        else:

        print(header)
        data = bytes(header.ljust(HEADERSIZE), 'utf-8')+data
        #print(data)
        conn.sendall(data)
        resp = conn.recv(32)
        print(resp.decode())
        conn.close()

    print('Connection Finished')

if __name__ == '__main__':
    defaultHost = False
    for arg in sys.argv[1:]:
        if arg == '-o':
            defaultHost = True

    main(sys.argv[1:], defaultHost)
