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
