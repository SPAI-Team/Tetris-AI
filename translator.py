from subprocess import Popen, check_output, check_call, PIPE, call, run, STDOUT
import ctypes	
import os
import sys

class Translator():
    def __init__():
        pass

    def encode_details(board, ):
        pass

    def pass_info():
        pass

os.chdir(
    os.path.abspath(os.path.dirname(__file__))
)


cur = ""
p = run(['cpp_modules/src/main.exe'], stdout=PIPE,
        input='00000000000000000000000000000000000000000000000000000000000000000011100000001110000000111100000111110000011110000011111100011101110011101110001111111000111111100111111110011111111001111111101111111110|18|4|0|0|X...|', encoding='ascii')
print(p.stdout)
for i, v in enumerate("00000000000000000000000000000000000000000000000000000000000000000011100000001110000000111100000111110000011110000011111100011101110011101110001111111000111111100111111110011111111001111111101111111110"):
    if (i % 10 == 0):
        print(cur)
        cur = v
    else:
        cur += v
# for i in range(200):



# p = Popen(['cpp_modules/src/main.exe'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
# grep_stdout = p.communicate(input=b'5')[0]
# print(grep_stdout)
# f.seek(0)
# content = f.read()
# print(content)
# stdout_data = process.communicate(input=b'5')[0]
# print(stdout_data)