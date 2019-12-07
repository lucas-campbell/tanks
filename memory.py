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
    __init__(self, _player1, _player2, _missles = [], _game_over = False):
        self.player1 = _player1 
        self.player2 = _player2
        self.missles = _missles
        self.game_over = _game_over

class Memory:
	def __init__(self, player1, new_missles = None, game_over = False, p_won = False):

		self.p1 = player1
		self.end = game_over
		self.player_won = p_won
		self.missles = new_missles
