import sys
import math
import time
import random
import matplotlib.pyplot as plt

from itertools import combinations


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
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float):
        return Point(self.x * scalar, self.y * scalar) 
    
    def __truediv__(self, scalar: float):
        return Point(self.x / scalar, self.y / scalar)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return f"Point({self.x:.3f}, {self.y:.3f})"
    

class Circle():
    def __init__(self, c=Point(0, 0), r=1):
        self.c = c
        self.r = r

    def __repr__(self):
        return f"Circle(Centroid={self.c}, Radius={self.r:.3f})"

    @classmethod
    def two_points(cls, p1:Point, p2:Point):
        c = (p1 + p2) / 2.0
        r = abs(p1 - p2) / 2.0
        return cls(c, r)

    @classmethod
    def three_points(cls, p1:Point, p2:Point, p3:Point):
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y

        det = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

        if det == 0:
            raise ValueError("Determinant is invalid.")

        x1_sq = x1**2 + y1**2
        x2_sq = x2**2 + y2**2
        x3_sq = x3**2 + y3**2

        cx = (x1_sq * (y2 - y3) + x2_sq * (y3 - y1) + x3_sq * (y1 - y2)) / det
        cy = (x1_sq * (x3 - x2) + x2_sq * (x1 - x3) + x3_sq * (x2 - x1)) / det

        center = Point(cx, cy)
        radius = abs(center - p1)

        return cls(center, radius)

    def inside(self, p):
        return abs(p - self.c) < self.r
    

def generate_points(n=1, circle=Circle(Point(0,0), r=1)):
    points = []

    centroid = circle.c
    radius = circle.r

    for _ in range(n):
        θ = random.uniform(0, 2 * math.pi)
        x = centroid.x + radius * math.sqrt(random.uniform(0, 1)) * math.cos(θ)
        y = centroid.y + radius * math.sqrt(random.uniform(0, 1)) * math.sin(θ)
        points.append(Point(x, y))

    return points


@profiler
def min_circle_heuristic(points: list[Point]):
    boundary_points = [
        min(points, key=lambda p: p.x),
        max(points, key=lambda p: p.x),
        min(points, key=lambda p: p.y),
        max(points, key=lambda p: p.y)
    ]

    max_dist = 0
    max_pair = None

    for p1, p2 in combinations(boundary_points, 2):
        dist = math.dist(p1, p2)

        if(dist > max_dist):
            max_dist = dist
            max_pair = (p1, p2)

    p1, p2 = max_pair

    circle = Circle.two_points(p1, p2)

    for p in points:
        d = p - circle.c

        if(abs(d) > circle.r):
            centroid = circle.c + d * (abs(d) - circle.r) / 2.0
            radius = (abs(d) + circle.r) / 2.0
            circle = Circle(centroid, radius)

    return circle


@profiler
def min_circle_randomized(points: list[Point]):
    random.shuffle(points)
    circle = Circle.two_points(points[0], points[1])

    for i in range(2, len(points)):
        if(not circle.inside(points[i])):
            circle = min_circle_with_point(points[:i], points[i])

    return circle


def min_circle_with_point(points:list, q:Point):
    circle = Circle.two_points(points[0], q)

    for i in range(1, len(points)):
        if(not circle.inside(points[i])):
            circle = min_circle_with_2_points(points[:i], points[i], q)

    return circle


def min_circle_with_2_points(points:list, q1:Point, q2:Point):
    circle = Circle.two_points(q1, q2)

    for i in range(0, len(points)):
        if(not circle.inside(points[i])):
            circle = Circle.three_points(points[i], q1, q2)

    return circle


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    points = generate_points(n)
    circle_heuristic = min_circle_heuristic(points)
    circle_randomized = min_circle_randomized(points)
    
    x_vals = [p.x for p in points]
    y_vals = [p.y for p in points]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x_vals, y_vals, color='blue', s=5)

    circles = [
        (0, 0, 1, 'black', 'Unit Circle', 1.0),
        (circle_heuristic.c.x, circle_heuristic.c.y, circle_heuristic.r, 'red', f'Heuristic (r={circle_heuristic.r:.3f})', 0.5),
        (circle_randomized.c.x, circle_randomized.c.y, circle_randomized.r, 'green', f'Randomized (r={circle_randomized.r:.3f})', 0.5)
    ]

    for x, y, r, color, label, alpha in circles:
        circle = plt.Circle((x, y), r, edgecolor=color, fill=False, linewidth=2, alpha=alpha, label=label)
        ax.add_patch(circle)

    padding = 0.5
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-1 - padding, 1 + padding)
    ax.set_ylim(-1 - padding, 1 + padding)

    ax.legend()
    ax.grid(True)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Minimum Enclosing Circle')
    plt.tight_layout()
    plt.show()