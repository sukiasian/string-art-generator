from dotenv import load_dotenv
from cv2 import imread
from string_generator import String_Generator
from image_processors.shape_processor import Shape_Processor
from image_processors.grayscaler import Grayscale
from image_processors.enhancer import Enhancer

load_dotenv()

source_image = imread('src/assets/cropped.png')
bitmap = source_image

strGenerator = String_Generator(source_image=source_image, pins=240, iterations=3000, radius=32)

strGenerator.generate()

import cv2
import numpy as np

def draw_strings_on_rounded_image(image, string_coordinates, color=(255, 255, 255), thickness=1):
    result_image = image.copy()

    for coord in string_coordinates:
        start_point, end_point = coord
        x1, y1 = start_point
        x2, y2 = end_point

        cv2.line(result_image, (x1, y1), (x2, y2), color, thickness)

    return result_image

# Example usage:
image = cv2.imread('src/assets/enhanced.jpg')
string_coordinates = [((100, 100), (200, 200)), ((150, 150), (250, 150))]  # Example coordinates
result_image = draw_strings_on_rounded_image(image, string_coordinates)

cv2.imwrite('output_image_with_strings.jpg', result_image)
cv2.imshow('Output Image with Strings', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()