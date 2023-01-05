import webbrowser
import requests
import re
import pyautogui
import time
import socket

foods = [
	'AI-Beehoon', 'AI-TehTarik', 'AI-CurryPuff', 'AI-MeeGoreng', 'AI-DuckRice', 'AI-CurryRice',
	'AI-CharSiu', 'AI-HokkienMee', 'AI-BakKutTeh', 'AI-CharKwayTeow', 'AI-ChaiTowKway', 'AI-FishballSoup',
	'AI-KayaToast', 'AI-Meepok', 'AI-AyamPenyet', 'AI-IceKachang', 'AI-MiloDinosaur', 'AI-ChilliGrab',
	'AI-CerealPrawn', 'AI-Banmian', 'AI-ChickenRice', 'AI-Satay', 'AI-OrganSoup', 'AI-PepperCrab'
]

comp_id = int(socket.gethostname().split('-')[1])
name = foods[comp_id]

code = re.search("<div><p>(.*)</p></div>", requests.get('http://rentry.co/spaiTetris').text, re.IGNORECASE)

assert code
code = code.group(1)

webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s &").open(f"tetr.io/#{code}")
time.sleep(2)

import pygetwindow as gw
win = gw.getWindowsWithTitle('TETR.IO - Google Chrome')[0]
if not win.isMaximized:
	win.maximize()
time.sleep(1)
pyautogui.moveTo(739, 583)
time.sleep(0.5)
pyautogui.click()
pyautogui.write(name)
pyautogui.moveTo(739, 682)
time.sleep(0.5)
pyautogui.click()
pyautogui.moveTo(968, 632)
time.sleep(1)
pyautogui.click()