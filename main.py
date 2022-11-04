from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import cv2
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import customtkinter as ct
import threading
import time
from translator import Translator
from imageprocessor import ImageProcessor
from screenlocate import ScreenLocate
from config import *
import os
import pyautogui


from utils import *

trans = Translator()
os.chdir(
    os.path.abspath(os.path.dirname(__file__))
)

ct.set_appearance_mode("light")
ct.set_default_color_theme('blue')

run_ai = False

class MainApp(ct.CTk):
	'''
		Main Tkinter App
	'''
	def __init__(self):
		super().__init__()

		self.title("SPAI Project Tetris v0.1")
		self.geometry('300x500')

		self.statuses = [['Not initialized', rgb_hack((100, 100, 100))], ['Ready', rgb_hack((50, 200, 80))], ['Running', rgb_hack((10, 100, 205))]]

		self.coords = np.array(CAPTURE_RATIO).copy()
		self.coords[0] *= 1920
		self.coords[2] *= 1920
		self.coords[1] *= 1080
		self.coords[3] *= 1080
		self.coords = self.coords.tolist()
		self.abs_c = [None, None, None, None]
		self.capturing = [False]

		# self.locate = ScreenLocate(self, self.coords, self.capturing)

		status_title = ct.CTkLabel(self, text = 'Status:', text_font='monospace')
		status_title.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

		self.status = ct.CTkLabel(self, text = self.statuses[0][0], text_color = self.statuses[0][1])
		self.status.place(relx = 0.5, rely = 0.144, anchor = tk.CENTER)

		self.input = ct.CTkEntry(self, placeholder_text="Enter Speed")
		self.input.pack(padx = 20, pady = 10)
		self.input.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)
		

		self.confirm_speed_button = ct.CTkButton(self, text='Confirm Speed', command=self.set_speed)
		self.confirm_speed_button.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)

		self.start = False

		self.button = ct.CTkButton(self,text="Start",command=self.play_toggle, fg_color=rgb_hack((193, 237, 172)), text_color='black', hover=False)
		self.button.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

	def play_toggle(self):
		global run_ai
		self.start = not self.start
		run_ai = self.start
		print(self.coords)
		self.thread_AI(self.coords)
		if self.start:
			self.set_status('running')
			self.button.configure(fg_color = rgb_hack((238, 154, 154)), text="Stop")
		else:
			self.set_status('ready')
			self.button.configure(fg_color = rgb_hack((193, 237, 172)), text="Start")

	def set_status(self, state):
		states = ['not init', 'ready', 'running']
		self.status.configure(text = self.statuses[states.index(state)][0], text_color = self.statuses[states.index(state)][1])
		if state == 'ready':
			self.button.configure(state = 'normal')
		elif state == 'not init':
			self.button.configure(state = 'disabled')

	def set_speed(self):
		self.input.configure(state='disabled', fg_color = rgb_hack((200, 200, 200)))
		self.speed = float(self.input.get())

	def sync_AI(self, coords):
		'''
			Synchronous AI Loop
		'''
		img_pro = ImageProcessor(coords)

		img = np.array(ImageGrab.grab(bbox = coords))
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		img_pro.quick_setup()
		piece = img_pro.get_cur(img)
		next_piece = img_pro.get_next(img)
		img_pro.wait_go()
		first_time = 2
		img = np.array(ImageGrab.grab(bbox = coords))
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

		print(self.speed)
		while run_ai:
			try:
				board = img_pro.get_board(img, empty_board = first_time)
				temp = img_pro.get_next(img)

				x_move, rotation = trans.get_best_move(board, piece, next_piece)

				if first_time > 0:
					first_time -= 1

				piece = next_piece
				next_piece = temp
					
				pause = False
				rotation = rotation % 4
				if abs(rotation - 4) < rotation:
					rotation = rotation - 4

				rot = 'z' if rotation < 0 else 'up'
				mov = 'left' if x_move < 0 else 'right'

				pyautogui.press(rot, presses = abs(rotation), interval=0, _pause=pause)
				pyautogui.press(mov, presses = abs(x_move), interval=0, _pause=pause)
				pyautogui.press('space', presses = 1, interval=0, _pause=pause)
				time.sleep(0.05)
				# time.sleep(max(0.05, 0.55 * (1 / self.speed)))

				img = np.array(ImageGrab.grab(bbox = coords))
				img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
			except:
				self.input.configure(state='normal')
				break
		self.play_toggle()

	def thread_AI(self, coords):
		'''
			Threaded sync_AI to enable non-blocking code. Otherwise, tkinter does not work.
		'''
		if (run_ai):
			t1 = threading.Thread(target = lambda: self.sync_AI(coords))
			t1.start()
		

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)

	main = MainApp()
	main.mainloop()
