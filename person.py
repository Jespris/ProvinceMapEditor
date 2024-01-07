import random
from typing import Union


class Person:
    def __init__(self, name: str, age: int):
        self.name: str = name
        self.age: int = age
        self.is_dead = False
        self.father: Union[Person, None] = None
        self.sons: [Person] = []
        self.heir: Union[Person, None] = None
        self.months_until_birthday = 12

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

    def have_birthday(self):
        self.age += 1
        self.check_if_dead()

    def die(self):
        print(f"{self.name} died at age {self.age}")
        self.is_dead = True

    def get_random_name(self):
        # TODO: get random name
        return f"{self.name}'s son nr {len(self.sons) + 1}"

    def monthly_update(self):
        self.months_until_birthday -= 1
        if self.months_until_birthday <= 0:
            self.have_birthday()
            self.months_until_birthday = 12

    def check_if_dead(self):
        if random.randint(1, self.death_risk_function()) == 1:
            self.die()

    def death_risk_function(self):
        # at age 10 or returns 100
        # at age 50 should return 20
        # at age 60 should return 10
        # age 70 -> 5
        # age 80 -> 2
        if self.age <= 80:
            return int(0.02 * (self.age - 90) ** 2 + 2)
        return 2

