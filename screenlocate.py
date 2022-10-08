from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import ImageGrab
import cv2
import numpy as np
from imageprocessor import ImageProcessor

class ScreenLocate(QtWidgets.QWidget):
	'''
		Responsible for enabling user to capture the screen
	'''
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

		img_pro = ImageProcessor(self.coords)
		cleaned = img_pro.setup(img)
		for i in range(4):
			self.coords[i] = cleaned[i]