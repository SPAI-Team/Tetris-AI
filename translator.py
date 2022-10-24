import subprocess
import time
from config import *
import os
import pyautogui
import numpy as np

class Translator():
    def __init__(self):
        os.system('g++ cpp_modules/src/main.cpp -o cpp_modules/src/main')
        self.piece_detail = {
            'I': {
                'id': 0,
                'x_bias': -3,
                'rotation_bias': 0,
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
        self.count = 0

    def encode_details(self, board, current_piece, next_piece):
        encoded_board = ''
        for i in range(20):
            for j in range(10):
                encoded_board += str(board[i][j])
        cur = self.piece_detail[current_piece]['id']
        nex = self.piece_detail[next_piece]['id']
        return f'{encoded_board}|{NES_LEVEL}|1|{cur}|{nex}|X...|'

    def get_best_move(self, board, current_piece, next_piece):
        if self.count % 200 == 0:
            self.p = subprocess.Popen('cpp_modules/src/main.exe',
                                stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
            count = 0
        count += 1
        encoded = self.encode_details(board, current_piece, next_piece)
        self.p.stdin.write('{}\n'.format(encoded).encode('utf-8'))
        self.p.stdin.flush()
        result = self.p.stdout.readline().decode('utf-8').rstrip('\n')
        rotation, x_move, _ = list(map(int, result.split('|')))
        x_move += self.piece_detail[current_piece]['x_bias']
        rotation += self.piece_detail[current_piece]['rotation_bias']
        return x_move, rotation

    # def perform_move(self, x_move, rotation):