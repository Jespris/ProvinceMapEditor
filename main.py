import pygame as p
from win32api import GetSystemMetrics

from gamestate import State
from testing import test_set

# GLOBALS
WIDTH = GetSystemMetrics(0)  # 1920 on PC monitor
HEIGHT = GetSystemMetrics(1)  # 1080
FPS = 30


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
                if e.key == p.K_1:h
                    state.set_map_mode(1)
                if e.key == p.K_2:
                    state.set_map_mode(2)
                if e.key == p.K_3:
                    state.set_map_mode(3)
                if e.key == p.K_h:
                    state.hide_names = not state.hide_names

            elif e.type == p.KEYUP:
                pass

            elif e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                print(f"Mouse button pressed: {e.button}")
                if state.selected_province is not None:
                    # check if edit buttons are pressed
                    if e.button == 1:
                        if state.get_button_pressed(pos):
                            continue
                    if e.button == 3:
                        # right click, we test pathing
                        clicked_province = state.get_province_clicked(pos)
                        if clicked_province is not None and clicked_province != state.selected_province:
                            # right-click on a different province with a province selected
                            unit = state.create_unit("Bob", state.get_province(state.selected_province))
                            state.set_unit_path(unit, clicked_province.id)

                if e.button == 1:  # left click
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
    return p.transform.scale(p.image.load('resources/StaticMapImage.png'), (1920, 1080))


if __name__ == "__main__":
    main()
    # test_set()
