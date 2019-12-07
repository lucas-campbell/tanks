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
	def __init__(self, pos, direct)
	self.position = pos
	self.direction = direct  

class State:
    __init__(self, _player1, _player2, _p1_missiles = [], _p2_missiles = [] _game_over = False):
        self.player1 = _player1 
        self.player2 = _player2
        self.p1_missiles = _p1_missiles
        self.p2_missiles = _p2_missiles
        self.game_over = _game_over

class Memory:
	def __init__(self, player, new_missiles = None, game_over = False, p_won = False):
		self.p = player
		self.end = game_over
		self.player_won = p_won
		self.missiles = new_missiles
