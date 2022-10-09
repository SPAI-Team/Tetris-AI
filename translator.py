from subprocess import Popen, check_output, check_call, PIPE, call, run, STDOUT
from config import *
import ctypes	
import os
import sys
import pyautogui
import numpy as np

class Translator():
    def __init__(self):
        self.piece_detail = {
            'I': {
                'id': 0,
                'x_bias': -3,
                'rotation_bias': 0
            },
            'O': {
                'id': 1,
                'x_bias': -3,
                'rotation_bias': 0
            },
            'L': {
                'id': 2,
                'x_bias': -2,
                'rotation_bias': 2
            },
            'J': {
                'id': 3,
                'x_bias': -2,
                'rotation_bias': 2
            },
            'T': {
                'id': 4,
                'x_bias': -2,
                'rotation_bias': 2
            },
            'S': {
                'id': 5,
                'x_bias': -2,
                'rotation_bias': 0
            },
            'Z': {
                'id': 6,
                'x_bias': -2,
                'rotation_bias': 0
            }
        }

    def encode_details(self, board, current_piece, next_piece):
        encoded_board = ''
        for i in range(20):
            for j in range(10):
                encoded_board += str(board[i][j])
        cur = self.piece_detail[current_piece]['id']
        nex = self.piece_detail[next_piece]['id']
        return f'{encoded_board}|{NES_LEVEL}|1|{cur}|{nex}|X...|'

    def get_best_move(self, board, current_piece, next_piece):
        encoded = self.encode_details(board, current_piece, next_piece)
        p = run(
            ['cpp_modules/src/main.exe'],
            stdout=PIPE,
            input=encoded,
            encoding='ascii'
        )
        result = p.stdout.rstrip('\n')
        rotation, x_move, _ = list(map(int, result.split('|')))
        x_move += self.piece_detail[current_piece]['x_bias']
        rotation += self.piece_detail[current_piece]['rotation_bias']
        return x_move, rotation

    def perform_move(self, x_move, rotation):
        multiplier = 0.01
        if rotation < 0:
            pyautogui.press('z', presses = abs(rotation), interval=np.random.random() * multiplier)
        else:
            pyautogui.press('up', presses = abs(rotation), interval=np.random.random() * multiplier)
        
        if x_move < 0:
            pyautogui.press('left', presses = abs(x_move), interval=np.random.random() * multiplier)
        else:
            pyautogui.press('right', presses = abs(x_move), interval=np.random.random() * multiplier)
        
        pyautogui.press('space')

    # def pass_info(board):
    #     pass



# cur = ""
# p = run(['cpp_modules/src/main.exe'], stdout=PIPE,
#         input='00000000000000000000000000000000000000000000000000000000000000000011100000001110000000111100000111110000011110000011111100011101110011101110001111111000111111100111111110011111111001111111101111111110|18|4|0|0|X...|', encoding='ascii')
# print(p.stdout)
# for i in range(200):

# p = Popen(['cpp_modules/src/main.exe'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
# grep_stdout = p.communicate(input=b'5')[0]
# print(grep_stdout)
# f.seek(0)
# content = f.read()
# print(content)
# stdout_data = process.communicate(input=b'5')[0]
# print(stdout_data)