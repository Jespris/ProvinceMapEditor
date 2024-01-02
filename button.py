import pygame as p

from province import Province
from terraintype import TerrainType


class EditProvinceButton:
    def __init__(self, pos, text):
        self.pos = pos
        self.size = (100, 20)
        self.text = text
        self.text_size = 14

    def on_click(self, province: Province):
        pass

    def is_clicked(self, mouse):
        return self.pos[0] < mouse[0] < self.pos[0] + self.size[0] and self.pos[1] < mouse[1] < self.pos[1] + self.size[1]

    def draw(self, screen):
        p.draw.rect(screen, p.Color("black"), p.Rect(self.pos, self.size))
        font = p.font.Font("freesansbold.ttf", self.text_size)
        text = font.render(self.text, False, p.Color("white"))
        text_rect = text.get_rect()
        text_rect.center = (self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2)
        screen.blit(text, text_rect)


class NameButton(EditProvinceButton):
    def __init__(self, pos, text):
        super().__init__(pos, text)

    def on_click(self, province: Province):
        user_input = input("Province name >")
        province.set_name(user_input)


class TerrainButton(EditProvinceButton):
    def __init__(self, pos, text, terrain_type):
        super().__init__(pos, text)
        self.terrain_type = terrain_type

    def on_click(self, province):
        province.set_terrain(self.terrain_type)

