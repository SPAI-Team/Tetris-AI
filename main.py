import win32api
import time
import pyautogui
import numpy as np
import pandas as pd
import cv2
import sys
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui


state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
img = ImageGrab.grab(bbox=(0, 0, 1920, 1080)) #x, y, w, h
img_np = np.array(img)
frame = img_np
frame += 10
app = QtWidgets.QApplication(sys.argv)
QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
while True:

	# cv2.imshow('frame',frame + 30)
	if cv2.waitKey(30) & 0Xff == ord('q'):
		QtWidgets.QApplication.restoreOverrideCursor()
		break
cv2.destroyAllWindows()



# while True:
# 	a = win32api.GetKeyState(0x01)

# 	if a != state_left:  # Button state changed
# 		state_left = a
# 		if a < 0:
# 			print(pyautogui.position())
# 			print('Left Button Pressed')
# 		else:
# 			print(pyautogui.position())
# 			print('Left Button Released')

# 	time.sleep(0.001)

# cv2.destroyAllWindows()

# while True: