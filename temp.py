from itertools import count
import sys
from turtle import done
from unittest import case
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2
import tkinter.ttk as ttk
from tkinter.font import families
import customtkinter as ct
import tkinter.messagebox as msg
import threading
import time

ct.set_appearance_mode("System")
ct.set_default_color_theme('blue')

REFRESH_RATE = 15
DEBUG = False

run_ai = False

def differ(a, b):
	total = 0
	for i in range(len(a)):
		total += abs(a[i] - b[i])
	return total

def same_color(a, b, threshold = 20):
	return differ(a, b) < threshold

piece_color = {
	'L': [43, 114, 230],
	'I': [159, 228, 42], 
	'S': [43, 229, 159],
	'Z': [55, 45, 230],
	'O': [43, 193, 229],
	'J': [207, 59, 84],
	'T': [193, 60, 207],
	'X': [0, 0, 0]
}

def is_gray(color):
	return np.mean([
		abs(color[0] - color[1]),
		abs(color[1] - color[2]),
		abs(color[0] - color[2])
	]) < 5

def get_piece(color, mode = 'normal', threshold = 60):
	best_piece = 'X'
	best_dist = 10000
	for k, v in piece_color.items():
		if best_dist > differ(v, color) and differ(v, color) < 200:
			best_piece = k
			best_dist = differ(v, color)
	
	if mode == 'gray':
		return (best_piece == 'X') and not is_gray(color)
	else:
		return best_piece


def rgb_hack(rgb):
	return "#%02x%02x%02x" % rgb  

def sync_AI(coords):
	img_pro = ImageProcessor(None, coords)
	img_pro.wait_go()
	if (DEBUG):
		img_pro.analyze()
	else:
		while run_ai:
			img_pro.analyze()
			time.sleep(1 / REFRESH_RATE)

def thread_AI(coords):
	t1 = threading.Thread(target = lambda: sync_AI(coords))
	t1.start()

class MainApp(ct.CTk):
	def __init__(self):
		super().__init__()

		self.title("SPAI Tetris Bot v0.1")
		self.geometry('300x500')

		self.statuses = [['Not initialized', rgb_hack((100, 100, 100))], ['Ready', rgb_hack((50, 200, 80))], ['Running', rgb_hack((10, 100, 205))]]

		self.coords = [None, None, None, None]
		self.abs_c = [None, None, None, None]
		self.capturing = [False]
		self.locate = ScreenLocate(self, self.coords, self.capturing)

		# self.ai = AISession()

		self.foreground = 'black'
		self.background = 'lightgrey'
		self.text_foreground = 'black'
		self.text_background='white'

		status_title = ct.CTkLabel(self, text = 'Status:', text_font='monospace')
		status_title.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

		self.status = ct.CTkLabel(self, text = self.statuses[0][0], text_color = self.statuses[0][1])
		self.status.place(relx = 0.5, rely = 0.144, anchor = tk.CENTER)

		button = ct.CTkButton(self, text='Screen Locate', command=self.screen_locate)
		button.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

		self.start = False

		other = ct.CTkButton(self, text='Show Locate', command=self.get_locate)
		other.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)

		self.button = ct.CTkButton(self,text="Start",command=self.play_toggle, fg_color=rgb_hack((193, 237, 172)), text_color='black', hover=False)
		self.button.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

	def play_toggle(self):
		global run_ai
		self.start = not self.start
		run_ai = self.start
		thread_AI(self.coords)
		if self.start:
			self.set_status('running')
			self.button.configure(fg_color = rgb_hack((238, 154, 154)), text="Stop")
		else:
			self.set_status('ready')
			self.button.configure(fg_color = rgb_hack((193, 237, 172)), text="Start")

	def set_status(self, state):
		states = ['not init', 'ready', 'running']
		self.status.configure(text = self.statuses[states.index(state)][0], text_color = self.statuses[states.index(state)][1])
	
	def screen_locate(self):
		self.locate.show()
		self.set_status('ready')

	def get_locate(self):
		img = ImageGrab.grab(bbox=self.coords)
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
		cv2.imshow('Captured', img)
	
class AISession():
	def __init__(self):
		img = ImageGrab.grab(bbox=self.coords)

	def reset(self):
		pass

	def start(self):
		sleep_time = 1 / REFRESH_RATE

	def stop(self):
		pass


class ImageProcessor():
	def __init__(self, img, coords):
		self.img = img
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


	def setup(self):
		dim, x_len, y_len = self.img.shape[::-1]
		gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
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

		board = [[0 for i in range(10)] for j in range(20)]
		for i in range(int(block_size / 2) + board_start[0], board_end[0], block_size):
			for j in range(int(block_size / 2) + board_start[1], board_end[1], block_size):
				i_block = (i - board_start[0]) // block_size
				j_block = (j - board_start[1]) // block_size
				board[j_block][i_block] = int(get_piece(img[j][i], mode='gray'))

		## Current Piece
		pieces = []
		for x_dm in range(3, 6):
			p_x = board_start[0] + block_size * x_dm + int(block_size / 2)
			for y_dm in range(2):
				p_y = board_start[1] - block_size * y_dm - int(block_size / 2)
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
				# img[p_y][p_x] = [255, 0, 0]
				print(img[p_y][p_x])
				extracted_piece = get_piece(img[p_y][p_x])
				next_pieces.append(None if extracted_piece == 'X' else extracted_piece)
		
		next_piece = None
		for p in next_pieces:
			next_piece = next_piece or p

		print('----------')
		print('Current:', piece, ' | Next:', next_piece)
		for row in board:
			print("".join(list(map(str, row))))




class ScreenLocate(QtWidgets.QWidget):
	def __init__(self, root, coords, capturing):
		super().__init__()
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()
		self.coords = coords
		self.setGeometry(0, 0, screen_width, screen_height)
		self.capturing = capturing
		self.capturing[0] = True
		self.setWindowTitle(' ')
		self.begin = QtCore.QPoint()
		self.end = QtCore.QPoint()
		self.setWindowOpacity(0.3)
		QtWidgets.QApplication.setOverrideCursor(
			QtGui.QCursor(QtCore.Qt.CrossCursor)
		)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

	def paintEvent(self, event):
		qp = QtGui.QPainter(self)
		qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
		qp.setBrush(QtGui.QColor(128, 128, 255, 128))
		qp.drawRect(QtCore.QRect(self.begin, self.end))

	def mousePressEvent(self, event):
		self.begin = event.pos()
		self.end = self.begin
		self.update()

	def mouseMoveEvent(self, event):
		self.end = event.pos()
		self.update()

	def mouseReleaseEvent(self, event):
		self.close()

		self.coords[0] = min(self.begin.x(), self.end.x())
		self.coords[1] = min(self.begin.y(), self.end.y())
		self.coords[2] = max(self.begin.x(), self.end.x())
		self.coords[3] = max(self.begin.y(), self.end.y())
		self.capturing[0] = False

		img = ImageGrab.grab(bbox=self.coords)
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		img_pro = ImageProcessor(img, self.coords)
		cleaned = img_pro.setup()
		for i in range(4):
			self.coords[i] = cleaned[i]

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	main = MainApp()
	main.mainloop()