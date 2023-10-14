from bresenham import bresenham
from random import randint
import math

class String_Generator: 
	pins_coordinates = []
	output = []

	def __init__(self, pins, radius, source_image, iterations = 3000): 
		self.pins = pins
		self.radius = radius
		self.source_image = source_image
		self.iterations = iterations

		self.angle_between_pins = pins / 360

		self.__set_pins_coordinates()
	

	def __to_radian(self, angle): 
		return (math.pi * angle) / 180


	def __get_x_0(self, angle): 
		return self.radius * math.cos(self.__to_radian(angle))
	

	def __get_y_0(self, angle): 
		return self.radius * math.sin(self.__to_radian(angle))


	def __set_pins_coordinates(self): 
		r = self.source_image.shape[0] / 2 

		for i in range(0, self.pins): 
			x = self.__get_x_0(i * self.angle_between_pins) + r
			y = self.__get_y_0(i * self.angle_between_pins) + r

			self.pins_coordinates.append((x, y))

	def __find_unallowed_to_connect_with(self, initial_pin_number):
		indices = []
		
		output = enumerate(self.output)
		output_length = len(self.output)

		for idx, value in output:
			if value == initial_pin_number:
				if idx != output_length - 1: 
					indices.append(self.output[idx + 1])

				if output_length > 2: 
					indices.append(self.output[idx - 1])
				
		return indices
	
	# ???       i = 10
	def __current_pin_to_connect_with_is_allowed(self, initial_pin_number, current_pin_number): 
		""" 
		 
		  Итак, мы отправляем следующую точку. Смотрим, можно ли с ней связаться.
		  Для этого мы должны найти в списке все начальные точки и посмотреть - какие у них предыдущие и следующие индексы.
		  С этими точками нельзя связываться.

		  Далее, берем и сравниваем следующую точку с предыдущей
		   
			 """
		unallowed = self.__find_unallowed_to_connect_with(initial_pin_number)


		try: 
			unallowed.index(current_pin_number)
		except: 
			return True
		
		return False


	def __get_average_intensity(self, initial_pin_number, current_pin_to_connect_with):
		x0, y0 = self.pins_coordinates[initial_pin_number] 
		x1, y1 = self.pins_coordinates[current_pin_to_connect_with]

		bresenham_args = (x0, y0, x1, y1)
		bresenham_args_floored = list(map(lambda coordinate: math.floor(coordinate), bresenham_args))

		intersection_points = list(bresenham(*bresenham_args_floored))

		print(intersection_points, x0, x1)

		intensity = 0

		for x, y in intersection_points:
			avg_color_value_per_pixel = 0

			for color_value in self.source_image[x][y]:  
				avg_color_value_per_pixel += color_value

			intensity += avg_color_value_per_pixel / 3

		return intensity


	def __pin_is_allowed_for_overflowing_offset(self, initial_pin_number, current_pin_number, offset): 
		lower_bound = initial_pin_number - self.pins + offset
		upper_bound = initial_pin_number - offset

		return initial_pin_number + offset > self.pins and (current_pin_number > lower_bound and current_pin_number < upper_bound)
	

	def __pin_is_allowed_for_neutral_offset(self, initial_pin_number, current_pin_number, offset): 
		lower_bound = initial_pin_number - offset
		upper_bound = initial_pin_number + offset

		return initial_pin_number - offset > 0 and (current_pin_number < lower_bound or current_pin_number > upper_bound)
	

	def __pin_is_allowed_for_underflowing_offset(self, initial_pin_number, current_pin_number, offset): 
		lower_bound = initial_pin_number + offset
		upper_bound = self.pins - (offset + initial_pin_number)

		return current_pin_number > lower_bound and current_pin_number < upper_bound

		
	def generate(self): 
		initial_pin_number = randint(1, 100)

		self.output.append(initial_pin_number)

		# should overwrite
		with open ('./output.txt', 'a') as output: 
			output.write(f'{initial_pin_number},')

			output.close()


		for _ in range(0, self.iterations): 
			best_option = { 
				'intensity': 0, 
				'pin_number': 0
			}

			offset = 24

			

			# как так получается, что повторяются 0, 25 ? 
			for j in range(
				0, self.pins
			): 
				check_if_pin_is_in_bounds_args = (initial_pin_number, j, offset)

				# if self.__current_pin_to_connect_with_is_allowed(initial_pin_number, j) and (self.__pin_is_allowed_for_overflowing_offset(*check_if_pin_is_in_bounds_args) or self.__pin_is_allowed_for_neutral_offset(*check_if_pin_is_in_bounds_args) or self.__pin_is_allowed_for_underflowing_offset(*check_if_pin_is_in_bounds_args)): 
				if self.__current_pin_to_connect_with_is_allowed(initial_pin_number, j): 
					# also need to check if number is allowed 
					avg_intensity = self.__get_average_intensity(initial_pin_number, j)

					if avg_intensity > best_option['intensity']: 
						best_option['intensity'] = avg_intensity
						best_option['pin_number'] = j


			with open('./output.txt', 'a') as output: 
				output.write(f'{best_option["pin_number"]}, ')
				
				output.close()		

			initial_pin_number = best_option['pin_number']

			self.output.append(initial_pin_number)



""" 

	1. взять промежуток - до 6000 к примеру, и там решать сколько нитей сделать, высчитывая ошибку
	2.  Брать какой то зазор - если фотография будет лучше выглядеть - то добавить +- n нитей 

"""


			