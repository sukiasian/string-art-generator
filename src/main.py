from PIL import Image, ImageDraw
import numpy as np

a = 'src/assets/initial.jpg'
b = 'src/assets/c.jpg'

im_1 = Image.open(a)

grayscale = im_1.convert('L')

grayscale_image_matrix =  np.array(grayscale)


import generator