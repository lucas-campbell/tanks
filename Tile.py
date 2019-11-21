"""
Tile.py: a simple class to represent a Tile on the game map
"""
from pygame import Rect

# Imports go here

class Tile:
    def __init__(self, x_coord, y_coord, width=40, height=40, is_obst=False):
        self.rect = Rect((x_coord, y_coord), (width, height))
        self.is_obstacle = is_obst
