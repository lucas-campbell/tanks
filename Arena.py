#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# 11/5/19
# Map.py Class Definition
##########################
import socket
import pickle
import sys
from Tile import Tile

class Arena:
##################################
# INIT AND GENERATION
##################################
    def __init__(self, length = 2, obstacleTiles = []):
        self.tiles = []
        self.tank1 = self._defaultGenTank(length)
        self.tank2 = self._defaultGenTank(length, 20, 20)
        self._genArena(obstacleTiles = obstacleTiles)

    ##################################
    # defaultGenTank
    ##################################

    def _defaultGenTank(self, length, startX = 0, startY = 0):
        '''
        Generate a default tank with top-left Tile in location
         startX, startY
        '''
        tankTiles = []
        for x in range(startX, length):
            for y in range(startY, length):
                tankTiles.append(Tile(x,y))
        return tankTiles


    ##################################
    # genArena
    ##################################
    def _genArena(self, length = 25, obstacleTiles = []):
        '''
        Generates a new map with basic Tiles
        '''
        for x in range(0, length):
            for y in range(0, length):
                self.tiles.append(Tile(x,y))
        self._setObstacles(length, obstacleTiles)

    ##################################
    # setObstacles
    ##################################
    def _setObstacles(self, length, obstacleTiles):
        '''
        Sets Obstacles inside a map.
        length = length of one side of a map
        NOTE: Tile order is IMMUTABLE in the list.
        '''
        for t in obstacleTiles:
            if t.x < 0 or t.x >= length or t.y < 0 or t.y >= length:
                raise Exception("Tile out-of-bounds")
            index = t.x*length + t.y
            if t.x != self.tiles[index].x:
                print >> sys.stderr, "Update a Tile incorrectly"
            self.tiles[index].is_obstacle = True

##################################
# UPDATING AND COLLISION
##################################


##################################
# TESTING
##################################
def main(argv):
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                obstacleTiles = [Tile(2,4), Tile(3,3), Tile(0,0), Tile(1,7)]
                testArena = Arena(obstacleTiles = obstacleTiles)
                for t in testArena.tiles:
                    if t.is_obstacle:
                        print(t.x, t.y, t.is_obstacle)

                if not data:
                    break
                    conn.sendall(data)
        
if __name__ == '__main__':
    main(sys.argv[1:])
