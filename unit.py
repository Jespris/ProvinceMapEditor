import math

from province import Province


class Unit:
    def __init__(self, name: str, spawn_province: Province):
        self.name = name
        self.path: [Province] = []
        self.movement_points = 0  # 10 per day plus maybe some modifiers from king
        self.current_province = spawn_province
        self.move_points_regen = 10

    def update(self):  # should get called every day
        if self.has_path():
            self.movement_points += self.move_points_regen
            self.move()
        else:
            self.movement_points = 0

    def move(self):
        if self.has_path():
            movement_cost = self.get_next_province().base_cost_to_enter()
            # TODO: add current province as a parameter to cost_function?
            if self.movement_points - movement_cost >= 0:
                self.current_province = self.path.pop(0)
                self.movement_points -= movement_cost

    def can_change_path(self):
        if self.has_path():
            return self.movement_points < self.get_next_province().base_cost_to_enter() // 2
        return True

    def has_path(self):
        return self.path is not None

    def get_next_province(self) -> Province:
        assert self.has_path()
        return self.path[0]

    def cost_to_enter_province(self, province: Province, cost_so_far: int):
        distance = self.distance(province.center_pos)
        base_days_to_enter_province = math.ceil(self.movement_cost_to_enter_province(province) / self.move_points_regen * distance)
        print(f"Days to enter province {base_days_to_enter_province} from {self.current_province.name} to {province.name}")
        if base_days_to_enter_province < 0:
            # impassable terrain
            return -99999

        days_used_after_move = cost_so_far + base_days_to_enter_province
        return days_used_after_move

    def movement_cost_to_enter_province(self, province):
        # TODO: king proficiency affects cost?
        return province.base_cost_to_enter()

    def distance(self, b):
        a = self.current_province.center_pos
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)





