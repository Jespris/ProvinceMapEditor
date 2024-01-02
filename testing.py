from province import Province
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def test_point_inside_polygon():
    province = Province(0)
    # test 1
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0)]
    point = (2, 2)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 2
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0)]
    point = (6, 6)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: false")

    # test 3
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0), (3, 3)]
    point = (3, 3)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 4
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0), (3, 3)]
    point = (6, 6)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: false")

    # test 5
    polygon = [(0, 0), (0, 5), (2, 6), (5, 5), (5, 0)]
    point = (2, 3)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 6
    polygon = [(0, 0), (0, 5), (2, 6), (5, 5), (5, 0)]
    point = (4, 4)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 7
    polygon = [(0, 0), (2, 5), (1, 8), (4, 10), (7, 8), (6, 5), (8, 0)]
    point = (4, 6)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")

    # test 8
    polygon = [(0, 0), (2, 5), (1, 8), (4, 10), (7, 8), (6, 5), (8, 0)]
    point = (1, 4)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: false")
    print("Plotting...")
    plot_polygon_and_point(polygon, point, result)

    # test 9
    polygon = [(0, 0), (1, 8), (4, 10), (7, 8), (6, 5), (8, 0)]
    point = (1, 4)
    province.set_border(polygon)
    result = province.is_clicked(point)
    print(f"The point {point} is inside polygon: {str(result)}, expected result: true")
    print("Plotting...")
    plot_polygon_and_point(polygon, point, result)


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


def test_set():
    test_point_inside_polygon()
    
    