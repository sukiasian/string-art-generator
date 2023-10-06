from image_processors._processor import _Processor
import numpy as np
from PIL import Image, ImageDraw


class Shape_Processor(_Processor): 
	output_URL = 'src/assets/cropped.png'

	def __init__(self, enhanced_url): 
		self.enhanced_url = enhanced_url


	def process(self): 
		
		img = Image.open(self.enhanced_url)
		height, width = img.size

		lum_img = Image.new('L', [height, width], 0)
		
		draw = ImageDraw.Draw(lum_img)
		draw.pieslice(
			[
				(0,0), 
				(height,width)
			], 
			0, 
			360, 
			fill = 255, 
			outline = "white"
		)
		
		img_arr = np.array(img)
		lum_img_arr = np.array(lum_img)

		final_img_arr = np.dstack((img_arr, lum_img_arr))

		final = Image.fromarray(final_img_arr)
		final.save(self.output_URL)

		
	


