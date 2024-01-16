import math

from sympy.geometry.polygon import Polygon

from province import Province


def calculate_center(vertices):

    polygon = Polygon(*vertices)
    point = polygon.centroid
    return int(point[0]), int(point[1])


def get_province_distance(province_a: Province, province_b: Province) -> int:
    return int(math.sqrt((province_a.center_pos[0] - province_b.center_pos[0])**2 +
                         (province_a.center_pos[1] - province_b.center_pos[1])**2))