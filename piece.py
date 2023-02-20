import pygame as pg

class Piece:
    def __init__(self, center, starting_color):
        self.center = center
        self.color = starting_color
        # will add later
        self.image = None
    
    def flip(self):
        self.color = (255, 255, 255) if self.color == (0, 0, 0) else (0, 0, 0)