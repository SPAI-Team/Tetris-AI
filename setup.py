from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
import re
import pyautogui
import time
import socket
import random

foods = [
    'AI-Beehoon', 'AI-TehTarik', 'AI-CurryPuff', 'AI-MeeGoreng', 'AI-DuckRice', 'AI-CurryRice',
    'AI-CharSiu', 'AI-HokkienMee', 'AI-BakKutTeh', 'AI-CharKwayTeow', 'AI-ChaiTowKway', 'AI-FishballSoup',
    'AI-KayaToast', 'AI-Meepok', 'AI-AyamPenyet', 'AI-IceKachang', 'AI-MiloDinosaur', 'AI-ChilliGrab',
    'AI-CerealPrawn', 'AI-Banmian', 'AI-ChickenRice', 'AI-Satay', 'AI-OrganSoup', 'AI-PepperCrab',
    'AI-RotiPrata', 'AI-NasiLemak', 'AI-OysterOmelette', 'AI-BakChorMee', 'AI-Laksa', 'AI-Rendang',
    'AI-SambalStingray', 'AI-CurryFishHead', 'AI-HainaneseChicken', 'AI-NgohHiang', 'AI-SambalSotong',
    'AI-KwayChap', 'AI-Cendol', 'AI-DurianPengat', 'AI-Rojak', 'AI-PrawnMee', 'AI-FriedHokkienPrawnMee',
    'AI-CrispySquid', 'AI-CrabBeeHoon', 'AI-FriedCarrotCake', 'AI-OrhLua', 'AI-MeeSiam', 'AI-MeeRebus',
    'AI-ChickenSatay', 'AI-BeefSatay', 'AI-MuttonSatay', 'AI-Popiah', 'AI-ChweeKueh'
]

try: 
	comp_id = int(socket.gethostname().split('-')[1])
except:
	comp_id = random.randint(0, len(foods) - 1)

name = foods[comp_id]

code = re.search("<div><p>(.*)</p></div>", requests.get('http://rentry.co/spaiTetris').text, re.IGNORECASE)

assert code
code = code.group(1)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])

try:
	driver = webdriver.Chrome(executable_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe", options = chrome_options)
except:
	driver = webdriver.Chrome(executable_path = "C:/Program Files/Google/Chrome/Application/chrome.exe", options = chrome_options)

driver.get(f'https://tetr.io/#{code}')


time.sleep(3)
import pygetwindow as gw
win = gw.getWindowsWithTitle('TETR.IO - Google Chrome')[0]

userConfigText = str(open('userConfig.txt', 'r').read())
# print(f'window.localStorage.setItem("userConfig", `{userConfigText}`)')
driver.execute_script(f'''window.localStorage.setItem("userConfig", '{userConfigText}')''')

# local_storage = chrome_local_storage.ChromeLocalStorage(port=9222)
# local_storage.set('tetr.io', 'userConfig', userConfigText)


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