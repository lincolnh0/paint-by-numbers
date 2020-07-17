from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from collections import deque, defaultdict
import random

input_file = 'black.jpg'
output_file = 'paint_' + input_file
cluster_count = 20
cluster_factor = 3
run_diff_threshold = 500
uniform_clusters = False

im = np.array(Image.open(input_file))

print(im.dtype)
print(im.ndim)
print(im.shape[0] * im.shape[1])

class ColourPixel(object):
    '''
    Represents a pixel by its RGB values.
    '''

    def __init__(self, pixel, row=None, col=None):
        '''
        Class constrcutor.
        '''
        self.red = int(pixel[0])
        self.green = int(pixel[1])
        self.blue = int(pixel[2])
        self.r = row
        self.c = col

    @staticmethod
    def distance(pointA, pointB):
        '''
        Calculate distance between two points.
        '''
        if isinstance(pointA, ColourPixel) and isinstance(pointB, ColourPixel):
            return np.sqrt((pointA.red - pointB.red) ** 2 + (pointA.blue - pointB.blue) ** 2 + (pointA.green - pointB.green) ** 2)


    def __sub__(self, x):
        '''
        Add attributes.
        '''
        if isinstance(x, ColourPixel):
            return ColourPixel([self.red - x.red, self.green - x.green, self.blue - x.blue])
        else:
            return ColourPixel([self.red - x, self.green - x, self.blue - x])

    def __truediv__(self, x):
        '''
        Divide all attribute by x.
        '''
        return ColourPixel([self.red / x, self.green / x, self.blue / x])

    def __add__(self, x):
        '''
        Add attributes.
        '''
        if isinstance(x, ColourPixel):
            return ColourPixel([self.red + x.red, self.green + x.green, self.blue + x.blue])
        else:
            return ColourPixel([self.red + x, self.green + x, self.blue + x])

    def __eq__(self, x):
        '''
        Compare if two pixels have the same values.
        '''
        if isinstance(x, ColourPixel):
            return self.red == x.red and self.green == x.green and self.blue == x.blue
        else:
            return NotImplemented

    def __repr__(self):
        '''
        Retuns a string that prints own RGB values.
        '''
        return str((self.red, self.green, self.blue))

class ColourCluster(object):
    '''
    Stores a list of colour pixels.
    '''
    def __init__(self, points=[], default=None):
        '''
        Class constrcutor.
        '''
        self.pixels = deque(points)
        self.default = default

    def append(self, x):
        '''
        Add new pixels to cluster.
        '''
        if isinstance(x, ColourPixel):
            self.pixels.append(x)



    def __repr__(self):
        '''
        Returns a string with own mean value.
        '''
        return f'<ColourCluster @{ self.mean_value }>'

    def clearClusterKeepPosition(self):
        if len(self.pixels) > 0:
            self.updateAverage()
            self.pixels.clear()

    def updateAverage(self):
        if len(self.pixels) > 0:
            total_pixels = len(self.pixels)
            redAverage, greenAverage, blueAverage = int(sum([x.red for x in self.pixels]) / total_pixels), \
                                                    int(sum([x.green for x in self.pixels]) / total_pixels), \
                                                    int(sum([x.blue for x in self.pixels]) / total_pixels)
            
            self.default = ColourPixel([redAverage, greenAverage, blueAverage])
    @property
    def mean_value(self):
        '''
        Returns the mean of all pixels in this cluster.
        '''
        return self.default


    

def createClusters(count):
    '''
    Create count ^ 3 clusters equally apart in the colour space.
    '''
    clusters = deque()
    for r in range(count):
        for g in range(count):
            for b in range(count):
                red = 0 if r == 0 else 255 / r
                green = 0 if g == 0 else 255 / g
                blue = 0 if b == 0 else 255 / b
                clusters.append(ColourCluster([], ColourPixel([red, green, blue])))

    return clusters

def createRandomClusters(count):
    '''
    Create x clusters randomly in the colour space.
    '''
    clusters = deque()
    for i in range(count):
        red, green, blue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        clusters.append(ColourCluster([], ColourPixel([red, green, blue])))
    
    return clusters


def getClosestCluster(point, clusters):
    distance = defaultdict(ColourCluster)
    for cluster in clusters:
        distance[ColourPixel.distance(cluster.mean_value, point)] = cluster

    return distance[min(distance.keys())]

if uniform_clusters:
    stock_clusters = createClusters(cluster_factor)
else:
    stock_clusters = createRandomClusters(cluster_count)
distribution = [im.shape[0] * im.shape[1]]
count = 0
next_check = 1
prevMax = run_diff = max(distribution)
while run_diff > run_diff_threshold:
    for cluster in stock_clusters:
        cluster.clearClusterKeepPosition()
    count += 1
    for r, row in enumerate(im):
        print(f'{ round(100 * r/im.shape[0], 2)} %')
        for c, column in enumerate(row):
            pixel = ColourPixel(column, r, c)
            closest_cluster = getClosestCluster(pixel, stock_clusters)
            closest_cluster.append(pixel)
    
    distribution = [len(x.pixels) for x in stock_clusters]
    print(distribution)

    run_diff = prevMax - max(distribution)
    print(f'Cluster reduced by { run_diff } - {run_diff - 30} away from goal.')
    prevMax = max(distribution)

    if count == next_check:
        prompt = input(f'Run no. {count} finished.\nPause again after ? runs: ')
        next_check = count + 1 if  prompt == '' else count + int(prompt)
        if next_check == count: break



output = Image.new('RGB', [im.shape[1], im.shape[0]], 255)
data = output.load()
for cluster in stock_clusters:
    cluster.updateAverage()
    for pixel in cluster.pixels:
        data[pixel.c, pixel.r] = (
            cluster.mean_value.red,
            cluster.mean_value.green,
            cluster.mean_value.blue
        )    
plt.imshow(output)
plt.show()

output.save(output_file)

    
'''
IDEA:
Create colour clusters
Assign pixel to colour cluster
Array of dictionary of cluster to array of pixels position
Apply edge filter to get black lines
Assgin cluster number to spaces between lines

'''