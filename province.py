import json
import random

import calculations
from mapmodes import MapMode
from terraintype import TerrainType
import pygame as p
from typing import Union

from ui import UI_Table, TextBox, TextAlignment


class Province:

    # Constants
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
        # Initialize province attributes
        self.id: int = province_id
        self.name: Union[str, None] = None
        self.border: [int] = None
        self.center_pos = None
        self.terrain: Union[TerrainType, None] = None
        self.temperature: Union[int, None] = None
        self.neighbours: [int] = []
        self.is_selected = False
        self.development = 1
        self.info_ui_table = None
        self.nation = None
        self.occupied_by = None

    def __eq__(self, other):
        # Check if two provinces are equal
        if not isinstance(other, Province):
            return False

        return self.id == other.id and self.name == other.name

    # region Province attribute setters
    def set_name(self, name):
        # Set the name of the province
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

        # update the UI element in the table
        element = self.info_ui_table.get_table_element_by_name("Attribute Province name Value")
        assert isinstance(element, TextBox)
        element.set_text([self.name])  # the table should now be updated?!?

    def set_center(self, pos, node_dict):
        # Set the center position of the province
        if pos is None:
            pos = calculations.calculate_center([node_dict[border_id].pos for border_id in self.border])
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

        self.temperature = self.calculate_temp()
        # ui table needs the center set
        self.create_ui_table()

    def set_border(self, border):
        # Set the border nodes of the province
        self.border = border
        # self.set_center(None, node_dict)

    def set_terrain(self, terrain: TerrainType):
        # Set the terrain type of the province
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

        # update the UI element in the table
        element = self.info_ui_table.get_table_element_by_name("Attribute Terrain Value")
        assert isinstance(element, TextBox)
        element.set_text([self.terrain.to_string()])  # the table should now be updated?!?

    def set_temperature(self, temperature):
        # Set the temperature of the province
        self.temperature = temperature
        # update the UI element in the table
        element = self.info_ui_table.get_table_element_by_name("Attribute Temperature Value")
        assert isinstance(element, TextBox)
        element.set_text([str(self.temperature)])  # the table should now be updated?!?

    def set_neighbours(self, neighbours):
        # Set the neighbouring provinces
        self.neighbours = neighbours

    def set_random_dev(self):
        # Set a random development value for non-water provinces
        if not self.terrain.is_water():
            # Mean around 3, standard deviation determines the spread
            mu = 3
            sigma = 1.5

            # Generate a random number with a normal distribution
            random_number = random.normalvariate(mu, sigma)
            # mountains get a penalty of 2
            if self.terrain == TerrainType.MOUNTAIN:
                random_number -= 2

            # Ensure the number is within the desired range (1-10)
            self.development = max(1, min(10, round(random_number)))

        # update the UI element in the table
        element = self.info_ui_table.get_table_element_by_name("Attribute Development Value")
        assert isinstance(element, TextBox)
        element.set_text([str(self.development)])  # the table should now be updated?!?
    # endregion

    def calculate_temp(self):
        # TODO: Calculate the average temperature based on the vertical position of the center coordinate
        return 15

    def add_neighbour(self, neighbour_id):
        # Add a neighbouring province
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
        # Check if a point is inside the province
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

    # region Province drawing

    def draw(self, screen, node_dict, map_mode, hide_names):
        # Draw the province on the screen
        self.draw_province(screen, node_dict, map_mode)
        if not hide_names:
            self.draw_name(screen)
        if self.is_selected:
            # draw the table
            self.info_ui_table.draw(screen)

    def draw_name(self, screen):
        # Draw the province name on the screen
        text_size = 18
        font = p.font.Font('freesansbold.ttf', text_size)
        text = font.render(self.name, False, p.Color("black"))
        text_rect = text.get_rect()
        text_rect.center = self.center_pos
        screen.blit(text, text_rect)

    def draw_province(self, screen, node_dict, map_mode: MapMode):
        # Draw the province shape on the screen
        color = self.get_color(map_mode)

        p.draw.polygon(screen, color, [node_dict[node_id].pos for node_id in self.border])

        for i in range(len(self.border)):
            pos_1 = node_dict[self.border[i]].pos
            if i == len(self.border) - 1:
                pos_2 = node_dict[self.border[0]].pos
            else:
                pos_2 = node_dict[self.border[i + 1]].pos
            p.draw.line(screen, p.Color("black"), pos_1, pos_2, self.BORDER_THICKNESS)

    def draw_neighbour_connections(self, screen, province_dict):
        # Draw connections to neighbouring provinces
        pos_a = self.center_pos
        for neighbour_id in self.neighbours:
            pos_b = province_dict[neighbour_id].center_pos
            p.draw.line(screen, p.Color("pink"), pos_a, pos_b, self.BORDER_THICKNESS)
    # endregion

    # region Pathing
    def is_passable(self):
        # Check if the province is passable
        # TODO: implement impassable terrain?
        return True

    def cost_to_enter(self, cost_so_far: int, source_terrain: TerrainType, unit):
        # Calculate the cost to enter the province for a unit
        cost = unit.cost_to_enter_province(self, cost_so_far)

        embarking_penalty = 100  # 10 Days with base move regen
        if ((source_terrain.is_water() and not self.terrain.is_water()) or
                (not source_terrain.is_water() and self.terrain.is_water())):
            cost += embarking_penalty

        print(f"Cost to enter this province ({self.name}): {cost}")
        return cost

    def base_cost_to_enter(self):
        # Calculate the base cost to enter the province
        return 1 / self.terrain.get_movement_speed()

    # endregion

    def get_neighbours(self) -> [int]:
        # Get the neighbouring province IDs
        return self.neighbours

    # region Province coloring

    def get_color(self, map_mode: MapMode):
        # Get the color of the province based on the map mode
        if self.is_selected:
            return self.HIGHLIGHT_COLOR

        default = self.TERRAIN_COLOR[self.terrain]

        if not self.terrain.is_water():
            if map_mode.is_dev():
                return self.lerp_dev_color()
            elif map_mode == MapMode.POLITICAL:
                return default  # TODO: implement political map mode

        return default

    def lerp_dev_color(self):
        # Linear interpolation of development color
        start_color = (255, 0, 0)  # Red
        end_color = (0, 255, 0)    # Green
        t = self.development / 10.0
        return self.lerp_color(start_color, end_color, t)

    @staticmethod
    def lerp_color(start_color, end_color, t):
        # Linear interpolation of RGB color
        r = int((1 - t) * start_color[0] + t * end_color[0])
        g = int((1 - t) * start_color[1] + t * end_color[1])
        b = int((1 - t) * start_color[2] + t * end_color[2])
        return r, g, b

    # endregion
    def create_ui_table(self):
        from main import WIDTH, HEIGHT
        table_width = WIDTH // 4
        table_height = HEIGHT // 2
        x_pos = 0
        if self.center_pos[0] < WIDTH // 2:
            x_pos = WIDTH - table_width
        table_texts = [
            ("Province name", self.name),
            ("Terrain", "None"),
            ("Temperature", str(self.temperature)),
            ("Development", str(self.development)),
            ("Owned by", "None"),
            ("Occupied by", "None")
        ]

        ui_table = UI_Table((x_pos, HEIGHT // 2), (table_width, table_height), f"ProvinceTable", len(table_texts), 2)
        ps = (0, 0)
        for index, (title, value) in enumerate(table_texts):
            # positions and sizes automatically get set by table
            title_ui_element = TextBox(ps, ps, f"Attribute {title}", 24, bold=False, alignment=TextAlignment.LEFT)
            title_ui_element.set_text([title])
            value_ui_element = TextBox(ps, ps, f"Attribute {title} Value", 24, bold=True, alignment=TextAlignment.RIGHT)
            value_ui_element.set_text([value])

            ui_table.set_table_element(index, 0, title_ui_element)
            ui_table.set_table_element(index, 1, value_ui_element)

        self.info_ui_table = ui_table
