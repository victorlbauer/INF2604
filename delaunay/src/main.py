import sys
import math
import time
import random
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

RAND_LIMIT = (-1.0, 1.0)
PLOT_LIMIT = (-1.2, 1.2)
EPS = 1e-10

def profiler(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start
        print(f"{func.__name__} took {duration:.6f} seconds.")
        return result
    return wrapper


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS

    def __hash__(self):
        return hash((self.x, self.y))


class Edge:
    def __init__(self, p1: Point, p2: Point):
        if (p1.x, p1.y) < (p2.x, p2.y):
            self.p1, self.p2 = p1, p2
        else:
            self.p1, self.p2 = p2, p1

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __hash__(self):
        return hash((self.p1, self.p2))


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        if self._orientation(p1, p2, p3) < EPS:
            p2, p3 = p3, p2

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.edges = [Edge(p1, p2), Edge(p2, p3), Edge(p3, p1)]

    def _orientation(self, a, b, c):
        return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

    def inside_circumcircle(self, p: Point):
        ax, ay = self.p1.x - p.x, self.p1.y - p.y
        bx, by = self.p2.x - p.x, self.p2.y - p.y
        cx, cy = self.p3.x - p.x, self.p3.y - p.y

        mat = np.array([
            [ax, ay, ax * ax + ay * ay],
            [bx, by, bx * bx + by * by],
            [cx, cy, cx * cx + cy * cy]
        ])

        return np.linalg.det(mat) > EPS
    
    def circumcircle(self):
        ax, ay = self.p1.x, self.p1.y
        bx, by = self.p2.x, self.p2.y
        cx, cy = self.p3.x, self.p3.y

        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < EPS:
            return None, None

        a2 = ax**2 + ay**2
        b2 = bx**2 + by**2
        c2 = cx**2 + cy**2

        ux = (a2 * (by - cy) + b2 * (cy - ay) + c2 * (ay - by)) / d
        uy = (a2 * (cx - bx) + b2 * (ax - cx) + c2 * (bx - ax)) / d

        radius = math.hypot(ux - ax, uy - ay)
        return (ux, uy), radius

    def contains_vertex(self, point: Point):
        return point == self.p1 or point == self.p2 or point == self.p3


@profiler
def bowyer_watson(points: list):
    super_triangle = Triangle(Point(3.0, 0.0), Point(0.0, 3.0), Point(-3.0, -3.0))
    triangulation = [super_triangle]

    for p in points:
        bad_triangles = [t for t in triangulation if t.inside_circumcircle(p)]

        edge_count = defaultdict(int)
        for t in bad_triangles:
            for edge in t.edges:
                edge_count[edge] += 1

        boundary_edges = [e for e, count in edge_count.items() if count == 1]

        for t in bad_triangles:
            triangulation.remove(t)

        for e in boundary_edges:
            triangulation.append(Triangle(e.p1, e.p2, p))

    triangles = [
        t for t in triangulation if not
        (super_triangle.contains_vertex(t.p1) or super_triangle.contains_vertex(t.p2) or super_triangle.contains_vertex(t.p3))
    ]

    return triangles


def plot_triangulation(points, triangles, circumcircle=False):
    _, ax = plt.subplots(figsize=(8, 8))

    for triangle in triangles:
        xs = [triangle.p1.x, triangle.p2.x, triangle.p3.x, triangle.p1.x]
        ys = [triangle.p1.y, triangle.p2.y, triangle.p3.y, triangle.p1.y]
        ax.plot(xs, ys, 'b-', linewidth=0.6)

        if circumcircle:
            center, radius = triangle.circumcircle()
            if center and radius:
                circle = plt.Circle(center, radius, edgecolor='green', fill=False, linestyle='--', linewidth=0.5)
                ax.add_patch(circle)

    ax.scatter([p.x for p in points], [p.y for p in points], c='red', s=10)

    ax.set_xlim(PLOT_LIMIT)
    ax.set_ylim(PLOT_LIMIT)
    ax.set_aspect('equal')
    ax.set_title("Delaunay Triangulation (Bowyer-Watson)")
    plt.show()


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    points = [
        Point(random.uniform(*RAND_LIMIT), random.uniform(*RAND_LIMIT))
        for _ in range(n)
    ]

    points = list(set(points))

    triangles = bowyer_watson(points)

    plot_triangulation(points, triangles)
