from typing import Union

from province import Province
from army import Army


"""
PathSearch returns a path using arguments: (ourWorld, theUnit, startTile, endTile)
- the unit is an object that tries to path between tiles
- it might have special logic based on it's movement type and the type of tiles being moved through

The tiles need to be able to get the following info:
- List of neighbours  (function should be called: get_neighbours())
- The "cost" to enter this tile from another tile  (function should be called: aggregate_cost_to_enter())
- if tile is impassable, return negative cost
"""


class PathSearch:
    def __init__(self, world: {int: Province}, unit: Army, start: int, end: int, cost_func):
        self.world: {int: Province} = world
        self.unit: Army = unit
        self.start: int = start
        self.end: int = end
        self.cost_func = cost_func
        self.path: Union[int, None] = None

    def find_path(self):
        if self.world is None or self.unit is None or self.start is None or self.end is None or self.cost_func is None:
            print("Null values passed to PathSearch!!!")
            return

        self.do_work()

        if self.path is not None:
            return self.path
        else:
            print("No path found :/")
            return

    def do_work(self):
        closed_set = []
        open_set = [self.start]
        open_set_dict = {self.start: 0}
        came_from = {}
        g_score = {self.start: 0}
        first_score = self.cost_func(self.world[self.start], self.world[self.end])
        assert isinstance(first_score, int)
        f_score = {self.start: first_score}

        while len(open_set) > 0:
            current = open_set.pop(0)
            # check if goal is where we are
            if current == self.end:
                self.reconstruct_path(came_from, current)
                return

            closed_set.append(current)

            for neighbour_id in self.world[current].get_neighbours():
                assert isinstance(neighbour_id, int)
                neighbour = self.world[neighbour_id]
                assert isinstance(neighbour, Province)
                if closed_set.__contains__(neighbour_id):
                    continue  # ignore this completed neighbour

                total_pathfinding_cost_to_neighbour = (
                    neighbour.cost_to_enter(
                        g_score[current],
                        self.world[current].terrain,
                        self.unit
                    )
                )

                if total_pathfinding_cost_to_neighbour < 0:
                    # impassable terrain
                    continue

                tgs = total_pathfinding_cost_to_neighbour

                if open_set.__contains__(neighbour_id) and tgs >= g_score[neighbour_id]:
                    continue  # skip, shorter path already found

                came_from[neighbour_id] = current
                g_score[neighbour_id] = tgs
                f_score[neighbour_id] = tgs + self.cost_func(neighbour, self.world[self.end])

                if neighbour_id not in open_set:
                    open_set.append(neighbour_id)

                open_set_dict[neighbour_id] = f_score[neighbour_id]

    def reconstruct_path(self, came_from: {int: int}, current: int):
        # at this point, current is the goal
        # go backwards through the dictionaries, until we reach the end, aka starting tile
        total_path = [current]
        while True:  # TODO: maybe change this to something else, seems dangerous
            try:
                current = came_from[current]
            except KeyError:
                break
            total_path.append(current)

        # now, total path is a queue that is running backwards from end tile to start tile, so reverse
        total_path.reverse()
        self.path = total_path
        # path is now a list of province IDs
