#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# 11/5/19
# Memory.py Class Definition
##########################
From Arena import *
import pickle
from Sprites import UDLR
from enum import Enum

class Player_pos:
	def __init__(self, pos, direct)
	self.position = pos
	self.direction = direct  


class Memory:
	def __init__(self, player1, player2, new_missles = None, game_over = False, p_won = False):

		self.p1 = player1
		self.p2 = player2
		self.end = game_over
		self.player_won = p_won
		self.missles = new_missles
