# Arguments list
#
# -r            Use randomly placed clusters instead of uniformly distributed.
# -c [number]   Specify the number of randomly placed clusters.
# -f [number]   Specify the number (after being raised to the power of 3) of uniformly distributed clusters.

import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm

from colours import (
    ColourPixel,
    create_clusters,
    create_random_clusters,
    get_closest_cluster,
)

input_file = "examples/bruno.jpg"
output_file = "examples/output/paint_bruno.jpg"
cluster_count = int(sys.argv[sys.argv.index("-c") + 1]) if "-c" in sys.argv else 20
cluster_factor = int(sys.argv[sys.argv.index("-f") + 1]) if "-f" in sys.argv else 3
uniform_clusters = "-r" not in sys.argv

im = np.array(Image.open(input_file))

print(f"Image represented with datatype {im.dtype}")
print(f"Image represented in {im.ndim} dimensions")
print(f"Total number of pixels {im.shape[0] * im.shape[1]}")
print(
    f"Creating {f'{cluster_factor ** 3 } uniform' if uniform_clusters else f'{cluster_count} random'} clusters"
)

if uniform_clusters:
    stock_clusters = create_clusters(cluster_factor)
else:
    stock_clusters = create_random_clusters(cluster_count)

# Super hacky code here to query user input.

count = 0
next_check = 1

while count != next_check:
    count += 1
    total_cluster_distance = 0
    for cluster in stock_clusters:
        cluster.clear_cluster_keep_position()

    print("----------------")
    print(f"Run no. {count}")

    for r, row in tqdm(enumerate(im), initial=0, unit_scale=True):
        for c, column in enumerate(row):
            pixel = ColourPixel(column, r, c)
            closest_cluster, cluster_distance = get_closest_cluster(
                pixel, stock_clusters
            )
            closest_cluster.append(pixel)
            total_cluster_distance += cluster_distance

    distribution = [len(x.pixels) for x in stock_clusters]
    print(f"Clusters count distribution:\n{distribution}")
    cluster_count = len([x for x in distribution if x != 0])
    print(f"Reduced image to {cluster_count} colours.")
    print(
        f"Average distance between pixel and closest cluster:\n{round(total_cluster_distance / sum(distribution), 2)}"
    )

    if count == next_check:
        prompt = input(
            f"Run no. {count} finished.\nPause again after ? runs (0 to cancel): "
        )
        next_check = count + 1 if prompt == "" else count + int(prompt)

output = Image.new("RGB", [im.shape[1], im.shape[0]], 255)
data = output.load()
for cluster in stock_clusters:
    cluster.update_average()
    for pixel in cluster.pixels:
        data[pixel.c, pixel.r] = (
            cluster.mean_value.red,
            cluster.mean_value.green,
            cluster.mean_value.blue,
        )
plt.imshow(output)
# plt.show()

output.save(output_file)

"""
IDEA:
Create colour clusters
Assign pixel to colour cluster
Array of dictionary of cluster to array of pixels position
Apply edge filter to get black lines
Assigns cluster number to spaces between lines

"""
