import ctypes	
import os
import sys

dirname = os.path.dirname(sys.argv[0])
dll = ctypes.CDLL(dirname + "\\cpp_modules\\src\\main.so")
# pathToWin32Environment = os.getcwd() + "/environment-win32/libmagic/"
# pathToDll = pathToWin32Environment + "magic1.dll"
# if not os.path.exists(pathToDll):
#     #Give up if none of the above succeeded:
#     raise Exception('Could not locate ' + pathToDll)
# curr_dir_before = os.getcwd()
# os.chdir(pathToWin32Environment)
# libmagic = ctypes.CDLL('magic1.dll')

# test = open('C:/Users/kenne/Documents/GitHub/tetris-ai/cpp_modules/src/masdf.so', 'r')

# class Translator():
# 	def __init__():
# 		pass
	
# 	def assess(self, board, piece, next_piece):
		
# 		pass
# class Translator():
# 	def __init__():
# 		pass
	
# 	def assess(self, board, piece, next_piece):
		
# 		pass
