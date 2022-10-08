import numpy as np
from colors import piece_color, next_piece_color


def rgb_hack(rgb: list):
	"""
	This function converts RGB values into an RGB string, used for tkinter purposes

	*rgb* -> a size-3 list containing the RGB values
	"""
	return "#%02x%02x%02x" % rgb  

def get_piece(color: list, mode: str = 'normal', threshold: int = 60, context: str = 'piece'):
	"""
	Given the color, this function attempts to return the most probable piece that
	the color belongs to

	NOTE: the colors should be in BGR

	*color* -> a size-3 list containing the BGR values

	*mode* 
		-> if mode is "normal", the name of the piece is returned
		-> if mode is "gray", return True if there is a color associated with a piece and False if not.

	*threshold* -> the acceptable difference between two colors, used in determining whether or not they
				   represent the same piece

	*context*
		-> if context is "piece", uses the colors of the pieces on the board
		-> if context is "next_piece", uses the colors of the pieces from the 'next pieces' column.

		This is because the colors of pieces in the 'next' column are different compared to the colors
		of the pieces on the board.
	
	"""

	# Defining which color dicitonary we want
	if context == 'piece':
		color_dict = piece_color
	elif context == 'next_piece':
		color_dict = next_piece_color

	# Find the most probable piece that also fits the color difference threshold
	best_piece = 'X'
	best_dist = 10000
	for k, v in color_dict.items():
		if best_dist > differ(v, color) and differ(v, color) < threshold:
			best_piece = k
			best_dist = differ(v, color)
	
	if mode == 'gray':
		# Return 1 if it is a valid piece, otherwise 0 (no piece).
		return (best_piece != 'X') and not is_gray(color)

	elif mode == 'normal':
		# Return the name of the piece
		return best_piece

def is_gray(color: list):
	'''
	This function checks if the color is grayscale.

	*color* -> a size-3 list
	'''
	return np.mean([
		abs(color[0] - color[1]),
		abs(color[1] - color[2]),
		abs(color[0] - color[2])
	]) < 10

def differ(a: list, b: list):
	'''
	Returns the sum of the absolute differences of each color channel

	*a* -> the first color
	*b* -> the second color
	'''
	total = 0
	for i in range(len(a)):
		total += abs(a[i] - b[i])
	return total

def same_color(a: list, b: list, threshold: int = 20):
	'''
	Check if two colors are the same given a difference threshold

	*a* -> the first color
	*b* -> the second color

	*threshold* -> maximum acceptable difference value

	'''
	return differ(a, b) < threshold