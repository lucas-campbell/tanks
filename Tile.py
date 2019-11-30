"""
Tile.py: a simple class to represent a Tile on the game map
"""
from pygame import Rect

# Imports go here

class Tile:
    def __init__(self, x_coord, y_coord, _width=40, _height=40, _is_obst=False):
        self.rect = Rect((x_coord, y_coord), (_width, _height))
        self.x = x_coord
        self.y = y_coord
        self.width = _width
        self.height = _height
        self.is_obstacle = _is_obst
