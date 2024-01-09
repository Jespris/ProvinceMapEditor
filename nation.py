import random
import male_names
from log_handler import log_message
from mapmodes import MapMode
from person import Person
from army import Army
from ui import TextBox, Circle_UI_Element, UI_Table
import pygame as p


class Nation:
    def __init__(self, name: str, capital: int):
        self.name: str = name
        self.name_text_box: TextBox = TextBox((0, 0), (1, 1), f"{self.name} TextBox", 24, bold=True, box_thickness=0, transparent=True)
        self.capital_icon: Circle_UI_Element = Circle_UI_Element((0, 0), 12, f"{self.name} Capital")
        self.nation_stats_table: UI_Table = None
        self.is_clicked = False
        self.capital: int = capital  # province id
        self.provinces: [int] = [self.capital]  # list of province IDs
        self.total_dev = 0
        self.at_war_with: [] = []  # list of other nations
        self.alliances: [] = []  # list of other nations
        self.color = self.get_random_color()
        self.armies: [Army] = []
        self.king: Person = None
        self.get_new_king()
        self.create_table()
        self.civil_war_risk = 0

    def update_nation_ui_elements(self, province_dict, node_dict):
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

        self.capital_icon.color = p.Color("gold")
        pos = province_dict[self.capital].center_pos
        self.capital_icon.x = pos[0]
        self.capital_icon.y = pos[1]

    def draw(self, screen, map_mode, node_dict, province_dict):
        if map_mode == MapMode.POLITICAL:
            self.capital_icon.draw(screen)
            self.name_text_box.draw(screen)
            if self.is_clicked:
                # display the nation stats
                self.nation_stats_table.draw(screen)
                # draw the provinces green, alliance nations blue and war enemies red, all other provinces white
                for key, value in province_dict.items():
                    if key in self.provinces:
                        continue
                    elif key in [ally.provinces for ally in self.alliances]:
                        value.draw(screen, node_dict, map_mode, True, is_ally=True)
                    elif key in [enemy.provinces for enemy in self.at_war_with]:
                        value.draw(screen, node_dict, map_mode, True, is_enemy=True)
                    else:
                        value.draw(screen, node_dict, map_mode, True, is_ally=True, is_enemy=True)

    def add_province(self, province_id: int):
        self.provinces.append(province_id)

    def daily_update(self):
        pass

    def monthly_update(self, province_dict):
        if self.civil_war_risk > 0:
            self.civil_war_risk -= 1
        self.king.monthly_update()
        if self.king.is_dead:
            self.get_new_king()
            if len(self.provinces) > 1:
                self.civil_war_risk += random.randint(0, 10) + abs(self.king.diplo_power - 10)
            log_message(f"{self.king.name} ({self.king.admin_power}, {self.king.diplo_power}, {self.king.mil_power}) took the throne at age {self.king.age}")

        self.update_king_info()
        self.develop_nation(province_dict)
        self.calculate_total_dev(province_dict)

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
        self.king = Person(f"King {name} 'the {personality}' of {self.name}", random.randint(0, 50))

    def develop_nation(self, province_dict):
        development_rate = 70  # higher number -> less development
        if random.randint(0, development_rate) - self.king.admin_power == 0:
            provinces = [province_dict[p_id] for p_id in self.provinces]
            random.shuffle(provinces)
            chosen_province = provinces[0]
            while chosen_province.development >= 10 and len(provinces) > 1:  # one province nations cannot increase above 10
                random.shuffle(provinces)
                chosen_province = provinces[0]
            if chosen_province.development < 10:
                chosen_province.increase_development()
            # log_message(f"{chosen_province.name} increased development to {chosen_province.development}!")

    def create_table(self):
        from main import WIDTH
        table_width = WIDTH
        table_height = 50

        table_texts = {0: self.name,
                       1: f"{self.king.name} ({self.king.age})",
                       2: f"Admin {self.king.admin_power}, Diplo {self.king.diplo_power}, Mil {self.king.mil_power}",
                       3: f"Total development: {self.total_dev}"}

        ui_table = UI_Table((0, 0), (table_width, table_height), f"NationTable", 1, len(table_texts))
        ps = (0, 0)
        for key, value in table_texts.items():
            # positions and sizes automatically get set by table
            ui_element = TextBox(ps, ps, f"Attribute {key}", 20, bold=False)
            ui_element.set_text([value])

            ui_table.set_table_element(0, key, ui_element)

        self.nation_stats_table = ui_table

    def calculate_total_dev(self, province_dict):
        total = 0
        for p_id in self.provinces:
            total += province_dict[p_id].development

        self.total_dev = total
        if self.nation_stats_table is not None:
            text_box = self.nation_stats_table.get_table_element_by_name("Attribute 3")
            assert isinstance(text_box, TextBox)
            text_box.set_text([f"Total development: {self.total_dev}"])

    def update_king_info(self):
        if self.nation_stats_table is not None:
            text_box = self.nation_stats_table.get_table_element_by_name("Attribute 1")
            assert isinstance(text_box, TextBox)
            text_box.set_text([f"{self.king.name} ({self.king.age})"])

            text_box = self.nation_stats_table.get_table_element_by_name("Attribute 2")
            assert isinstance(text_box, TextBox)
            text_box.set_text([f"Admin {self.king.admin_power}, Diplo {self.king.diplo_power}, Mil {self.king.mil_power}"])



