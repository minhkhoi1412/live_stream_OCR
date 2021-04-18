import cv2
import numpy as np

img = cv2.imread('C:\\Users\\neonx\\OneDrive\\OCR\\test image v1.9.png', 0)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(img, (21, 21), 0)

mask = np.zeros((512, 512, 3), dtype=np.uint8)
mask = cv2.circle(mask, (258, 258), 100, np.array([255, 255, 255]), -1)

out = np.where(mask==np.array([255, 255, 255]), img, blurred_img)

cv2.imwrite("./background_removed.png", out)