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

webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(f"tetr.io/#{code}")
time.sleep(2)

import pygetwindow as gw
win = gw.getWindowsWithTitle('TETR.IO - Google Chrome')[0]
if not win.isMaximized:
	win.maximize()
time.sleep(1)
win.activate()
pyautogui.moveTo(1781, 957)
config = '{"controls":{"style":"guideline","custom":{"moveLeft":[],"moveRight":[],"softDrop":[],"hardDrop":[],"rotateCCW":[],"rotateCW":[],"rotate180":[],"hold":[],"exit":[],"retry":[],"chat":[],"target1":[],"target2":[],"target3":[],"target4":[],"menuUp":[],"menuDown":[],"menuLeft":[],"menuRight":[],"menuBack":[],"menuConfirm":[],"openSocial":[]},"sensitivity":0.5,"vibration":1},"handling":{"arr":2,"das":10,"dcd":0,"sdf":6,"safelock":true,"cancel":false},"volume":{"disable":false,"music":1,"sfx":1,"stereo":0.5,"others":true,"attacks":true,"next":false,"noreset":true,"oof":true,"scrollable":true,"bgmtweak":{}},"video":{"graphics":"minimal","caching":"medium","actiontext":"all","particles":0.6,"background":"0","bounciness":"0","shakiness":"0","gridopacity":"0.55","boardopacity":0.85,"shadowopacity":0.15,"zoom":1,"alwaystiny":false,"nosuperlobbyanim":false,"colorshadow":false,"sidebyside":false,"spin":true,"chatfilter":true,"background_url":null,"background_usecustom":null,"nochat":false,"hideroomids":false,"emotes":true,"emotes_anim":true,"siren":true,"powersave":false,"invert":false,"nobg":false,"chatbg":true,"replaytoolsnocollapse":false,"kos":true,"fire":true,"focuswarning":true,"hidenetwork":false,"guide":false,"lowrescounters":false,"desktopnotifications":true,"lowres":true,"webgl":"webgl2","bloom":1,"chroma":0.5,"flashwave":1,"grinch":true},"gameoptions":{"pro_40l":true,"pro_40l_alert":false,"pro_40l_retry":false,"stride_40l":false,"pro_blitz":false,"pro_blitz_alert":false,"pro_blitz_retry":false,"stride_blitz":false},"electron":{"loginskip":"always","frameratelimit":"4x","presence":true,"taskbarflash":true,"anglecompat":false,"adblock":false},"notifications":{"suppress":false,"forcesound":true,"online":"ingame","offline":"off","dm":"both","dm_pending":"both","invite":"both","other":"both"}}'
pyautogui.press('f12')
time.sleep(1)
pyautogui.moveTo(1353, 256)
pyautogui.click()
pyautogui.click()
pyautogui.write(config)
pyautogui.press('enter')
pyautogui.press('f12')
pyautogui.hotkey('ctrl', 'f5')
time.sleep(1)
pyautogui.moveTo(739, 583)
pyautogui.click()
pyautogui.write(name)
pyautogui.moveTo(739, 682)
pyautogui.click()
pyautogui.moveTo(968, 632)
time.sleep(1)
pyautogui.click()