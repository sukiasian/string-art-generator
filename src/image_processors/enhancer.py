from os import environ, path
from image_processors._processor import _Processor	
import json
import requests

class Enhancer(_Processor):
	output_URL = 'src/assets/enhanced.jpg'
	
	def __init__(self, grayscaled_URL=''): 
		self.grayscaled_URL = grayscaled_URL 


	def send_image_to_enhancement(self): 
		with open(self.grayscaled_URL, 'rb') as f:
		# try except 
			res = requests.post(
				url='https://api.deepai.org/api/torch-srgan', 
				files={'image': f}, 
				headers={ 'api-key': environ.get('DEEP_AI_API_KEY') }
			)
		
		return res.json()['output_url']



	def get_and_save_enhanced_image(self, url = ''): 
		res = requests.get(url)
		# res = requests.get('https://api.deepai.org/job-view-file/0a39e813-832a-4d75-8179-d763c24362ed/outputs/output.jpg')
		
		with open(self.output_URL, 'wb') as f: 
			f.write(res.content)
	

	def process(self): 
		enhanced_image_url = self.send_image_to_enhancement()

		self.get_and_save_enhanced_image(enhanced_image_url)



# убрать цвет - улучшить - сделать круглым ( в последнюю очередь )