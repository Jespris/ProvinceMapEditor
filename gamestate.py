import pygame as p


class State:
    def __init__(self):
        pass

    def update(self, screen, ref_image):
        screen.fill(p.Color("black"))
        screen.blit(ref_image, (0,0))
