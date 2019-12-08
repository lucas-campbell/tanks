#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# 11/5/19
# Memory.py Class Definition
##########################
from Arena import *
import pickle
from Sprites import UDLR
from enum import Enum

class Player_pos:
	def __init__(self, pos, direct):
		self.position = pos
		self.direction = direct  

class State:
    def __init__(self, _players, _missiles = [[],[]], _game_over = False, _player_won = 1, _ps_ready = [False, False]):
        self.ps = _players
        self.missiles = _missiles
        self.game_over = _game_over
        self.player_won = _player_won
        self.ps_ready = _ps_ready

class Memory:
	def __init__(self, player, new_missiles = [], game_over = False, p_won = False, _ready = False):
            self.p = player
            self.end = game_over
            self.player_won = p_won
            self.missiles = new_missiles
            self.ready = _ready
