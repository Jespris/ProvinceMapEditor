import pygame as p
from win32api import GetSystemMetrics
from gamestate import GameState
from mainstate import MainState

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
    state = GameState()
    main_state = MainState()
    clock = p.time.Clock()
    delta_time = 0

    while main_state.running:
        for event in p.event.get():
            key_input_handler(event, state, main_state)

        # update
        clock.tick(FPS)
        state.update(screen, image, delta_time)
        delta_time = clock.get_rawtime()
        p.display.flip()

    p.image.save(screen, 'output/CreatedGame.png')
    print("Goodbye!")


def key_input_handler(event, state, main_state):
    if event.type == p.KEYDOWN:
        handle_key_down(event, state, main_state)
    elif event.type == p.KEYUP:
        pass
    elif event.type == p.MOUSEBUTTONDOWN:
        handle_mouse_button_down(event, state, main_state)
    elif event.type == p.MOUSEBUTTONUP:
        pass
    elif event.type == p.QUIT:
        main_state.running = False


def handle_key_down(event, state, main_state):
    if event.key == p.K_ESCAPE:
        main_state.running = False
    elif event.key == p.K_n:
        state.create_node(p.mouse.get_pos())
    elif event.key == p.K_p and not main_state.editing_province:
        print("Editing new province...")
        main_state.reset_state()
        main_state.editing_province = True
    elif event.key == p.K_o and main_state.editing_province:
        print("Finishing new province!")
        if main_state.nodes_clicked is None:
            # nothing should happen
            pass
        else:
            state.create_new_province(main_state.nodes_clicked)
        main_state.reset_state()
    elif event.key == p.K_l:
        print("Creating neighbours...")
        main_state.creating_neighbours = True
        main_state.first_nei = None
    elif event.key in (p.K_1, p.K_2, p.K_3):
        state.set_map_mode(int(event.unicode))
    elif event.key == p.K_h:
        state.hide_names = not state.hide_names


def handle_mouse_button_down(event, state, main_state):
    pos = p.mouse.get_pos()
    print(f"Mouse button pressed: {event.button}")
    if state.selected_province is not None:
        if event.button == 1:
            if state.get_button_pressed(pos):
                return
        elif event.button == 3:
            clicked_province = state.get_province_clicked(pos)
            if clicked_province is not None and clicked_province != state.selected_province:
                unit = state.create_unit("Bob", state.get_province(state.selected_province))
                state.set_unit_path(unit, clicked_province.id)

    if event.button == 1:
        province = state.get_province_clicked(pos)
        if main_state.editing_province:
            node = state.get_node_clicked(pos)
            if node is not None:
                main_state.nodes_clicked.append(node.id)
        elif main_state.creating_neighbours:
            if main_state.first_nei is not None and province is not None:
                state.create_neighbour_pair(main_state.first_nei, province)
                main_state.first_nei = None
                main_state.creating_neighbours = False
            elif province is not None:
                main_state.first_nei = province
        if province is not None:
            if state.selected_province is not None and state.selected_province == province.id:
                state.selected_province = None
            else:
                state.selected_province = province.id


def load_ref_image():
    return p.transform.scale(p.image.load('resources/StaticMapImage.png'), (1920, 1080))


if __name__ == "__main__":
    main()
    # test_set()
