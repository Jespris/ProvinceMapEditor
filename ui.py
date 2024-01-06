import math
from enum import Enum, auto
from typing import Union

import pygame as p


class Rect_UI_Element:
    def __init__(self, pos: (int, int), size: (int, int), name: str):
        self.x, self.y = pos  # the top left corner of the rectangle
        self.width, self.height = size  # width and height
        self.name: str = name  # for ID-ing purposes

    def draw(self, screen):
        pass

    def get_clicked(self, pos: (int, int)) -> bool:
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

    def to_string(self):
        return self.name


class Circle_UI_Element:
    def __init__(self, center: (int, int), radius: int, name):
        self.x, self.y = center
        self.radius = radius
        self.name = name

    def draw(self, screen):
        pass

    def get_clicked(self, pos: (int, int)) -> bool:
        distance = math.sqrt((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2)
        return distance < self.radius

    def to_string(self):
        return self.name


class TextAlignment(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class TextBox(Rect_UI_Element):
    def __init__(
            self,
            pos: (int, int),
            size: (int, int),
            name: str,
            text_size, bold=False,
            box_thickness=4,
            transparent=False,
            black_text=True,
            alignment=TextAlignment.CENTER
    ):

        super().__init__(pos, size, name)
        self.text_size = text_size
        self.font = p.font.Font("freesansbold.ttf", self.text_size)
        self.bold = bold
        self.box_thickness = box_thickness
        self.transparent = transparent
        self.text: [str] = []
        self.black_text = black_text
        self.alignment = alignment

    def set_text(self, text: [str]):
        self.text = text

    def draw(self, screen):
        black = p.Color("black")
        white = p.Color("white")
        # draw background
        if not self.transparent:
            color = white
            if not self.black_text:
                color = black
            p.draw.rect(screen, color, p.Rect(self.x, self.y, self.width, self.height))

        # draw box
        if not self.box_thickness == 0:
            color = black
            if not self.black_text:
                color = white
            p.draw.rect(screen, color, p.Rect(self.x, self.y, self.width, self.height), self.box_thickness)

        # draw the text
        self.draw_text(screen)

    def draw_text(self, screen):
        side_gap = self.text_size
        total_text_height = len(self.text) * self.text_size
        # print(f"Total text height: {total_text_height}, text: {self.text}, font size: {self.text_size}")
        assert total_text_height < self.height
        start_y = self.y + (self.height - total_text_height) // 2
        text_color = p.Color("black")
        if not self.black_text:
            text_color = p.Color("white")

        for index, text in enumerate(self.text):
            text_surface = self.font.render(text, self.bold, text_color)
            text_rect = text_surface.get_rect()
            if self.alignment == TextAlignment.CENTER:
                text_rect.midtop = (self.x + self.width // 2, start_y + index * self.text_size)
            elif self.alignment == TextAlignment.LEFT:
                text_rect.topleft = (self.x + side_gap, start_y + index * self.text_size)
            elif self.alignment == TextAlignment.RIGHT:
                text_rect.topright = (self.x + self.width - side_gap, start_y + index * self.text_size)
            screen.blit(text_surface, text_rect)


class UI_Table(Rect_UI_Element):
    def __init__(self, pos: (int, int), size: (int, int), name, rows: int, cols: int):
        super().__init__(pos, size, name)
        self.rows: int = rows
        self.cols: int = cols
        self.table: {(int, int): Rect_UI_Element} = {}
        self.is_fitted = False

    def set_table_element(self, row: int, col: int, element: Rect_UI_Element):
        assert row < self.rows
        assert col < self.cols
        self.table[(row, col)] = element
        self.is_fitted = False

    def fit_table(self):
        print("Fitting table")
        col_width = self.width // self.cols
        row_height = self.height // self.rows
        for (row, col), element in self.table.items():
            assert isinstance(element, Rect_UI_Element)
            element.x = self.x + col * col_width
            element.y = self.y + row * row_height
            element.width = col_width
            element.height = row_height
        self.is_fitted = True

    def draw(self, screen):
        # draw white background
        p.draw.rect(screen, p.Color("white"), p.Rect(self.x, self.y, self.width, self.height))
        # draw black frame
        p.draw.rect(screen, p.Color("black"), p.Rect(self.x, self.y, self.width, self.height), 4)
        # fit elements on table
        if not self.is_fitted:
            self.fit_table()
        # draw every element in table
        for element in self.table.values():
            assert isinstance(element, Rect_UI_Element)
            element.draw(screen)

    def get_table_element_by_name(self, element_name: str):
        for key, element in self.table.items():
            assert isinstance(element, Rect_UI_Element)
            if element.name == element_name:
                return element
        return None


