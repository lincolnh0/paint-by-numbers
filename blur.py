import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy import misc
import scipy.ndimage as ndimage


im = np.array(Image.open('paint_xtina.jpeg'))
result = ndimage.uniform_filter(im, size=(2, 2, 1))
plt.imshow(result)
plt.axis('off')
plt.savefig('pbx.jpeg', bbox_inches='tight')
plt.show()