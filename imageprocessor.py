import cv2
import numpy as np
from PIL import ImageGrab
from config import *
import time
import copy
from utils import *

class ImageProcessor():
	'''
		Class responsible for extracting information from raw screen captures.
	'''
	def __init__(self, coords):
		self.coords = coords 
		self.white = [255, 255, 255]
		pass

	def _get_white(self):
		img = np.array(ImageGrab.grab(bbox=self.coords))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		dim, x_len, y_len = img.shape[::-1]
		gray_white = max(gray.flatten())
		done_loop = False
		a, b = 0, 0
		for j in range(y_len):
			for i in range(x_len):
				if gray[j][i] == gray_white:
					a = i
					b = j
					done_loop = True
					break

			if done_loop:
				break

		return img[b][a]


	def setup(self, img):
		dim, x_len, y_len = img.shape[::-1]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		white = 0
		for j in range(0, y_len):
			for i in range(0, x_len):
				white = max(white, gray[j][i])

		coords = {
			'top_left': [None, None],
			'top_right': [None, None]
		}
		done_loop = False
		for i in range(0, x_len):
			for j in range(0, y_len):
				if gray[j][i] == white:
					coords['top_left'][0] = i
					coords['top_left'][1] = j
					done_loop = True
					break
			if done_loop:
				break
			
		temp = np.array(gray)
		for i in range(x_len - 1, 0, -1):
			if gray[coords['top_left'][1] + 2][i] == white:
				coords['top_right'] = [i, coords['top_left'][1]]
				break

		done_loop = False
		for j in range(y_len - 1, 0, -1):
			for i in range(0, x_len):
				if gray[j][i] == white:
					coords['bottom_right'] = [coords['top_right'][0], j]
					done_loop = True
					break
			if done_loop:
				break

		for dx in range(-2, 3):
			for dy in range(-2, 3):
				temp[coords['top_left'][1] + dy][coords['top_left'][0] + dx] = 255
				temp[coords['bottom_right'][1] + dy][coords['bottom_right'][0] + dx] = 255

		final = [*coords['top_left'], *coords['bottom_right']]
		final[0] += self.coords[0]
		final[1] += self.coords[1]
		final[2] += self.coords[0]
		final[3] += self.coords[1]

		final[1] -= ((final[3] - final[1]) / 20) * 2
		
		self.white = self._get_white()


		return final
	
	def wait_go(self):
		img = np.array(ImageGrab.grab(bbox=self.coords))
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		dim, x_len, y_len = img.shape[::-1]

		go_y = int((345 / 727) * y_len)
		go_x = list(map(int, [
			(251 / 696) * x_len,
			(284 / 696) * x_len,
			(350 / 696) * x_len,
			(416 / 696) * x_len
		]))


		while True:
			img = np.array(ImageGrab.grab(bbox=self.coords))
			img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
			go_check_count = 0
			for val in go_x:
				go_check_count += differ(img[go_y][val], [5, 199, 255]) < 20
			
			if go_check_count >= 3:
				break
			time.sleep(1 / REFRESH_RATE)

		print('first pass')
		
		while True:
			img = np.array(ImageGrab.grab(bbox=self.coords))
			img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
			go_check_count = 0
			for val in go_x:
				go_check_count += differ(img[go_y][val], [0, 0, 0]) < 50
			
			if go_check_count >= 3:
				break
			time.sleep(1 / REFRESH_RATE)

	def analyze(self):
		img = np.array(ImageGrab.grab(bbox=self.coords))
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		dim, x_len, y_len = img.shape[::-1]

		dx = 0
		base_coords = [0, 0]
		
		done_loop = False
		for i in range(x_len):
			for j in range(y_len):
				if (same_color(img[j][i], self.white)):
					base_coords[0] = i
					base_coords[1] = j
					done_loop = True
					break
			if done_loop:
				break
	
		while (same_color(img[base_coords[1]][base_coords[0] + dx], self.white)):
			dx += 1

		board_start = [int(base_coords[0] + dx), int(base_coords[1])]

		while (not same_color(img[base_coords[1] + 3][base_coords[0] + dx], self.white, 120)):
			dx += 1

		board_end = [int(base_coords[0] + dx), y_len - 1]
		if board_end[0] > (390 / 515 * x_len - 1):
			board_end[0] = int(board_end[0] * 0.95)

		img[board_end[1]][board_end[0]] = [255, 0, 0]
		img[board_start[1]][board_start[0]] = [255, 0, 0]
		
		block_size = int(
			np.mean([
				(board_end[1] - board_start[1]) / 20,
				(board_end[0] - board_start[0]) / 10
			])
		)

		copy_img = copy.deepcopy(img)

		board = [[0 for i in range(10)] for j in range(20)]
		for i in range(int(block_size / 2) + board_start[0], board_end[0], block_size):
			for j in range(int(block_size / 2) + board_start[1], board_end[1], block_size):
				i_block = (i - board_start[0]) // block_size
				j_block = (j - board_start[1]) // block_size
				copy_img[j][i] = [255, 0, 0]
				board[j_block][i_block] = int(get_piece(img[j][i], mode='gray', threshold=120))

		## Current Piece
		pieces = []
		for x_dm in range(3, 6):
			p_x = board_start[0] + block_size * x_dm + int(block_size / 2)
			for y_dm in range(2):
				p_y = board_start[1] - block_size * y_dm - int(block_size / 2)
				copy_img[p_y][p_x] = [255, 0, 0]
				extracted_piece = get_piece(img[p_y][p_x])
				pieces.append(None if extracted_piece == 'X' else extracted_piece)

		piece = None
		for p in pieces:
			piece = piece or p
			


		## Next Piece
		next_pieces = []
		for x_dm in range(2, 5):
			p_x = int(board_end[0] + x_dm * block_size + int(block_size / 2) - (5 / 696) * x_len)
			for y_dm in range(2, 4):
				p_y = int(board_start[1] + y_dm * block_size - (4 / 727) * y_len)
				copy_img[p_y][p_x] = [255, 0, 0]
				print(img[p_y][p_x])
				extracted_piece = get_piece(img[p_y][p_x], context='next_piece', threshold=120)
				next_pieces.append(None if extracted_piece == 'X' else extracted_piece)

		# cv2.imshow('img', copy_img)
		# cv2.waitKey(0)
		
		next_piece = None
		for p in next_pieces:
			next_piece = next_piece or p
		if next_piece == None:
			next_piece = 'I'

		print('----------')
		print('Current:', piece, ' | Next:', next_piece)
		for row in board:
			print("".join(list(map(str, row))))