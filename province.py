import itertools
import json

import calculations
from terraintype import TerrainType
import pygame as p
from typing import Union


class Province:

    BORDER_THICKNESS = 4
    HIGHLIGHT_COLOR = p.Color("yellow")
    TERRAIN_COLOR = {
        TerrainType.FLAT: p.Color("darkseagreen"),
        TerrainType.HILLS: p.Color("wheat"),
        TerrainType.MOUNTAIN: p.Color("burlywood4"),
        TerrainType.OCEAN: p.Color("cadetblue4"),
        TerrainType.SEA: p.Color("cadetblue3")
    }

    def __init__(self, province_id):
        self.id: int = province_id
        self.name: Union[str, None] = None
        self.border: [int] = None
        self.center_pos = None
        self.terrain: Union[TerrainType, None] = None
        self.temperature: Union[int, None] = None
        self.neighbours: [int] = []

        self.is_selected = False

        self.development = 1

    def __eq__(self, other):
        if not isinstance(other, Province):
            return False

        return self.id == other.id and self.name == other.name

    def set_name(self, name):
        self.name = name
        try:
            with open('resources/province_data.json', "r") as data_file:
                data = json.load(data_file)

            for province in data["provinces"]:
                if province["id"] == self.id:
                    province["name"] = name
                    break

            with open('resources/province_data.json', "w") as data_file:
                json.dump(data, data_file, indent=2)
        except Exception as e:
            print(f"Setting name ({name}) to province to json file failed! {e}")

    def set_center(self, pos, node_dict):
        if pos is None:
            pos = calculations.calculate_center([node_dict[id].pos for id in self.border])
            self.center_pos = (int(pos[0]), int(pos[1]))
            try:
                with open('resources/province_data.json', "r") as data_file:
                    data = json.load(data_file)

                c_x, c_y = self.center_pos
                for province in data["provinces"]:
                    if province["id"] == self.id:
                        province["center"] = (c_x, c_y)
                        break

                with open('resources/province_data.json', "w") as data_file:
                    json.dump(data, data_file, indent=2)
            except Exception as e:
                print(f"Setting center pos to province to json file failed! {e}")
        else:
            self.center_pos = pos

    def set_border(self, border, node_dict):
        self.border = border
        self.set_center(None, node_dict)
        self.temperature = self.calculate_temp()

    def set_terrain(self, terrain: TerrainType):
        self.terrain = terrain
        try:
            with open('resources/province_data.json', "r") as data_file:
                data = json.load(data_file)

            for province in data["provinces"]:
                if province["id"] == self.id:
                    province["terrain"] = terrain.to_string()
                    break

            with open('resources/province_data.json', "w") as data_file:
                json.dump(data, data_file, indent=2)
        except Exception as e:
            print(f"Setting terrain to province to json file failed! {e}")

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

    def point_inside_province(self, pos, node_dict) -> bool:
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

    def set_random_dev(self):
        # TODO: random development
        pass

    def calculate_temp(self):
        # TODO: calculate average temp based on vertical position of the center coord lerping between like -20 to 40
        return 15

    def draw(self, screen, node_dict, province_dict):
        self.draw_borders(screen, node_dict)
        # self.draw_neighbour_connections(screen, province_dict)
        self.draw_name(screen)

    def draw_name(self, screen):
        text_size = 18
        font = p.font.Font('freesansbold.ttf', text_size)
        text = font.render(self.name, False, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = self.center_pos
        screen.blit(text, text_rect)

    def draw_borders(self, screen, node_dict):
        if self.is_selected:
            color = self.HIGHLIGHT_COLOR
        else:
            color = self.TERRAIN_COLOR[self.terrain]

        p.draw.polygon(screen, color, [node_dict[node_id].pos for node_id in self.border])

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

    def is_passable(self):
        # TODO: implement impassable terrain?
        return True

    def cost_to_enter(self, cost_so_far: int, source_terrain: TerrainType, unit):
        cost = unit.cost_to_enter_province(self, cost_so_far)

        embarking_penalty = 100  # 10 Days with base move regen
        if ((source_terrain.is_water() and not self.terrain.is_water()) or
                (not source_terrain.is_water() and self.terrain.is_water())):
            cost += embarking_penalty

        print(f"Cost to enter this province ({self.name}): {cost}")
        return cost

    def base_cost_to_enter(self):
        return 1 / self.terrain.get_movement_speed()

    def get_neighbours(self) -> [int]:
        return self.neighbours





