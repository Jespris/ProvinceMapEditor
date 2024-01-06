import json
import math
import random
import string
import pygame as p

from button import EditProvinceButton, NameButton, TerrainButton
from mapmodes import MapMode
from node import Node
from pathFinder import PathSearch
from province import Province
from terraintype import TerrainType
from typing import Union, Optional
from unit import Unit


def create_buttons():
    buttons = []

    name_button = NameButton((20, 20), "Edit name")
    buttons.append(name_button)

    ocean_button = TerrainButton((140, 20), "Ocean", TerrainType.OCEAN)
    buttons.append(ocean_button)

    sea_button = TerrainButton((260, 20), "Sea", TerrainType.SEA)
    buttons.append(sea_button)

    flat_button = TerrainButton((380, 20), "Flat", TerrainType.FLAT)
    buttons.append(flat_button)

    hills_button = TerrainButton((500, 20), "Hills", TerrainType.HILLS)
    buttons.append(hills_button)

    mountain_button = TerrainButton((620, 20), "Mountain", TerrainType.MOUNTAIN)
    buttons.append(mountain_button)

    return buttons


class GameState:
    def __init__(self):
        # Initialize game state attributes
        self.border_nodes: {int: Node} = {}
        self.provinces: {int: Province} = {}
        self.selected_province: Union[int, None] = None
        self.buttons: [EditProvinceButton] = create_buttons()
        self.day = 0
        self.lapsed_ms = 0
        self.game_speed = 1  # TODO: implement game speed
        self.units: [Unit] = []
        self.is_paused = False
        self.map_mode: MapMode = MapMode.TERRAIN
        self.hide_names = True
        self.developer_mode = False

        self.parse_data()

    # region Game state updaters
    def update(self, screen, ref_image, delta_time):
        # Main update function for the game state
        if not self.is_paused:
            self.update_in_game_time(delta_time)

        screen.fill(p.Color("black"))
        if self.map_mode == MapMode.TERRAIN:
            screen.blit(ref_image, (0, 0))

        selected_province = None
        for province_id, province in self.provinces.items():
            if province_id == self.selected_province:
                province.is_selected = True
                selected_province = province
            else:
                province.is_selected = False
            if self.map_mode != MapMode.TERRAIN:
                province.draw(screen, self.border_nodes, self.map_mode, self.hide_names)

        if selected_province is not None:
            selected_province.draw(screen, self.border_nodes, self.map_mode, self.hide_names)

        for unit in self.units:
            unit.draw(screen, self.selected_province)

        # self.display_nodes(screen)
        if self.developer_mode:
            if self.selected_province is not None:
                self.show_edit_province_buttons(screen)

            self.show_fps(screen, delta_time)

    def display_nodes(self, screen):
        # Draw all border nodes on the screen
        for node in self.border_nodes.values():
            node.draw(screen)

    def update_in_game_time(self, delta_time):
        self.lapsed_ms += delta_time
        ms_per_day = 1000  # 1s per day
        if self.lapsed_ms > ms_per_day:
            self.day += 1
            self.update_day()
            self.lapsed_ms -= ms_per_day

    def update_day(self):
        # TODO: Update more stuff daily
        for unit in self.units:
            unit.daily_update()

    # endregion

    def parse_data(self):
        # Parse province and node data from a JSON file
        print("Paring data from file...")
        data_file = open('resources/province_data.json', "r")

        data = json.loads(data_file.read())

        print(f"Number of border nodes: {len(data['nodes'])}")
        for node_data in data['nodes']:
            print(node_data)
            node_id = node_data['id']
            node_pos = node_data['pos']
            node = Node(node_id, tuple(node_pos))
            self.border_nodes[node_id] = node

        for province_data in data['provinces']:
            pro_center = None
            print(province_data)
            pro_id = province_data['id']
            pro_name = province_data['name']
            pro_border = province_data['border']
            pro_terrain = province_data['terrain']
            try:
                pro_center = province_data['center']
            except Exception as e:
                print(f"Province has no defined center property, {e}")
            terrain = TerrainType.get_terrain(pro_terrain)
            pro_neighbours = province_data['neighbours']

            province = Province(pro_id)
            province.set_border(pro_border)
            province.set_center(pro_center, self.border_nodes)
            province.set_name(pro_name)
            province.set_terrain(terrain)
            province.set_neighbours(pro_neighbours)
            province.set_random_dev()
            self.provinces[province.id] = province
        print("Parsing complete!")

    def set_map_mode(self, i: int):
        if i == 1:
            self.map_mode = MapMode.TERRAIN
        elif i == 2:
            self.map_mode = MapMode.DEVELOPMENT
        elif i == 2:
            self.map_mode = MapMode.POLITICAL

    # region 'create' functions
    def add_node(self, node: Node):
        self.border_nodes[node.id] = node
        try:
            # add to json file
            with open('resources/province_data.json', "r") as data_file:
                data = json.load(data_file)

            data['nodes'].append({"id": node.id, "pos": list(node.pos)})

            with open('resources/province_data.json', "w") as data_file:
                json.dump(data, data_file, indent=2)
        except Exception as e:
            print(f"Adding node {node.id}:{node.pos} to json file failed! {e}")

    def create_unit(self, name, province) -> Unit:
        unit = Unit(name, province)
        self.units.append(unit)
        return unit

    def create_node(self, pos):
        new_id = len(self.border_nodes)
        node = Node(new_id, pos)
        self.add_node(node)

    def create_new_province(self, nodes_id):
        new_province = Province(len(self.provinces))
        new_province.set_name(self.generate_random_name())
        new_province.set_border(nodes_id, self.border_nodes)
        new_province.set_center(None, self.border_nodes)

        self.provinces[new_province.id] = new_province
        try:
            # add to json file
            with open('resources/province_data.json', "r") as data_file:
                data = json.load(data_file)

            data['provinces'].append({
                "id": new_province.id,
                "name": new_province.name,
                "border": new_province.border,
                "terrain": "flat",
                "neighbours": [],
                "center": new_province.center_pos
            })

            with open('resources/province_data.json', "w") as data_file:
                json.dump(data, data_file, indent=2)
        except Exception as e:
            print(f"Adding province {new_province.name} to json file failed! {e}")

    def create_neighbour_pair(self, a: Province, b: Province):
        a.add_neighbour(b.id)
        b.add_neighbour(a.id)

    @staticmethod
    def generate_random_name():
        alphabet = list(string.ascii_lowercase)
        length = random.randint(3, 10)
        name = ""
        for i in range(length):
            letter = alphabet[random.randint(0, len(alphabet) - 1)]
            name += letter
        name = name[0].upper() + name[1:]
        return name

    # endregion

    def get_node_clicked(self, pos):
        # TODO: Optimize into quadrants?
        for node in self.border_nodes.values():
            if node.point_inside_province(pos):
                return node
        return None

    def get_province_clicked(self, pos):
        # TODO: Optimize this somehow?
        for pro in self.provinces.values():
            if pro.point_inside_province(pos, self.border_nodes):
                return pro
        return None

    # region display things
    def show_fps(self, screen, delta_time):
        if delta_time != 0:
            font = p.font.Font("freesansbold.ttf", 24)
            text = font.render(f"FPS: {1000 // delta_time}", True, p.Color("red"))
            text_rect = text.get_rect()
            text_rect.topleft = (0, 0)
            screen.blit(text, text_rect)

    def show_edit_province_buttons(self, screen):
        for button in self.buttons:
            button.draw(screen)

    # endregion

    # region All the getters

    def get_button_pressed(self, pos):
        if self.selected_province is not None:  # redundant
            for button in self.buttons:
                if button.is_clicked(pos):
                    button.on_click(self.provinces[self.selected_province])
                    self.selected_province = None
                    return True
        return False

    @staticmethod
    def get_province_distance(province_a: Province, province_b: Province) -> int:
        return int(math.sqrt((province_a.center_pos[0] - province_b.center_pos[0])**2 +
                             (province_a.center_pos[1] - province_b.center_pos[1])**2))

    def get_province_id_distance(self, a: int, b: int) -> int:
        pro_a = self.provinces[a]
        pro_b = self.provinces[b]
        return self.get_province_distance(pro_a, pro_b)

    def get_province_by_name(self, name) -> Optional[Province]:
        for province in self.provinces.values():
            if province.name == name:
                return province
        return None

    def get_random_province(self) -> Union[Province, None]:
        # Get a random province from the available provinces
        if self.provinces:
            random_province_id = random.choice(list(self.provinces.keys()))
            return self.provinces[random_province_id]
        else:
            return None  # Return None if there are no provinces

    def get_province(self, province_id):
        return self.provinces[province_id]

    # endregion

    def set_unit_path(self, unit: Unit, end_id: int):
        end_province = self.provinces[end_id]
        assert isinstance(end_province, Province)
        if end_province.is_passable():
            print(f"Setting path from {unit.current_province.name} to {end_province.name}")
            path_search = PathSearch(self.provinces, unit, unit.current_province.id, end_id, self.get_province_distance)
            path_search.find_path()
            assert path_search.path is not None
            path = [self.get_province(province_id) for province_id in path_search.path]
            unit.path = path






