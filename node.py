import pygame as p


class Node:

    RADIUS = 10

    def __init__(self, id, pos):
        self.id = id
        self.pos = pos

    def draw(self, screen):
        p.draw.circle(screen, p.Color("black"), self.pos, self.RADIUS)

    def is_clicked(self, pos):
        return (self.pos[0] - self.RADIUS <= pos[0] <= self.pos[0] + self.RADIUS and
                self.pos[1] - self.RADIUS <= pos[1] <= self.pos[1] + self.RADIUS)
