import json
import random
import string
import pygame as p
from node import Node
from province import Province
from terraintype import TerrainType
from typing import Union


class State:
    def __init__(self):
        self.border_nodes: {int: Node} = {}
        self.provinces: {int: Province} = {}
        self.selected_province: Union[int, None] = None
        self.parse_data()

    def update(self, screen, ref_image, delta_time):
        # screen.fill(p.Color("black"))
        screen.blit(ref_image, (0, 0))

        for province_id, province in self.provinces.items():
            if province_id == self.selected_province:
                province.is_selected = True
                province.draw(screen, self.border_nodes, self.provinces)
            else:
                province.is_selected = False

        # self.display_nodes(screen)

        self.show_fps(screen, delta_time)

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
            print(province_data)
            pro_id = province_data['id']
            pro_name = province_data['name']
            pro_border = province_data['border']
            pro_terrain = province_data['terrain']
            terrain = TerrainType.get_terrain(pro_terrain)
            pro_neighbours = province_data['neighbours']

            province = Province(pro_id)
            province.set_name(pro_name)
            province.set_border(pro_border, self.border_nodes)
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
                "neighbours": []
            })

            with open('resources/province_data.json', "w") as data_file:
                json.dump(data, data_file, indent=2)
        except Exception as e:
            print(f"Adding province {new_province.name} to json file failed! {e}")

    def get_node_clicked(self, pos):
        # TODO: Optimize into quadrants?
        for node in self.border_nodes.values():
            if node.is_clicked(pos):
                return node
        return None

    def get_province_clicked(self, pos):
        # TODO: Optimize this somehow?
        for pro in self.provinces.values():
            if pro.is_clicked(pos, self.border_nodes):
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


