# import the necessary packages
from PIL import Image
import cv2
import os


image = cv2.imread('C:\\Users\\neonx\\OneDrive\\OCR\\test image v1.7.png')
# image = cv2.imread('preprocessed_img v1.png', 0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 100, 200)
# gray = cv2.medianBlur(gray, 3)
# gray = cv2.GaussianBlur(gray, (21, 21), 0)
# gray = cv2.bilateralFilter(gray,9,75,75)
# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv2.imwrite('preprocessed_img v1.png', gray)

# from PIL import Image
#
# def binarize_image(im, threshold):
#     image = im.convert('L')  # convert image to monochrome
#     bin_im = image.point(lambda p: p > threshold and 255)
#     return bin_im
#
# im = Image.open('C:\\Users\\neonx\\OneDrive\\OCR\\test image v1.6.png')
# binarized = binarize_image(im, 100)
# binarized.save('preprocessed_img.png')