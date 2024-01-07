import random

import male_names
from mapmodes import MapMode
from person import Person
from army import Army
from ui import TextBox


class Nation:
    def __init__(self, name: str, capital: int):
        self.name: str = name
        self.name_text_box = TextBox((0, 0), (0, 0), f"{self.name} TextBox", 34, bold=True, box_thickness=0, transparent=True)
        self.capital: int = capital  # province id
        self.provinces: [int] = [self.capital]  # list of province IDs
        self.at_war_with: [] = []  # list of other nations
        self.alliances: [] = []  # list of other nations
        self.color = self.get_random_color()
        self.armies: [Army] = []
        self.king: Person = self.get_new_king()

    def update_name_text_box(self, province_dict, node_dict):
        # get the average position of all nodes in the nation and blit the name there
        pos = self.calculate_center(province_dict, node_dict)
        # default textbox size for all nations:
        size = (200, 50)

        self.name_text_box.x = pos[0] - size[0] // 2
        self.name_text_box.y = pos[1] - size[1] // 2
        self.name_text_box.width = size[0]
        self.name_text_box.height = size[1]

        # update the text
        self.name_text_box.set_text([self.name])

        pass

    def draw(self, screen, map_mode):
        if map_mode == MapMode.POLITICAL:
            self.name_text_box.draw(screen)

    def add_province(self, province_id: int):
        self.provinces.append(province_id)

    def daily_update(self):
        pass

    def monthly_update(self):
        self.king.monthly_update()
        if self.king.is_dead:
            self.king = self.get_new_king()

    def spawn_army(self):
        pass

    @staticmethod
    def get_random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

    def calculate_center(self, province_dict, node_dict):
        x = 0
        y = 0
        total_nodes = 0
        for province in [province_dict[p_id] for p_id in self.provinces]:
            for node in [node_dict[n_id] for n_id in province.border]:
                total_nodes += 1
                x += node.pos[0]
                y += node.pos[1]

        return x // total_nodes, y // total_nodes

    def get_new_king(self):
        name = male_names.get_random()
        personality = male_names.get_personality()
        return Person(f"King {name} 'the {personality}' of {self.name}", random.randint(0, 50))

