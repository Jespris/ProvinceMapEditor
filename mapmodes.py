from enum import Enum, auto


class MapMode(Enum):
    TERRAIN = auto()
    DEVELOPMENT = auto()
    POLITICAL = auto()

    def is_dev(self):
        if self == self.DEVELOPMENT:
            return True
        return False