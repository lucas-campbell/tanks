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
from constants import *

def getData(tsocket):
    '''Gets data and formats it using socket.recv'''
    msg = tsocket.recv(HEADERSIZE)
    header = msg[:HEADERSIZE]
    msg_len = int(header)
    return header, tsocket.recv(msg_len)

def add_header(data):
    '''Adds a header to a Bytes object'''
    msg_len = str(len(data))
    pack_header = '{:<{}}'.format(msg_len, HEADERSIZE)
    return bytes(pack_header, 'utf-8')+data

def main(argv, defaultHost):
    '''Start a server for Tanks and handle client connections'''
    # Default Host options for local play #
    if defaultHost:
        HOST = '127.0.0.1'
    else:
        HOST = input('SERVER IP:')
    PORT = 47477
    
    # INIT CONDITIONS #
    player1 = Player_pos(pos = P1_START, direct = UDLR.up)
    player2 = Player_pos(pos = P2_START, direct = UDLR.up)
    players = [player1, player2]
    state = State(players)
    sample_msg = Memory(player1, new_missiles = [], game_over = False, p_won = False)

    # CONNECTION SETUP W/ SOCKETS #
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print("Setup Server at IP:", HOST)
    
    # SETUP FOR UNBLOCKED CONNECTIONS #
    connections = [server]
    writes = []
    broken = []
    player_num = 0
    counter = 0

    # SERVER LOOP #
    while True:
        try:
            # BLOCKING SOCKET CALL #
            read_socks, write_socks, error_socks = select.select(connections, writes, broken)
            
            # ALL CLIENTS CONNECTED #
            if len(connections) == 3:
                # BEGIN GAME #
                try:
                    for sock in read_socks:
                        if sock != server:
                            # GET MESSAGE #
                            header, data = getData(sock)

                            # CLIENT DISCONNECT #
                            if header == -1:
                                connections.remove(sock)
                                continue

                            ### MAKE MESSAGE CHANGES/DATA UPDATES HERE ###
                            player_data = pickle.loads(data)
                            #print(player_data)
                            # Notes:
                                #Each tank should send ONLY their own info
                                #Prevents one tank from updating another tank's position
                            if sock == connections[1]:
                                #update from player1
                                state.ps[0] = player_data.p
                                state.missiles[0] = player_data.missiles
                                state.game_over = player_data.end
                                state.ps_ready[0] = player_data.ready
                            elif sock == connections[2]:
                                #update from player2
                                state.ps[1] = player_data.p
                                state.missiles[1]= player_data.missiles
                                state.game_over = player_data.end
                                state.ps_ready[1] = player_data.ready
                            else:
                                print("Uh oh, that's not right..")
                                exit() 
                            #print("Sending Data")

                            # CLIENT SENDING INFORMATION #
                            for client in connections:
                                if client != server and client != sock: 
                                    update = pickle.dumps(state)
                                    update = add_header(update)
                                    client.sendall(update)

                # SOCKET COMMUNICATION BROKE #
                except Exception:
                    for conn in connections:
                        conn.close()
            # WAITING ON CLIENT CONNETIONS #
            else: 
                for sock in read_socks:
                    # CLIENT RE-CONNECTING #
                    if sock != server and sock in connections:
                        connections.remove(sock)
                        counter -= 1

                    # HANDLE NEW CONNECTION #
                    if sock == server:
                        new_conn, new_addr = server.accept()
                        connections.append(new_conn)
                        print("Number of Connections:", len(connections))
                        print("Connected user from ip:{}".format(new_addr))
                        counter += 1
                        data = str(counter).encode()
                        new_conn.sendall(data)
        # ERROR WHEN LISTENING #
        except Exception as e:
            print("Uh oh! Ran into Exception [", str(e), "] while running.")            
            print("Shutting down...")
            exit(1)


if __name__ == '__main__':
    defaultHost = False
    for arg in sys.argv[1:]:
        if arg == '-o':
            defaultHost = True

    main(sys.argv[1:], defaultHost)
