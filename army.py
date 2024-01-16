import math
import pygame as p


class Army:
    def __init__(self, name: str, spawn_province, nation=None, max_strength=100):
        # Initialize unit attributes
        self.name = name
        self.path = []  # List to store the path of provinces
        self.movement_points = 0  # 10 per day plus maybe some modifiers from king
        self.current_province = spawn_province  # The current province the unit is in
        self.move_points_regen = 10  # Movement points regenerated per day
        self.nation = nation
        self.max_strength = max_strength
        self.strength = 1

    def set_nation(self, nation):
        self.nation = nation

    def daily_update(self):  # should get called every day
        # Update unit's movement points and move along the path if available
        if self.has_path():
            self.movement_points += self.move_points_regen
            self.move()
        else:
            self.movement_points = 0

    # region Pathing updates
    def move(self):
        # Move the unit along the path if movement points allow
        if self.has_path():
            if self.current_province == self.path[0]:
                self.current_province = self.path.pop(0)
            if self.has_path():
                movement_cost = self.get_next_province().base_cost_to_enter()
                if self.movement_points - movement_cost >= 0:
                    self.current_province = self.path.pop(0)
                    self.movement_points -= movement_cost

    def can_change_path(self):
        # Check if the unit can change its path based on movement points
        if self.has_path():
            return self.movement_points < self.get_next_province().base_cost_to_enter() // 2
        return True

    def has_path(self):
        # Check if the unit has a path to follow
        return self.path != []

    def get_next_province(self):
        # Get the next province in the unit's path
        assert self.has_path()
        return self.path[0]

    def cost_to_enter_province(self, province, cost_so_far: int):
        # Calculate the cost to enter a province based on the unit's movement and path
        distance = self.distance(province.center_pos)
        base_days_to_enter_province = math.ceil(self.movement_cost_to_enter_province(province) / self.move_points_regen * distance)

        if base_days_to_enter_province < 0:
            # Impassable terrain
            return -99999

        days_used_after_move = cost_so_far + base_days_to_enter_province
        return days_used_after_move

    def movement_cost_to_enter_province(self, province):
        # Calculate the movement cost to enter a province
        return province.base_cost_to_enter()

    # endregion

    def distance(self, b):
        # Calculate the distance between two points
        a = self.current_province.center_pos
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    # region Drawing the unit
    def draw(self, screen, selected_province_id):
        # Draw the unit on the screen
        p.draw.rect(screen, p.Color("green"), p.Rect(self.current_province.center_pos, (16, 16)))
        if self.has_path():
            self.draw_path(screen)

    def draw_path(self, screen):
        # Draw the path on the screen
        if len(self.path) >= 1:
            p.draw.line(screen, p.Color("black"), self.current_province.center_pos, self.path[0].center_pos, 8)
            p.draw.circle(screen, p.Color("red"), self.path[-1].center_pos, 10)

        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]
            p.draw.line(screen, p.Color("black"), start.center_pos, end.center_pos, 8)
    # endregion
