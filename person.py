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
        self.days_until_birthday = 360

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

    def add_son(self):
        print(f"{self.name} had a son at age {self.age}")
        name = self.get_random_name()
        new_son = Person(name, 0)
        self.sons.append(new_son)
        new_son.father = self
        self.check_heir(None)

    def have_birthday(self):
        self.age += 1
        self.check_if_dead()

    def die(self):
        print(f"{self.name} died at age {self.age}")
        self.is_dead = True

    def get_random_name(self):
        # TODO: get random name
        return f"{self.name}'s son nr {len(self.sons) + 1}"

    def daily_update(self):
        self.days_until_birthday -= 1
        if self.days_until_birthday <= 0:
            self.have_birthday()
            self.days_until_birthday = 365

        if random.randint(1, 8 * 360) == 1 and 18 <= self.age < 60:
            self.add_son()

        else:
            # this function is first called on the king of the nation, which means we have to recursively update
            for son in self.sons:
                assert isinstance(son, Person)
                son.daily_update()
                # check if son died
                if son.is_dead:
                    self.check_heir(son.heir)

            # update brothers for heir calculation purposes
            if self.father is not None:
                for brother_index in range(self.father.sons.index(self), len(self.father.sons)):
                    brother = self.father.sons[brother_index]
                    assert isinstance(brother, Person)
                    if brother.name == self.name:
                        continue
                    else:
                        brother.daily_update()

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
            return int(0.02 * (self.age - 80) ** 2 + 2)
        return 2

    def has_heir(self):
        return self.heir is not None

    def check_heir(self, sons_heir):
        # TODO: add heir calculations
        pass
