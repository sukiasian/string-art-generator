from image_processors._processor import _Processor
import cv2

# in - img.jpg, out - 

class Grayscale(_Processor): 
	output_URL = 'src/assets/grayscaled.jpg'

	def __init__(self, image_URL): 
		self.image_URL = image_URL

	def process(self): 
		img = cv2.imread(self.image_URL)

		(row, col) = img.shape[0:2]

		for i in range(row):
			for j in range(col):
				img[i, j] = sum(img[i, j]) * 0.33
		
		cv2.imwrite(self.output_URL, img)
		