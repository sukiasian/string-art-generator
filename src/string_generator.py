import numpy as np
import math
from PIL import Image
from random import randint
from bresenham import bresenham


image = Image.open('src/assets/cropped.png').convert('L').resize((100,  100))

image_matrix = np.array(image)

sample_factor = 4
supersampling = image_matrix.shape[0] * sample_factor

image_negative = 1 - image_matrix
image_matrix_normalized = image_negative / 255

def get_supersampled_canvas():
  return np.zeros((supersampling, supersampling))


def downsample(matrix):
  rows_downsampled = matrix.shape[0] // sample_factor
  cols_downsampled = matrix.shape[1] // sample_factor

  blocks = matrix.reshape(rows_downsampled, sample_factor, cols_downsampled, sample_factor)

  matrix_downsampled = np.mean(blocks, axis=(1, 3))

  return matrix_downsampled

pins_amount = 240
angle_between_pins = 360 / pins_amount
radius_supersampled = supersampling / 2

pins_coordinates = np.empty((240, 2))


def to_radian(angle):
	return (math.pi * angle) / 180


def get_x_0(angles):
	return radius_supersampled * np.cos(angles)


def get_y_0(angles):
	return radius_supersampled * np.sin(angles)


def set_pins_coordinates():
	angles = np.arange(240) * angle_between_pins
	angles_radians = np.radians(angles)

	pins_coordinates[:, 0] = get_x_0(angles_radians) + radius_supersampled
	pins_coordinates[:, 1] = get_y_0(angles_radians) + radius_supersampled


set_pins_coordinates()

bresenham_cache = {}

def get_bresenham(i):
  x0, y0 = pins_coordinates[latest_pin]
  x1, y1 = pins_coordinates[i]

  x0 = math.floor(x0) - 1
  y0 = math.floor(y0) - 1
  x1 = math.floor(x1) - 1
  y1 = math.floor(y1) - 1

  key = tuple(sorted([(x0, y0), (x1, y1)]))

  if key not in bresenham_cache:
        bresenham_cache[key] = np.array(list(bresenham(x0, y0, x1, y1)))

  return bresenham_cache[key]


# Number of edges
strings_number = 0

# Tracking the pins posiotions
initial_pin = randint(5, 50)
latest_pin = initial_pin


# writing the results of pins at iterations to have the sequence then
with open('output.txt', 'a') as f:
	f.write(f'{latest_pin}, ')


# Getting the initial pin's position in a matrix - by flooring. I think we can use both latest or initial pin since up to this point they are equal
x0, y0 = np.floor(pins_coordinates[latest_pin]).astype(int)

latest_error = 3000
iteration_error = 2000

number_of_edges = 0
main_canvas = get_supersampled_canvas()


class Pin_Network: 
	def __init__(self, pins):
		self.connections = { pin: set() for pin in range(pins)}


	def add_connection(self, pin1, pin2): 
		if pin2 not in self.connections[pin1] and pin1 not in self.connections[pin2]: 
			self.connections[pin1].add(pin2)
			self.connections[pin2].add(pin1)

	
	def is_connected(self, pin1, pin2): 
		return pin2 in self.connections[pin1] and pin1 in self.connections[pin2]


pin_network = Pin_Network(pins_amount)


while True:
	print(number_of_edges, latest_error)
	if iteration_error < latest_error:
		latest_error = iteration_error

		best_pin_number = None

		lowest_error_step_canvas = None

		for i in range(pins_amount):
			# find the lowest error when connecting latest_pin to i pin

			# all steps work on this canvas
			copy_of_main_canvas = main_canvas.copy()

			if i != latest_pin:
				bresenham_points = get_bresenham(i)

				x_coordinates, y_coordinates = bresenham_points[:, 0], bresenham_points[:, 1]
								
				x_max, y_max = copy_of_main_canvas.shape 

				x_coord_plus_1_mask = (x_coordinates + 1) < x_max
				y_coord_plus_1_mask = (y_coordinates + 1) < y_max 

				exact_increment = 0.1
				near_increment = 0.05
				diagonal_increment = 0.01

				# pixel
				copy_of_main_canvas[x_coordinates, y_coordinates] = np.minimum(1, copy_of_main_canvas[x_coordinates, y_coordinates] + 0.2)
				
				step_error = np.linalg.norm(downsample(copy_of_main_canvas) - image_matrix_normalized)
				
				# when found better point
				if step_error < iteration_error and not pin_network.is_connected(i, latest_pin):
					best_pin_number = i
					iteration_error = step_error

					# Saved the best canvas
					lowest_error_step_canvas = copy_of_main_canvas.copy()

		pin_network.add_connection(latest_pin, best_pin_number)

		latest_pin = best_pin_number
		number_of_edges += 1
		# update canvas
		main_canvas = lowest_error_step_canvas.copy()

		with open('output.txt', 'a') as f:
			f.write(f'{latest_pin}, ')

	else:
		break

