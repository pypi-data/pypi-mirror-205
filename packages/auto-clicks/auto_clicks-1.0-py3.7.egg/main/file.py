import pyautogui
import keyboard
import random
def click():
    while True:
        if keyboard.is_pressed("c") or keyboard.is_pressed("w+c") or keyboard.is_pressed("s+c") or keyboard.is_pressed(
                "a+c") or keyboard.is_pressed("d+c"):
            while True:
                num = random.uniform(0.005, 0.1)
                pyautogui.click(interval=num)
                if keyboard.is_pressed("x") or keyboard.is_pressed("w+x") or keyboard.is_pressed(
                        "s+x") or keyboard.is_pressed("a+x") or keyboard.is_pressed("d+x"):
                    break
