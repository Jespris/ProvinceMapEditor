import pygame as p
from win32api import GetSystemMetrics

from gamestate import State

# GLOBALS
WIDTH = 500  # GetSystemMetrics(0)
HEIGHT = 500  # GetSystemMetrics(1)
FPS = 30


def main():
    print("Hello!")
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Province Map Editor")
    state = State()
    clock = p.time.Clock()

    running = True

    while running:
        for e in p.event.get():

            if e.type == p.KEYDOWN:
                print(e.key)
                if e.key == p.K_ESCAPE:
                    running = False

            elif e.type == p.KEYUP:
                pass

            elif e.type == p.MOUSEBUTTONDOWN:
                pass

            elif e.type == p.QUIT:
                running = False

        # update
        clock.tick(FPS)
        state.update(screen)
        p.display.flip()

    print("Goodbye!")



if __name__ == "__main__":
    main()
