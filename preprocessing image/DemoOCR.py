import PIL
import time
import ctypes
import win32ui
import win32gui
import win32api
import win32con
from PIL import ImageGrab
from PIL import ImageChops
from vietocr.tool.config import Cfg
from win32api import GetSystemMetrics
from vietocr.tool.predictor import Predictor

awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0, 0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

red = win32api.RGB(255, 0, 0)

past_coordinates = monitor

config = Cfg.load_config_from_name('vgg_transformer')

# load pretrained weight
config['weights'] = './transformerocr.pth'

# set device to use cpu
config['device'] = 'cpu'
# config['device'] = 'cuda'
config['cnn']['pretrained'] = False
config['predictor']['beamsearch'] = False

detector = Predictor(config)
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
        img = img_tmp
        _start_time = time.time()
        result = detector.predict(img)
        print(time.time()-_start_time, '\t\t', result)
    else:
        pass