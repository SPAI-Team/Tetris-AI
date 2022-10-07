import sys
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

run_ai = False

def rgb_hack(rgb):
	return "#%02x%02x%02x" % rgb  

def sync_AI(coords):
	count = 0
	img_pro = ImageProcessor(None, coords)
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

		self.statuses = [['Not initialized', rgb_hack((100, 100, 100))], ['Waiting for "GO"', rgb_hack((195, 150, 10))], ['Stopped', rgb_hack((230, 60, 70))]] 

		self.coords = [None, None, None, None]
		self.abs_c = [None, None, None, None]
		self.capturing = [False]
		self.locate = ScreenLocate(self, self.coords, self.capturing)

		# self.ai = AISession()

		self.foreground = 'black'
		self.background = 'lightgrey'
		self.text_foreground = 'black'
		self.text_background='white'

		status = ct.CTkLabel(self, text = 'Status:', text_font='monospace')
		status.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

		status = ct.CTkLabel(self, text = self.statuses[0][0], text_color = self.statuses[0][1])
		status.place(relx = 0.5, rely = 0.144, anchor = tk.CENTER)

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
			self.button.configure(fg_color = rgb_hack((238, 154, 154)), text="Stop")
		else:
			self.button.configure(fg_color = rgb_hack((193, 237, 172)), text="Start")
	
	def screen_locate(self):
		self.locate.show()

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
		pass

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

		return final

	def analyze(self):
		img = ImageGrab.grab(bbox=self.coords)
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
		print(len(img))
	

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