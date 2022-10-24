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

		self.coords = [None, None, None, None]
		self.abs_c = [None, None, None, None]
		self.capturing = [False]

		self.locate = ScreenLocate(self, self.coords, self.capturing)

		status_title = ct.CTkLabel(self, text = 'Status:', text_font='monospace')
		status_title.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

		self.status = ct.CTkLabel(self, text = self.statuses[0][0], text_color = self.statuses[0][1])
		self.status.place(relx = 0.5, rely = 0.144, anchor = tk.CENTER)

		self.screen_locate_button = ct.CTkButton(self, text='Screen Locate', command=self.screen_locate)
		self.screen_locate_button.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

		self.start = False

		self.show_locate = ct.CTkButton(self, text='Show Locate', command=self.get_locate)
		self.show_locate.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)

		self.button = ct.CTkButton(self,text="Start",command=self.play_toggle, fg_color=rgb_hack((193, 237, 172)), text_color='black', hover=False)
		self.button.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

		self.set_status('not init')

	def play_toggle(self):
		global run_ai
		self.start = not self.start
		run_ai = self.start
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
			self.screen_locate_button.configure(state = 'normal')
			self.show_locate.configure(state = 'normal')
			self.button.configure(state = 'normal')
		elif state == 'not init':
			self.screen_locate_button.configure(state = 'normal')
			self.show_locate.configure(state = 'disabled')
			self.button.configure(state = 'disabled')
		elif state == 'running':
			self.screen_locate_button['state'] = 'disabled'
	
	def screen_locate(self):
		self.locate.show()
		self.set_status('ready')

	def get_locate(self):
		img = ImageGrab.grab(bbox=self.coords)
		img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
		cv2.imshow('Captured', img)

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

		while run_ai:
			try:
				start = time.time()
				board = img_pro.get_board(img, empty_board = first_time)
				temp = img_pro.get_next(img)
				print("get board and next",time.time() - start)
				start = time.time()

				x_move, rotation = trans.get_best_move(board, piece, next_piece)
				print("c++ run",time.time() - start)

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
				# time.sleep(1 / REFRESH_RATE)
				pyautogui.press('space', presses = 1, interval=0, _pause = False)
				time.sleep(0.05)

				img = np.array(ImageGrab.grab(bbox = coords))
				img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
			except:
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