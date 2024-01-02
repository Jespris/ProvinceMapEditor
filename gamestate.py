import json

import pygame as p

from node import Node


class State:

    show_nodes = True

    def __init__(self):
        self.border_nodes: [Node] = []
        self.parse_data()

    def update(self, screen, ref_image):
        screen.fill(p.Color("black"))
        screen.blit(ref_image, (0, 0))
        if self.show_nodes:
            self.display_nodes(screen)

    def display_nodes(self, screen):
        for node in self.border_nodes:
            node.draw(screen)

    def parse_data(self):
        data_file = open('resources/province_data.json', "r")

        data = json.loads(data_file.read())

        print(f"Number of border nodes: {len(data['nodes'])}")
        for node_data in data['nodes']:
            print(node_data)
            node_id = node_data['id']
            node_pos = node_data['pos']
            node = Node(node_id, tuple(node_pos))
            self.border_nodes.append(node)

    def add_node(self, node: Node):
        try:
            self.border_nodes.append(node)
            # add to json file
            with open('resources/province_data.json', "r") as data_file:
                data = json.load(data_file)

            data['nodes'].append({"id": node.id, "pos": list(node.pos)})

            with open('resources/province_data.json', "w") as data_file:
                json.dump(data, data_file)
        except Exception as e:
            print(f"Adding node {node.id}:{node.pos} to json file failed! {e}")

    def create_node(self, pos):
        new_id = len(self.border_nodes)
        node = Node(new_id, pos)
        self.add_node(node)
