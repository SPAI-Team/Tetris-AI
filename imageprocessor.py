import cv2
from joblib import Parallel, delayed
import numpy as np
from PIL import ImageGrab
from config import *
import time
import copy
from utils import *
import math

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
	
		mid = int((coords['top_left'][0] + coords['top_right'][0]) / 2)
		bottom_y = 0
		for j in range(y_len - 1, 0, -1):
			if gray[j][mid] == white:
				bottom_y = j
				break
		# img_copy = copy.deepcopy(img)

		coords['bottom_right'] = [coords['top_right'][0], bottom_y]

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

	def quick_setup(self):
		img = np.array(ImageGrab.grab(bbox=self.coords))
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		dim, x_len, y_len = img.shape[::-1]
		self.x_len = x_len
		self.y_len = y_len
		
		self.board_start = [int(BOARD_RATIO[0][0] * self.x_len), int(BOARD_RATIO[0][1] * self.y_len)]
		self.board_end = [int(BOARD_RATIO[1][0] * self.x_len), int(BOARD_RATIO[1][1] * self.y_len)]

		self.block_size = int(
			np.mean([
				(self.board_end[1] - self.board_start[1]) / 20,
				(self.board_end[0] - self.board_start[0]) / 10
			])
		)
		self.half_block = int(self.block_size / 2)

	def wait_go(self):
		img = np.array(ImageGrab.grab(bbox=self.coords))
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		go_y = int((317 / 676) * self.y_len)
		go_x = list(map(int, [
			(264 / 646) * self.x_len,
			(288 / 646) * self.x_len,
			(345 / 646) * self.x_len,
			(414 / 646) * self.x_len
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

	def fill_board(self, img, i, j, board):
		i_block = math.floor((i - self.board_start[0]) / self.block_size)
		j_block = math.floor((j - self.board_start[1]) / self.block_size)
		board[j_block][i_block] = int(get_piece(img[j][i], mode='gray', threshold=120))

	def get_board(self, img, empty_board = False):
		board = np.full((20, 10), 0)

		if (empty_board):
			extra = self.block_size * 9
		else:
			extra = 0
		
		start = time.time()
		Parallel(n_jobs = -1, require='sharedmem')(delayed(self.fill_board)(img, i, j, board)
			for i in range(self.half_block + self.board_start[0], self.board_end[0], self.block_size)
			for j in range(self.half_block + self.board_start[1] + self.block_size * 1 + extra, self.board_end[1], self.block_size)
		)
		print('get board parallel', time.time() - start)
				# for dis in range(-2, 3):
				# 	for dis_y in range(-2, 3):
				# 		copying[j + dis][i + dis_y] = [255, 0, 0]
				# i_block = math.floor((i - self.board_start[0]) / self.block_size)
				# j_block = math.floor((j - self.board_start[1]) / self.block_size)
				# board[j_block][i_block] = int(get_piece(img[j][i], mode='gray', threshold=120))
		
		# cv2.imwrite('./board.jpg', copying)
		# cv2.waitKey(0)
		# if True:
		# 	for row in self.board:
		# 		print("".join(list(map(str, row))))
		return board

		## Current Piece
	
	def get_cur(self, img):
		## Cur Piece
		pieces = []
		for piece_coord in CUR_RATIO:
			extracted_piece = get_piece(img[int(piece_coord[1] * self.x_len)][int(piece_coord[0] * self.x_len)], context='next_piece', threshold=120)
			pieces.append(None if extracted_piece == 'X' else extracted_piece)

		# cv2.imwrite('./current.jpg', copying)
		# cv2.waitKey(0)
		piece = None
		for p in pieces:
			piece = piece or p
		if piece == None:
			piece = 'I'

		# print('piece:',piece)
		return piece

	def extract_piece(self, piece_coord, img):
		p_y = int(piece_coord[1] * self.y_len)
		p_x = int(piece_coord[0] * self.x_len)
		extracted_piece = get_piece(img[p_y][p_x], context='next_piece', threshold=120)
		return None if extracted_piece == 'X' else extracted_piece
			
	def get_next(self, img):
		## Next Piece
		start = time.time()
		next_pieces = Parallel(n_jobs = -1, require='sharedmem')(
			delayed(self.extract_piece)(piece_coord, img) for piece_coord in NEXT_RATIO
		)
		print('get next parallel', time.time() - start)
		# cv2.imwrite(f'./next{time.time()}.jpg', copying)
		# cv2.waitKey(0)
		next_piece = None
		for p in next_pieces:
			next_piece = next_piece or p
		if next_piece == None:
			next_piece = 'I'
		
		return next_piece