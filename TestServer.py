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

HEADERSIZE = 16

def getData(tsocket):
    msg = tsocket.recv(HEADERSIZE)
    header = msg[:HEADERSIZE]
    msg_len = int(header)
    return header, tsocket.recv(msg_len)

def main(argv, defaultHost):
    if defaultHost:
        HOST = '127.0.0.1'
    else:
        HOST = input('SERVER IP:')
        PORT = 47477
    
    
    # TEST ARENA #
    obstacleTiles = [Tile(2,4), Tile(3,3), Tile(0,0), Tile(1,7)]
    testArena = Arena(obstacleTiles = obstacleTiles)
    for t in testArena.tiles:
        if t.is_obstacle:
            print(t.x, t.y, t.is_obstacle)
    
    #print(sys.getsizeof(data))
    # CONNECTION SETUP W/ SOCKETS #
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    #print('Bound to Socket')
    server.listen(10)
    
    # SETUP UNBLOCKED CONNECTIONS #
    connections = [server]
    writes = []
    broken = []

    while True:

        read_socks, write_socks, error_socks = select.select(connections, writes, broken)

        print(len(connections))
        
        if len(connections) == 3: #3:, set 2 for testing 
            #have all connections, run the game
            for sock in read_socks:
                if sock != server:
                    # Get message data
                    header, data = getData(sock)

                    ###MAKE MESSAGE CHANEGS/DATA UPDATES HERE###
                    oldInfo = pickle.loads(data)
                    
                    newData = oldInfo #change oldInfo and store it in newData
                    print("Sending Data")


                    # Client is sending updated information
                    for client in read_socks:
                        if client != server and client != sock: #and client != sock, turned off for testing one client
                            print("Sent")
                            update = pickle.dumps(newData)
                            msg_len = len(update)
                            pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
                            update = bytes(pack_header, 'utf-8')+update
                            client.sendall(update)

            for sock in write_socks:
                if sock != server:
                    print(sock)
                    
        elif len(connections) > 3:
            #too many connections, remove last connection
            connections.pop(len(connections)-1)
        else: 
            #wait on more connections                
            for sock in read_socks:
                if sock == server:
                    # New connection to add to server
                    new_conn, new_addr = server.accept()
                    connections.append(new_conn)
                    print(len(connections))
                    print("Connected user from ip:{}".format(new_addr))


if __name__ == '__main__':
    defaultHost = False
    for arg in sys.argv[1:]:
        if arg == '-o':
            defaultHost = True

    main(sys.argv[1:], defaultHost)
