#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# 11/5/19
# Sample Server Class
##########################
import socket, select
import pickle
import sys
from memory import *
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
    
    #init server state conditions
    player1 = Player_pos(pos = (200, 0), direct = UDLR.down)
    player2 = Player_pos(pos = (200, 400), direct = UDLR.up)
    players = [player1, player2]
    state = State(players, _p1_missles = [], _p2_missles = [], _game_over = False)
    sample_msg = Memory(player1, new_missles = [], game_over = False, p_won = False)

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
        
        if len(connections) == 3:
            #have all connections, run the game
            try:
                for sock in read_socks:
                    if sock != server:
                        # Get message data
                        header, data = getData(sock)

                        ###MAKE MESSAGE CHANEGS/DATA UPDATES HERE###
                        player_data = pickle.loads(data)
                        # Notes:
                            #Each tank should send ONLY their own info
                            #Prevents one tank from updating another tank's position
                        if sock == connections[1]:
                            #update from player1
                            state.ps[0] = player_data.player
                            state.p1_missles = player_data.missles
                            state.game_over = player_data.end
                        elif sock == connections[2]:
                            #update from player2
                            state.ps[1] = player_data.player
                            state.p2_missles = player_data.missles
                            state.game_over = player_data.end
                        else:
                            print("Uh oh, that's not right..")
                            exit() 
                        print("Sending Data")

                        # Client is sending updated information
                        for client in connections:
                            if client != server and client != sock: 
                                update = pickle.dumps(state)
                                msg_len = len(update)
                                pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
                                update = bytes(pack_header, 'utf-8')+update
                                client.sendall(update)
                                print("Sent")
            except ConnectionResetError:
                print(len(connections))
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
