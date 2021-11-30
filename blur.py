import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from PIL import Image
from scipy import misc
from scipy.ndimage import gaussian_filter

im = np.array(Image.open("examples/output/paint_bruno.jpg"))
result = ndimage.uniform_filter(im, size=(2, 2, 1))
plt.imshow(result)
plt.axis("off")
plt.savefig("pbx.jpeg", bbox_inches="tight")
plt.show()
