-----------------------------------------------------------------

# Changing Colourspaces
cv2.cvtColor(input_image, flag) and cv2.inRange(input, lower, upper)

# two most common color-space conversion methods (flags):
	# BGR <--> Gray
		cv2.COLOR_BGR2GRAY

	# BGR <--> HSV
		cv2.COLOR_BGR2HSV

-----------------------------------------------------------------

# Object Tracking
# take frame from video
# convert from BGR to HSV colour-space
# threshold HSV image for a range of blue colour
# extract the blue object alone

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

	# Take each frame
	_, frame = cap.read()

	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# define range of blue colour in HSV
	lower_blue = np.array([100, 50, 50])
	upper_blue = np.array([130, 255, 255])

	# Threshold the HSV image to get only blue colors
	mask = cv.inRange(hsv, lower_blue, upper_blue)
	
	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame, frame, mask = mask)

	cv2.imshow('res', res)

-----------------------------------------------------------------

# Image Thresholding
cv2.threshold() and cv2.adaptiveThreshold()

# simple thresholding
	# if pixel value is greater than threshold, it is assigned one value
	# else it is assigned another value

cv2.threshold(grayscale image, threshold value, maximum value, thresholding style)
# outputs are retval and thresholded image

ret, thresh = cv2.threshold(image, 127, 255, cv.THRESH_BINARY)

# adaptive thresholding
	# algorithm calculates threshold for a small region of the image
	# get different thresholds for different regions of the same image
	# better results for images with varying illumination

	# adaptive methods: cv2.ADAPTIVE_THRESH_MEAN_C and cv2.ADAPTIVE_THRESH_GAUSSIAN_C

cv2.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)

-----------------------------------------------------------------

# Smoothing Images

# Image Blurring (Image Smoothing)
	# achieved by convoling the image with a low-pass filter kernel
	# useful for removing noises

# 1. Averaging - specify width and height of kernel
blur = cv2.blur(img, (5,5))

# 2. Gaussian
blur = cv2.GaussianBlur(img, (5,5), 0)

# 3. Median Blurring - highly effective against salt-and-pepper noise
blur = cv.MedianBlur(img, 5)

# 4. Bilateral Filtering - effective in noise removal while keeping edges shar
blur = cv.bilateralFilter(img, 9, 75, 75)

-----------------------------------------------------------------

# Morphological Transformations

# 1. Erosion
kernel = np.ones((5,5), np.uint8)
erosion = cv2.erode(img, kernel, iterations = 1)

# 2. Dilation
dilation = cv2.dilate(img, kernel, iterations = 1)

# 3. Opening (erosion followed by dilation)
	# useful for removing noise
opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)

# 4. Closing (dilation followed by erosion)
closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

# 5. Morphological Gradient (different between dilation and erosian)
gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)

-----------------------------------------------------------------

# https://docs.opencv.org/master/d5/d0f/tutorial_py_gradients.html

# Image Gradients
# OpenCV provides 3 types of gradient filters or High-pass filters
# Sobel, Scharr and Laplacian

# 1. Sobel and Scharr
	# Sobel is joint Gaussian smoothing plus differentiation operation, so
	# more resistant to noise
	# specify direction of derivatives to be taken, vertical or horizontal
	# if ksize = -1, a 3x3 Scharr filter gives better results than 3x3 Sobel

sobelx = cv2.Sobel(img, cv.CV_64F, 1, 0, ksize = 5)
sobely = cv2.Sobel(img, cv.CV_64F, 0, 1, ksize = 5)

# 2. Laplacian Derivativse	
laplacian = cv2.Laplacian(img, cv.CV_64F)

-----------------------------------------------------------------

# Canny Edge Detection
cv2.Canny()

img = cv2.imread("test.jpg", 0)
edges = cv2.Canny(img, 100, 200)

# format:
	# input image
	# minVal
	# maxVal

-----------------------------------------------------------------

# Contours
# curve joining all the continuous points (along the boundary), having same
# colour or intensity
# for better accuracy use binary images (first apply threshold or canny edge detection)

im = cv2.imread("test.jpg")
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Drawing Contours
	# Draw all contours
	cv2.drawContours(img, contours, -1, (0,255,0), 3)

	# Draw an individual contour (e.g. 4th)
	cv2.drawContours(img, contours, 3, (0,255,0), 3)

-----------------------------------------------------------------

# Histogram Equilization
img = cv2.imread("wiki.jpg", 0)
equ = cv2.equalizeHist(img)

-----------------------------------------------------------------

# Template Matching
# method for searching and finding the location of a template image in a
# larger image

# methods are:
	# cv2.TM_CCOEFF
	# cv2.TM_CCOEFF_NORMED
	# cv2.TM_CCORR
	# cv2.TM_CCORR_NORMED
	# cv2.TM_SQDIFF
	# cv2.TM_SQDIFF_NORMED

img = cv2.imread("test.jpg", 0)
template = cv2.imread("template.jpg", 0)
w, h = template.shape[::-1]

# Apply template matching
res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
if method in [cv2.TM_SQDIFF, cvw.TM_SQDIFF_NORMED]:
	top_left = min_loc
else:
	top_left = max_loc

bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(img, top_left, bottom_right, 255, 2)

-----------------------------------------------------------------

# Hough Line Transform
# popular technique to detect any shape, if you can represent it mathematically

cv2.HoughLines()
# returns an array of :math:(rho, theta) values
# p in pixels and theta in radians

# format:
	# input image (should be binary so apply threshold or use canny edge detection first)
	# p and theta accuracies respectively
	# threshold (minimum vote it should get to be considered a line)
		# minimum length of line that should be detected

img = cv2.imread("sudoko.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

lines = cv2.HoughLines(edges, 1, np.pi/180, 200)