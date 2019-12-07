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

#pos is a tuple representing x,y coordinates 
#direction is an integer that represents degrees like 0, 90, 180, 270
class Player_pos:
	def __init__(self, pos, direct)
	self.position = pos
	self.direction = direct  

#reperesents server state
class State:
    __init__(self, _player1, _player2, _p1_missles = [], _p2_missles = [] _game_over = False):
        self.player1 = _player1 
        self.player2 = _player2
        self.p1_missles = _p1_missles
        self.p2_missles = _p2_missles
        self.game_over = _game_over

#removed player 2	
class Memory:
	def __init__(self, player, new_missles = None, game_over = False, p_won = False):
		self.p = player
		self.end = game_over
		self.player_won = p_won
		self.missles = new_missles
