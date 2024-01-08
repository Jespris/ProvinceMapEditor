import random
from typing import Union
from log_handler import log_message


class Person:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age
        self.is_dead = False
        self.months_until_birthday = 12
        self.diplo_power = random.randint(0, 10)
        self.admin_power = random.randint(0, 10)
        self.mil_power = random.randint(0, 10)

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

    def have_birthday(self):
        self.age += 1

    def die(self):
        log_message(f"{self.name} died at age {self.age}")
        self.is_dead = True

    def monthly_update(self):
        self.months_until_birthday -= 1
        if self.months_until_birthday <= 0:
            self.have_birthday()
            self.months_until_birthday = 12
        self.check_if_dead()

    def check_if_dead(self):
        if random.randint(1, self.death_risk_function()) == 1:
            self.die()

    def death_risk_function(self):
        # at age 10 or returns 100
        # at age 50 should return 20
        # at age 60 should return 10
        # age 70 -> 5
        # age 80 -> 2
        if self.age <= 90:
            return int(0.02 * (self.age - 90) ** 2 + 2) * 12
        return 1

