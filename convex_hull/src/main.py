import sys
import time
import math
import random
import matplotlib.pyplot as plt

from clifford import Cl

# 2D PGA
layout, blades = Cl(2, 0, 1, firstIdx=0)
e01 = blades['e01']
e02 = blades['e02']
e12 = blades['e12']

rand_limit = (-1.0, 1.0)
plot_limit = (-1.5, 1.5)


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.M = e12 + x*e02 - y*e01

    def __and__(self, other):
        if isinstance(other, Point):
            return self.M & other.M
        return self.M & other

    def __rand__(self, other):
        return other & self.M

    def __xor__(self, other):
        if isinstance(other, Point):
            return self.M ^ other.M
        return self.M ^ other
    
    def __rxor__(self, other):
        return other ^ self.M
    
    def __getitem__(self, blade):
        return self.M[blade]
    
    
def profiler(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start
        print(f"{func.__name__} took {duration:.6f} seconds.")
        return result
    return wrapper


def plot_points(points: list, enum=False):
    xs = [p.x for p in points]
    ys = [p.y for p in points]

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=10, color='black')

    if enum:
        for i, (x, y) in enumerate(zip(xs, ys)):
            plt.text(x + 0.02, y + 0.02, str(i), fontsize=9, color='blue')

    plt.xlim(*plot_limit)
    plt.ylim(*plot_limit)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Sorted Points")
    plt.show()


def plot_pivot_with_lines(points: list, enum=False):
    pivot = points[0]
    px, py = pivot.x, pivot.y

    xs = [p.x for p in points]
    ys = [p.y for p in points]

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, s=10, color='black')
    plt.scatter([px], [py], s=10, color='red', label='Pivot')

    for p in points[1:]:
        plt.plot([px, p.x], [py, p.y], 'k--', linewidth=1)

    if enum:
        for i, (x, y) in enumerate(zip(xs, ys)):
            plt.text(x + 0.02, y + 0.02, str(i), fontsize=9, color='blue')

    plt.xlim(*plot_limit)
    plt.ylim(*plot_limit)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Pivot with Lines")
    plt.legend()
    plt.show()


def plot_hull(hull: list, points: list):
    xs_hull   = [p.x for p in hull] + [hull[0].x]
    ys_hull   = [p.y for p in hull] + [hull[0].y]
    xs_points = [p.x for p in points]
    ys_points = [p.y for p in points]

    plt.figure(figsize=(6, 6))
    plt.scatter(xs_points, ys_points, s=10, color='black')
    plt.plot(xs_hull, ys_hull, 'g-', linewidth=2)
    plt.xlim(*plot_limit)
    plt.ylim(*plot_limit)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Convex Hull")
    plt.show()


@profiler
def graham_convex_hull(points: list):
    # Find the point with the lowest Y coordinate, with the right most X coordinate
    pivot = min(points, key=lambda p: (p.y, p.x))

    # Remove this point from the list
    points.remove(pivot)

    # Sort remaining points by their polar angle
    points = sorted(points, key=lambda p: math.atan2(p.y - pivot.y, p.x - pivot.x))

    # Reintroduce the pivot to the list as the first element
    sorted_points = [pivot] + points

    hull = [pivot]

    for p in sorted_points:
        while len(hull) >= 2 and (hull[-2].M & hull[-1].M & p.M).value[0] < 0:
            hull.pop()
        hull.append(p)

    return hull, sorted_points


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    points = []
    for _ in range(n):
        x = random.uniform(*rand_limit)
        y = random.uniform(*rand_limit)
        points.append(Point(x, y))
        
    hull, sorted_points = graham_convex_hull(points)

    plot_points(sorted_points, enum=True)
    plot_pivot_with_lines(sorted_points, enum=True)
    plot_hull(hull, sorted_points)