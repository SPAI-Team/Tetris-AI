set PATH=%path%;C:\ProgramData\Anaconda3\condabin;C:\ProgramData\Anaconda3\Scripts;C:\ProgramData\Anaconda3\Library\bin;
set PATH=%path%;C:\cygwin64\bin;
cd C:\Users\Student\Desktop\Tetris-AI-main
call activate base
pip install -r "requirements.txt"
python main.py
pause
call conda deactivate