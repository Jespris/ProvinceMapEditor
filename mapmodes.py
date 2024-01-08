from enum import Enum, auto


class MapMode(Enum):
    TERRAIN = auto()
    DEVELOPMENT = auto()
    POLITICAL = auto()
    TEMPERATURE = auto()

    def is_dev(self):
        if self == self.DEVELOPMENT:
            return True
        return False

    def is_political(self):
        if self == self.POLITICAL:
            return True
        return False

    def is_temp(self):
        if self == self.TEMPERATURE:
            return True
        return False
