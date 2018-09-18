import cv2
import numpy as np
import sys

# Import image
image = cv2.imread('PICT0006.JPG')

new_image = np.zeros(image.shape, image.dtype)
alpha = 1.2
beta = 5

print(" Basic Linear Transforms ")
print("--------------------------")

for y in range(image.shape[0]):
	for x in range(image.shape[1]):
		for c in range(image.shape[2]):
			new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)

cv2.imshow("Original Image", image)
cv2.imshow("New Image", new_image)
cv2.waitKey(0)

# Convert the image to grayscale
gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# Threshold the image
thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

mask = cv2.dilate(thresh, None, iterations = 5)
mask = cv2.erode(mask, None, iterations = 5)

# Erode then dilate the image
mask = cv2.erode(mask, None, iterations = 3)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

mask = cv2.dilate(mask, None, iterations = 3)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)