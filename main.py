import cv2
import numpy as np
from PIL import Image, ImageGrab, ImageChops
import pytesseract
import argparse
import os
import PIL
import time
import ctypes
import win32ui
import win32gui
import win32api
import win32con
from win32api import GetSystemMetrics


def main(image, text_font='white', threshold=0.7):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = gray.astype(np.double)

    (height, width) = gray.shape
    pixels = []
    for column in range(width):
        for row in range(height):
            pixels.append(gray[row, column])

    gray = gray / max(pixels)

    img = gray.copy()
    (height, width) = img.shape
    for column in range(width):
        for row in range(height):
            if img[row, column] > threshold:
                img[row, column] = 255
                img[row, column] = 255
                img[row, column] = 255
            else:
                img[row, column] = 0
                img[row, column] = 0
                img[row, column] = 0

    kernel = np.ones((1,2),np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    if text_font == 'white':
        img = (255 - img)
    elif text_font == 'black':
        pass

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, img)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(filename), lang='vie')
    os.remove(filename)

    return text


if __name__ == "__main__":
    text_font = input("Text color is white or black (please just type 'white' or 'black): ")
    threshold = input("\nPlease choose the threshold value (usually the threshold is 0.7 for live stream on phone and 0.6 for live stream on web browser): ")

    awareness = ctypes.c_int()
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    dc = win32gui.GetDC(0)
    dcObj = win32ui.CreateDCFromHandle(dc)
    hwnd = win32gui.WindowFromPoint((0, 0))
    monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

    red = win32api.RGB(255, 0, 0)

    past_coordinates = monitor

    print("start cap")
    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                mp = win32api.GetCursorPos()
            else:
                mr = win32api.GetCursorPos()
                break

    img = ImageGrab.grab(bbox=(mp[0], mp[1], mr[0], mr[1]))
    m = mp
    n = mr
    while True:
        win32gui.InvalidateRect(hwnd, (m[0], m[1], GetSystemMetrics(0), GetSystemMetrics(1)), True)
        for i in range((n[0]-m[0])//4):
            win32gui.SetPixel(dc, m[0]+4*i, m[1], red)
            win32gui.SetPixel(dc, m[0]+4*i, n[1], red)
        for i in range((n[1]-m[1])//4):
            win32gui.SetPixel(dc, m[0], m[1]+4*i, red)
            win32gui.SetPixel(dc, n[0], m[1]+4*i, red)

        img_tmp = ImageGrab.grab(bbox=(mp[0], mp[1], mr[0], mr[1]))
        if ImageChops.difference(img, img_tmp).getbbox():
            img = img_tmp.copy()
            _start_time = time.time()
            img.save('temp_img.png')
            time.sleep(0.25)
            image = cv2.imread('temp_img.png', cv2.IMREAD_UNCHANGED)
            print(time.time()-_start_time, '\n', main(image, text_font, float(threshold)))
            os.remove('temp_img.png')
        else:
            pass
