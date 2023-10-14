# from dotenv import load_dotenv
# from cv2 import imread
# from string_generator import String_Generator
# from image_processors.grayscaler import Grayscale
# from image_processors.enhancer import Enhancer

# load_dotenv()


# # Grayscale('src/assets/cropped.png').process()
# source_image = imread('src/assets/cropped.png')
# bitmap = source_image

# strGenerator = String_Generator(source_image=source_image, pins=240, iterations=3000, radius=32)

# strGenerator.generate()


# from cv2 import imread
# from PIL import Image, ImageDraw
# import numpy as np

# a = 'src/assets/initial.jpg'
# b = 'src/assets/c.jpg'

# im_1 = Image.open(a)

# grayscale = im_1.convert('L')
# print(grayscale.size)


# grayscale_image_matrix =  np.array(grayscale)

# print(len(grayscale_matrix[0]))

import generator