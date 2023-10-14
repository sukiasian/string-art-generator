from random import randint
from bresenham import bresenham
from PIL import Image
import numpy as np
import math

image_matrix = np.array(Image.open('src/assets/cropped.png').convert('L'))
matrix_size = len(image_matrix)
canvas_matrix = np.zeros((matrix_size, matrix_size))

pins_amount = 240 
pins_coordinates = []

angle_between_pins = 360 / pins_amount
radius = image_matrix.shape[0] / 2

strings_matrix = []

strings_number = 0

initial_pin = randint(5, 50)
latest_pin = initial_pin


""" 


Проблемы:

1. прерывается 
2. слишком медленно 


"""

def to_radian(angle): 
	return (math.pi * angle) / 180

def get_x_0(angle):
	return radius * math.cos(to_radian(angle))
	

def get_y_0(angle): 
	return radius * math.sin(to_radian(angle))

def set_pins_coordinates(): 
	r = image_matrix.shape[0] / 2 

	for i in range(0, pins_amount): 
		x = get_x_0(i * angle_between_pins) + r
		y = get_y_0(i * angle_between_pins) + r

		pins_coordinates.append((x, y))

set_pins_coordinates()

with open('output.txt', 'a') as f: 
	f.write(f'{latest_pin}, ')

# from previous step
latest_error = None
# after step

while (True): 
	iteration_min_error = None
	point_to_move = None
	canvas_matrix_copy = np.copy(canvas_matrix)
	canvas_matrix_final_copy = np.copy(canvas_matrix)

	for i in range(0, 240): 
		
		if i != latest_pin: 
		# 	# высчитать ошибку при каждой итерации 
			x0, y0 = pins_coordinates[latest_pin] 
			x1, y1 = pins_coordinates[i]

			bresenham_points = bresenham(math.floor(x0) - 1, math.floor(y0) - 1, math.floor(x1) - 1, math.floor(y1) - 1)
		# 	# 0.2 for each bresenham point
			for x, y in list(bresenham_points): 
				bresenham_add_value = 255 * 0.2
				# transform bresenham point
				if canvas_matrix_copy[y][x] + bresenham_add_value <= 255:
					canvas_matrix_copy[y][x] += bresenham_add_value

				# transform nearest points 

				if y + 1 < matrix_size and y - 1 >= 0 and x + 1 < matrix_size and x - 1 >= 0:
					nearest_add_value = 255 * 0.1

					if canvas_matrix_copy[y + 1][x] + nearest_add_value <= 255:
						canvas_matrix_copy[y + 1][x] += nearest_add_value

					if canvas_matrix_copy[y - 1][x] + nearest_add_value <= 255:
						canvas_matrix_copy[y - 1][x] += nearest_add_value

					if canvas_matrix_copy[y][x + 1] + nearest_add_value <= 255: 
						canvas_matrix_copy[y][x + 1] += nearest_add_value

					if canvas_matrix_copy[y][x - 1] + nearest_add_value <= 255: 
						canvas_matrix_copy[y][x - 1] += nearest_add_value


			current_step_error = np.linalg.norm(image_matrix - canvas_matrix_copy)

		
		# обнуляет для следующей внутренней итерации. Независимо от результата
				
		#  rewrite best pin to connect with 
		if not iteration_min_error or current_step_error < iteration_min_error:
			iteration_min_error = current_step_error
			point_to_move = i
			canvas_matrix_final_copy = np.copy(canvas_matrix_copy)
			# НЕ нужна матрица которая учитывает другие шаги. нужна только матрица которая учитывает текущий шаг 

		
		canvas_matrix_copy = np.copy(canvas_matrix)


	if latest_error and iteration_min_error > latest_error: 
		print(iteration_min_error, latest_error)
		break

	canvas_matrix = np.copy(canvas_matrix_final_copy)

	latest_error = iteration_min_error
	latest_pin = point_to_move

	with open('output.txt', 'a') as f:
		f.write(f'{point_to_move}, ') 

	++strings_number