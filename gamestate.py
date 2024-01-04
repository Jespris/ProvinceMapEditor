import json
import math
import random
import string
import pygame as p

from button import EditProvinceButton, NameButton, TerrainButton
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


class State:
    def __init__(self):
        self.border_nodes: {int: Node} = {}
        self.provinces: {int: Province} = {}
        self.selected_province: Union[int, None] = None
        self.buttons: [EditProvinceButton] = create_buttons()
        self.day = 0
        self.lapsed_ms = 0
        self.units: [Unit] = []
        self.is_paused = False
        self.parse_data()

    def update(self, screen, ref_image, delta_time):
        if not self.is_paused:
            self.update_in_game_time(delta_time)
        # screen.fill(p.Color("black"))
        screen.blit(ref_image, (0, 0))

        for province_id, province in self.provinces.items():
            if province_id == self.selected_province:
                province.is_selected = True
                province.draw(screen, self.border_nodes, self.provinces)
            else:
                province.is_selected = False
            # province.draw(screen, self.border_nodes, self.provinces)

        for unit in self.units:
            unit.draw(screen, self.selected_province)

        # self.display_nodes(screen)
        if self.selected_province is not None:
            self.show_edit_province_buttons(screen)

        self.show_fps(screen, delta_time)

    def create_unit(self, name, province) -> Unit:
        unit = Unit(name, province)
        self.units.append(unit)
        return unit

    def display_nodes(self, screen):
        for node in self.border_nodes.values():
            node.draw(screen)

    def parse_data(self):
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
            province.set_name(pro_name)
            province.set_border(pro_border, self.border_nodes)
            province.set_center(pro_center, self.border_nodes)
            province.set_terrain(terrain)
            province.set_neighbours(pro_neighbours)
            self.provinces[province.id] = province
        print("Parsing complete!")

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

    def create_neighbour_pair(self, a: Province, b: Province):
        a.add_neighbour(b.id)
        b.add_neighbour(a.id)

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

    def get_random_province(self):
        # TODO: implement!
        return self.provinces[0]  # hopefully this always exists

    def get_province(self, province_id):
        return self.provinces[province_id]

    def update_in_game_time(self, delta_time):
        self.lapsed_ms += delta_time
        ms_per_day = 1000  # 1s per day
        if self.lapsed_ms > ms_per_day:
            self.day += 1
            self.update_day()
            self.lapsed_ms -= ms_per_day

    def update_day(self):
        for unit in self.units:
            unit.daily_update()


