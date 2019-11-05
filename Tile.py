"""
Tile.py: a simple class to represent a Tile on the game map
"""

# Imports go here

class Tile:
    def __init__(self, x_coord, y_coord, is_obst=False):
        self.x = x_coord
        self.y = y_coord
        self.is_obstacle = is_obst
