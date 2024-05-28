import pyautogui as pag

pag.FAILSAFE = False


def close_window():
    pag.moveTo(1900, 15)
    pag.click()


def turn_window():
    pag.moveTo(1800, 15)
    pag.click()


def windowed_mode():
    pag.moveTo(1850, 15)
    pag.click()

#import time
#time.sleep(3)
#print(pag.position())
