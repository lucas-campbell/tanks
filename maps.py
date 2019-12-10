#!/usr/bin/env python3
##########################
# Cam, Lucas, Omar
# maps.py -- predefined list of objects for a map, can be extended to user's
# liking
##########################
from pygame import Rect
from constants import *

ul_square = Rect((7/32)*WIDTH, (7/32)*HEIGHT, OBST_DIM, OBST_DIM)
ur_square = Rect((23/32)*WIDTH, (7/32)*HEIGHT, OBST_DIM, OBST_DIM)
ll_square = Rect((7/32)*WIDTH, (23/32)*HEIGHT, OBST_DIM, OBST_DIM)
lr_square = Rect((23/32)*WIDTH, (23/32)*HEIGHT, OBST_DIM, OBST_DIM)

map1 = [ul_square, ur_square, ll_square, lr_square]
