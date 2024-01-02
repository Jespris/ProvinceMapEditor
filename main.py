import pygame as p
from win32api import GetSystemMetrics

from gamestate import State
from testing import test_set

# GLOBALS
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
FPS = 30


def main():
    print("Hello!")
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Province Map Editor")
    image = load_ref_image()
    state = State()
    clock = p.time.Clock()

    running = True

    while running:
        for e in p.event.get():

            if e.type == p.KEYDOWN:
                print(e.key)
                if e.key == p.K_ESCAPE:
                    running = False
                if e.key == p.K_n:
                    # new border node
                    state.create_node(p.mouse.get_pos())

            elif e.type == p.KEYUP:
                pass

            elif e.type == p.MOUSEBUTTONDOWN:
                pass

            elif e.type == p.MOUSEBUTTONUP:
                pass

            elif e.type == p.QUIT:
                running = False

        # update
        clock.tick(FPS)
        state.update(screen, image)
        p.display.flip()

    print("Goodbye!")


def load_ref_image():
    return p.transform.scale(p.image.load('resources/Eu4ProvinceMapEurope.png'), (WIDTH, HEIGHT))


if __name__ == "__main__":
    main()
    # test_set()
