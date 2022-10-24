from joblib import Parallel
import numpy as np
from colors import colors, name, next_color


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
		color_val = colors
	elif context == 'next_piece':
		color_val = next_color

	# Find the most probable piece that also fits the color difference threshold
	idx = np.argmin(np.sum(np.abs(colors - np.resize(color, (9, 3))), axis=1))
	best_piece = name[idx]

	if mode == 'gray':
		# Return 1 if it is a valid piece, otherwise 0 (no piece).
		return not (differ(color, np.array([0, 0, 0])) < 10)

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
	a = np.array(a)
	b = np.array(b)
	return np.sum(np.abs(a - b))

def same_color(a: list, b: list, threshold: int = 20):
	'''
	Check if two colors are the same given a difference threshold

	*a* -> the first color
	*b* -> the second color

	*threshold* -> maximum acceptable difference value

	'''
	return differ(a, b) < threshold