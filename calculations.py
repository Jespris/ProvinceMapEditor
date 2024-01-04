from pypoman.polyhedron import compute_chebyshev_center

from pypoman.duality import compute_polytope_halfspaces


def calculate_center(vertices):
    a, b = compute_polytope_halfspaces(vertices)
    center = compute_chebyshev_center(a, b)
    return center
