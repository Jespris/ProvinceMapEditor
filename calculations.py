from sympy.geometry.polygon import Polygon


def calculate_center(vertices):

    polygon = Polygon(*vertices)
    point = polygon.centroid
    return int(point[0]), int(point[1])
