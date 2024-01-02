import pygame as p
from win32api import GetSystemMetrics

from gamestate import State
from testing import test_set

# GLOBALS
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
FPS = 30


def save_screen():
    pass


def main():
    print("Hello!")
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Province Map Editor")
    image = load_ref_image()
    state = State()
    clock = p.time.Clock()
    delta_time = 0

    nodes_clicked = []
    editing_province = False
    creating_neighbours = False
    first_nei = None

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
                if e.key == p.K_p and not editing_province:
                    print("Editing new province...")
                    nodes_clicked = []
                    editing_province = True
                if e.key == p.K_o and editing_province:
                    print("Finishing new province!")
                    if nodes_clicked is None:
                        # nothing should happen
                        continue
                    else:
                        state.create_new_province(nodes_clicked)
                    editing_province = False
                    nodes_clicked = []
                if e.key == p.K_l:
                    print("Creating neighbours...")
                    creating_neighbours = True
                    first_nei = None

            elif e.type == p.KEYUP:
                pass

            elif e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if state.selected_province is not None:
                    # check if edit buttons are pressed
                    if state.get_button_pressed(pos):
                        continue

                province = state.get_province_clicked(pos)
                if editing_province:
                    node = state.get_node_clicked(pos)
                    if node is not None:
                        nodes_clicked.append(node.id)
                elif creating_neighbours:
                    if first_nei is not None and province is not None:
                        state.create_neighbour_pair(first_nei, province)
                        first_nei = None
                        creating_neighbours = False
                    elif province is not None:
                        first_nei = province
                if province is not None:
                    if state.selected_province is not None and state.selected_province == province.id:
                        state.selected_province = None
                    else:
                        state.selected_province = province.id

            elif e.type == p.MOUSEBUTTONUP:
                pass

            elif e.type == p.QUIT:
                running = False

        # update
        clock.tick(FPS)
        state.update(screen, image, delta_time)
        delta_time = clock.get_rawtime()
        p.display.flip()

    p.image.save(screen, 'output/CreatedGame.png')

    print("Goodbye!")


def load_ref_image():
    return p.transform.scale(p.image.load('resources/StaticMapImage.png'), (WIDTH, HEIGHT))


if __name__ == "__main__":
    main()
    # test_set()
