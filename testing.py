from gamestate import GameState
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from person import Person
from army import Army
from calculations import calculate_center


def test_patriarchy():
    for i in range(1, 10):
        king = Person(f"King Bob {'I'*i}", 30)
        while not king.is_dead:
            king.monthly_update()


def plot_polygon_and_farthest_point(vertices, farthest_point):
    x = [vertex.pos[0] for vertex in vertices]
    y = [vertex.pos[1] for vertex in vertices]

    plt.plot(x + [x[0]], y + [y[0]], 'b-')  # Connect the last point to the first to close the polygon
    plt.scatter(*zip(*[vertex for vertex in vertices]), color='red', label='Polygon Vertices')
    plt.scatter(*farthest_point, color='green', label='Farthest Point')

    plt.title('Polygon and Farthest Point')
    plt.legend()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()


def test_center():
    # Example usage:
    polygon_vertices = [(0, 0), (10, 0), (10, 10), (7, 7), (0, 10)]
    center = calculate_center(polygon_vertices)
    plot_polygon_and_point(polygon_vertices, center, True)
    print("Centroid:", center)


"""
def test_point_inside_polygon():
    province = Province(0)
    # test 1
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0)]
    point = (2, 2)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 2
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0)]
    point = (6, 6)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: false")

    # test 3
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0), (3, 3)]
    point = (3, 3)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 4
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0), (3, 3)]
    point = (6, 6)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: false")

    # test 5
    polygon = [(0, 0), (0, 5), (2, 6), (5, 5), (5, 0)]
    point = (2, 3)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 6
    polygon = [(0, 0), (0, 5), (2, 6), (5, 5), (5, 0)]
    point = (4, 4)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 7
    polygon = [(0, 0), (2, 5), (1, 8), (4, 10), (7, 8), (6, 5), (8, 0)]
    point = (4, 6)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 8
    polygon = [(0, 0), (2, 5), (1, 8), (4, 10), (7, 8), (6, 5), (8, 0)]
    point = (1, 4)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: false")
    print("Plotting...")
    plot_polygon_and_point(polygon, point, result)

    # test 9
    polygon = [(0, 0), (1, 8), (4, 10), (7, 8), (6, 5), (8, 0)]
    point = (1, 4)
    province.set_border(polygon)
    result = province.point_inside_province(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")
    print("Plotting...")
    plot_polygon_and_point(polygon, point, result)
"""


def plot_polygon_and_point(polygon, point, result):
    fig, ax = plt.subplots()

    # Plot the polygon
    polygon_patch = Polygon(polygon, edgecolor='b', fill=None)
    ax.add_patch(polygon_patch)

    # Plot the point
    ax.plot(point[0], point[1], 'ro', label='Point')

    # Highlight the point if it's inside the polygon
    if result:
        ax.plot(point[0], point[1], 'go', label='Inside')

    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    ax.set_aspect('equal', 'box')
    plt.legend()
    plt.show()


def test_distances():
    state = GameState()
    # test distances between some random provinces
    barcelona = state.get_province_by_name("Barcelona")
    mallorca = state.get_province_by_name("Mallorca")
    madrid = state.get_province_by_name("Madrid")
    bar_mal = state.get_province_distance(barcelona, mallorca)
    print(f"Distance between {barcelona.name} and {mallorca.name} is {str(bar_mal)}")
    mad_mal = state.get_province_id_distance(madrid.id, mallorca.id)
    print(f"Distance between {madrid.name} and {mallorca.name} is {str(mad_mal)}")
    mal_mad = state.get_province_distance(mallorca, madrid)
    print(f"Madrid - Mallorca = Mallorca - Madrid: {mad_mal == mal_mad}")


def test_pathing():
    state = GameState()
    start_province = state.get_province_by_name("Leon")
    unit = Army("Bob", start_province)
    end_province = state.get_province_by_name("Gibraltar")
    state.set_unit_path(unit, end_province.id)
    print(f"Path from {start_province.name} to {end_province.name}:")
    print([province.name for province in unit.path])
    bird_distance = unit.distance(end_province.center_pos)
    print(f"Straight line length from {start_province.name} to {end_province.name}: {bird_distance}")
    print(f"Best case amount of days: {bird_distance / unit.move_points_regen}")


def test_set():
    # test_point_inside_polygon()
    # test_distances()
    # test_pathing()
    # test_center()
    test_patriarchy()
    
    