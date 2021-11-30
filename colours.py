import random
from collections import defaultdict, deque

import numpy as np


class ColourPixel(object):
    """
    Represents a pixel by its RGB values.
    """

    def __init__(self, pixel, row=None, col=None):
        """
        Class constructor.
        """
        self.red = int(pixel[0])
        self.green = int(pixel[1])
        self.blue = int(pixel[2])
        self.r = row
        self.c = col

    @staticmethod
    def distance(point_a, point_b):
        """
        Calculates distance between two points.
        """
        if isinstance(point_a, ColourPixel) and isinstance(point_b, ColourPixel):
            return np.sqrt(
                (point_a.red - point_b.red) ** 2
                + (point_a.blue - point_b.blue) ** 2
                + (point_a.green - point_b.green) ** 2
            )

    def __sub__(self, x):
        """
        Subtract operator.
        """
        if isinstance(x, ColourPixel):
            return ColourPixel(
                [self.red - x.red, self.green - x.green, self.blue - x.blue]
            )
        else:
            return ColourPixel([self.red - x, self.green - x, self.blue - x])

    def __truediv__(self, x):
        """
        Divide operator.
        """
        return ColourPixel([self.red / x, self.green / x, self.blue / x])

    def __add__(self, x):
        """
        Add operator.
        """
        if isinstance(x, ColourPixel):
            return ColourPixel(
                [self.red + x.red, self.green + x.green, self.blue + x.blue]
            )
        else:
            return ColourPixel([self.red + x, self.green + x, self.blue + x])

    def __eq__(self, x):
        """
        Compares if two pixels have the same values.
        """
        if isinstance(x, ColourPixel):
            return self.red == x.red and self.green == x.green and self.blue == x.blue
        else:
            return NotImplemented

    def __repr__(self):
        """
        Returns a string that prints own RGB values.
        """
        return str((self.red, self.green, self.blue))


class ColourCluster(object):
    """
    Stores a list of colour pixels.
    """

    def __init__(self, points=[], default=None):
        """
        Class constructor.
        """
        self.pixels = deque(points)
        self.default = default

    def append(self, x):
        """
        Adds new pixels to cluster.
        """
        if isinstance(x, ColourPixel):
            self.pixels.append(x)

    def __repr__(self):
        """
        Returns a string with own mean value.
        """
        return f"<ColourCluster @{ self.mean_value }>"

    def clear_cluster_keep_position(self):
        """
        Updates self default and removes all pixels assigned to this.
        """
        if len(self.pixels) > 0:
            self.update_average()
            self.pixels.clear()

    def update_average(self):
        if len(self.pixels) > 0:
            total_pixels = len(self.pixels)
            red_average, green_average, blue_average = (
                int(sum([x.red for x in self.pixels]) / total_pixels),
                int(sum([x.green for x in self.pixels]) / total_pixels),
                int(sum([x.blue for x in self.pixels]) / total_pixels),
            )

            self.default = ColourPixel([red_average, green_average, blue_average])

    @property
    def mean_value(self):
        """
        Returns the mean of all pixels in this cluster.
        """
        return self.default


def create_clusters(count):
    """
    Create count ^ 3 clusters equally apart in the colour space.
    """
    clusters = deque()
    for r in range(count):
        for g in range(count):
            for b in range(count):
                red = 0 if r == 0 else 255 / r
                green = 0 if g == 0 else 255 / g
                blue = 0 if b == 0 else 255 / b
                clusters.append(ColourCluster([], ColourPixel([red, green, blue])))

    return clusters


def create_random_clusters(count):
    """
    Create x clusters randomly in the colour space.
    """
    clusters = deque()
    for i in range(count):
        red, green, blue = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        clusters.append(ColourCluster([], ColourPixel([red, green, blue])))

    return clusters


def get_closest_cluster(point, clusters):
    """
    Return the closest cluster from the given point in the given list of clusters.
    """
    distance = defaultdict(ColourCluster)
    if isinstance(point, ColourCluster):
        point = point.defaults

    for cluster in clusters:
        distance[ColourPixel.distance(cluster.mean_value, point)] = cluster

    return distance[min(distance.keys())], min(distance.keys())
