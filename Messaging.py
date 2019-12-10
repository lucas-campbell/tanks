#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# 11/5/19
# Memory.py class Definition
##########################
import pickle
from Sprites import UDLR
from enum import Enum

class Player_pos:
    '''For tracking player position and direction'''
    def __init__(self, pos, direct):
        self.position = pos
        self.direction = direct  

class State:
    '''Representation of the current state in the game'''
    def __init__(self, _players, _missiles = [[],[]], _game_over = False,
                 _player_won = 1, _ps_ready = [False, False]):
        self.ps = _players
        self.missiles = _missiles
        self.game_over = _game_over
        self.player_won = _player_won
        self.ps_ready = _ps_ready

class Memory:
    '''Information for a single client to send to the server on update'''
    def __init__(self, player, new_missiles = [], game_over = False,
                 p_won = False, _ready = False):
        self.p = player
        self.end = game_over
        self.player_won = p_won
        self.missiles = new_missiles
        self.ready = _ready
