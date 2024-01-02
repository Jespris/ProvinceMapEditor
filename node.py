import pygame as p


class Node:

    RADIUS = 10

    def __init__(self, id, pos):
        self.id = id
        self.pos = pos

    def draw(self, screen):
        p.draw.circle(screen, p.Color("black"), self.pos, self.RADIUS)
