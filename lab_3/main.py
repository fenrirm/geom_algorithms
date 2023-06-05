import matplotlib.pyplot as plt
import math


def dustance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def closest_pair(points):

    def divide_and_conquer(points):
        n = len(points)
        if n <= 3:
            return simple_finding(points)

        mid = n // 2
        mid_point = points[mid]

        left_points = points[:mid]
        right_points = points[mid:]

        min_dist_left = divide_and_conquer(left_points)
        min_dist_right = divide_and_conquer(right_points)

        min_dist = min(min_dist_left, min_dist_right)

        array = []
        for point in points:
            if abs(point[0] - mid_point[0]) < min_dist:
                array.append(point)

        return min(min_dist, closest_in_array(array, min_dist))

    def simple_finding(points):
        min_dist = float('inf')
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = dustance(points[i], points[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    def closest_in_array(array, min_dist):
        min_dist_strip = min_dist
        array.sort(key=lambda point: point[1])
        for i in range(len(array)):
            j = i + 1
            while j < len(array) and (array[j][1] - array[i][1]) < min_dist_strip:
                dist = dustance(array[i], array[j])
                min_dist_strip = min(dist, min_dist_strip)
                j += 1
        return min_dist_strip

    points.sort()
    return divide_and_conquer(points)


def plot_points(points, closest_pair_points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    plt.scatter(x, y, color='blue')
    plt.scatter([closest_pair_points[0][0], closest_pair_points[1][0]],
                [closest_pair_points[0][1], closest_pair_points[1][1]], color='yellow')

    plt.plot([closest_pair_points[0][0], closest_pair_points[1][0]],
             [closest_pair_points[0][1], closest_pair_points[1][1]], color='yellow')

    plt.show()


points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4), (20, 20), (30, 25), (35, 40), (15, 40), (20, 45), (30, 5), (32, 6), (30,5.5), (35, 10)]
closest_pair_points = []

closest_dist = closest_pair(points)

for i in range(len(points)):
    for j in range(i + 1, len(points)):
        if dustance(points[i], points[j]) == closest_dist:
            closest_pair_points.append(points[i])
            closest_pair_points.append(points[j])
            break

plot_points(points, closest_pair_points)
