import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def ζ(points: list , u: float):
    n = len(points) - 1
    segment_len = 1.0 / n

    i = min(int(u / segment_len), n - 1)
    local_u = (u - i * segment_len) / segment_len
    
    x0, y0 = points[i]
    x1, y1 = points[i + 1]
    x = (1 - local_u) * x0 + local_u * x1
    y = (1 - local_u) * y0 + local_u * y1
    
    return np.array((x, y))


def bilinear_projector(curves: list, subdivisions: int):
    if subdivisions <= 0:
        return []

    ψ1 = curves['ψ1']
    ψ2 = curves['ψ2']
    ξ1 = curves['ξ1']
    ξ2 = curves['ξ2']

    points = []
    step = 1.0 / (subdivisions + 1)

    for i in range(1, subdivisions + 1):
        u = i * step
        for j in range(1, subdivisions + 1):
            v = j * step

            ψ_point = (1 - v) * ζ(ψ1, u) + v * ζ(ψ2, u)
            ξ_point = (1 - u) * ζ(ξ1, v) + u * ζ(ξ2, v)

            p00 = ζ(ψ1, 0)
            p01 = ζ(ψ2, 0)
            p10 = ζ(ψ1, 1)
            p11 = ζ(ψ2, 1)
            corner = (1 - u)*(1 - v)*p00 + u*(1 - v)*p10 + u*v*p11 + (1 - u)*v*p01

            Q_point = ψ_point + ξ_point - corner
            points.append(tuple(Q_point))

    return points


def plot_curves(curves: list, points: list=None):
    plt.figure(figsize=(8, 6))
    
    for label, curve_points in curves.items():
        x, y = zip(*curve_points)
        plt.plot(x, y, marker='o', linestyle='-', markersize=3, label=label)
    
    if points:
        x, y = zip(*points)
        plt.scatter(x, y, c='red', marker='x', label='Quad vertex')
    
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Mesh")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python main.py <subdivisions> <input_file> <output_file>")
        sys.exit(1)

    subdivisions = int(sys.argv[1])
    input_file   = str(sys.argv[2])
    output_file  = str(sys.argv[3])

    script_dir   = os.path.dirname(os.path.abspath(__file__))
    infile_path  = os.path.join(script_dir, input_file)
    outfile_path = os.path.join(script_dir, output_file)

    curves = { 
        "ψ1" : [],
        "ψ2" : [],
        "ξ1" : [],
        "ξ2" : []
    }

    with open(infile_path, 'r') as file:
        for curve in curves:
            n = int(file.readline())
            for _ in range(n):
                line = file.readline()
                point = tuple(map(float, line.split()))
                curves[curve].append(point)

    points = bilinear_projector(curves, subdivisions)

    with open(outfile_path, 'w') as file:
        file.write(f"{len(points)}\n")
        for x, y in points:
            file.write(f"{x} {y}\n")
    
    plot_curves(curves, points)