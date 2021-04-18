import cv2
import numpy as np
from PIL import Image
import pytesseract
import os



# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Load image, convert to HSV format, define lower/upper ranges, and perform
# color segmentation to create a binary mask
# image = cv2.imread('C:\\Users\\neonx\\OneDrive\\OCR\\test image.jpg')
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# lower = np.array([0, 0, 145])
# upper = np.array([360, 255, 255])
#
# mask = cv2.inRange(hsv, lower, upper)
# result = cv2.bitwise_and(image, image, mask=mask)

# cv2.namedWindow('result', cv2.WINDOW_NORMAL)
# cv2.moveWindow('result', 50, 75)
# cv2.imshow('result', mask)
# cv2.waitKey()


# image = cv2.imread('C:\\Users\\neonx\\OneDrive\\OCR\\test image v1.3.jpg', cv2.IMREAD_UNCHANGED)
image = cv2.imread('C:\\Users\\neonx\\OneDrive\\OCR\\test2.4.png', cv2.IMREAD_UNCHANGED)

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
        # print(img[row, column])
        if img[row, column] > 0.6:
            img[row, column] = 255
            img[row, column] = 255
            img[row, column] = 255
        else:
            img[row, column] = 0
            img[row, column] = 0
            img[row, column] = 0

kernel = np.ones((1,2),np.uint8)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
img = (255 - img)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, img)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(Image.open(filename), lang='vie')
os.remove(filename)
print(text)
cv2.imshow('Converted Image', img)
cv2.imshow('Original Image', image)
cv2.waitKey(0)

