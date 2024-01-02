import json

from terraintype import TerrainType
import pygame as p
from typing import Union


class Province:

    BORDER_THICKNESS = 4

    def __init__(self, province_id):
        self.id: int = province_id
        self.name: Union[str, None] = None
        self.border: [int] = None
        self.center_pos = None
        self.terrain: Union[TerrainType, None] = None
        self.temperature: Union[int, None] = None
        self.neighbours: [int] = []

    def set_name(self, name):
        self.name = name

    def set_border(self, border, node_dict):
        self.border = border
        self.center_pos = self.calculate_center(node_dict)
        self.temperature = self.calculate_temp()

    def set_terrain(self, terrain: TerrainType):
        self.terrain = terrain

    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def add_neighbour(self, neighbour_id):
        self.neighbours.append(neighbour_id)
        try:
            with open('resources/province_data.json', "r") as data_file:
                data = json.load(data_file)

            for province in data["provinces"]:
                if province["id"] == self.id:
                    province["neighbours"].append(neighbour_id)
                    break

            with open('resources/province_data.json', "w") as data_file:
                json.dump(data, data_file, indent=2)
        except Exception as e:
            print(f"Adding neighbour to province to json file failed! {e}")

    def is_clicked(self, pos, node_dict) -> bool:
        x = pos[0]
        y = pos[1]
        n = len(self.border)
        inside = False

        p1x, p1y = node_dict[self.border[0]].pos
        for i in range(n + 1):
            p2x, p2y = node_dict[self.border[i % n]].pos
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= x_inters:
                                inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def calculate_center(self, node_dict):
        # TODO: calculate center
        # idea 1: average all nodes' coordinates
        x = 0
        y = 0
        for node_id in self.border:
            x += node_dict[node_id].pos[0]
            y += node_dict[node_id].pos[1]

        return (x // len(self.border), y // len(self.border))

    def calculate_temp(self):
        # TODO: calculate average temp based on vertical position of the center coord lerping between like -20 to 40
        return 15

    def draw(self, screen, node_dict, province_dict):
        self.draw_name(screen)
        self.draw_borders(screen, node_dict)
        # self.draw_neighbour_connections(screen, province_dict)

    def draw_name(self, screen):
        text_size = 18
        font = p.font.Font('freesansbold.ttf', text_size)
        text = font.render(self.name, False, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = self.center_pos
        screen.blit(text, text_rect)

    def draw_borders(self, screen, node_dict):
        for i in range(len(self.border)):
            pos_1 = node_dict[self.border[i]].pos
            if i == len(self.border) - 1:
                pos_2 = node_dict[self.border[0]].pos
            else:
                pos_2 = node_dict[self.border[i + 1]].pos
            p.draw.line(screen, p.Color("black"), pos_1, pos_2, self.BORDER_THICKNESS)

    def draw_neighbour_connections(self, screen, province_dict):
        pos_a = self.center_pos
        for neighbour_id in self.neighbours:
            pos_b = province_dict[neighbour_id].center_pos
            p.draw.line(screen, p.Color("pink"), pos_a, pos_b, self.BORDER_THICKNESS)



