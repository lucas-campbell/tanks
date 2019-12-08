from pygame import Rect
from constants import *

ul_square = Rect((7/32)*WIDTH, (7/32)*HEIGHT, HEIGHT/16 + 10, WIDTH/16 + 10)
ur_square = Rect((23/32)*WIDTH, (7/32)*HEIGHT, HEIGHT/16 + 10, WIDTH/16 + 10)
ll_square = Rect((7/32)*WIDTH, (23/32)*HEIGHT, HEIGHT/16 + 10, WIDTH/16 + 10)
lr_square = Rect((23/32)*WIDTH, (23/32)*HEIGHT, HEIGHT/16 + 10, WIDTH/16 + 10)

map1 = [ul_square, ur_square, ll_square, lr_square]
