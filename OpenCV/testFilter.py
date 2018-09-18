# import necessary modules
import cv2
import os
import numpy as np
import json
from matplotlib import pyplot as plt
import sys
import operator
import math
import imutils

# constants
lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 50, 50])
upper_red2 = np.array([180, 255, 255])
median_kernal_size = 5
dilate_kernel = (5,5)
min_contour_area = 1e2
max_contour_area = 1e5
angle_thresh = -45
bar_width_low = 15
bar_width_high = 75
min_red_count = 100
img_border = 2850

image = cv2.imread("IMG_0144.JPG")
image_orig = image

# reduce noise in image by local smoothing
image = cv2.medianBlur(image, median_kernal_size)

# height and width
h, w = image.shape[:2]

# identify red areas in image based on 2 harcoded ranges of HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
cv2.imshow("Mask 1", mask1)
cv2.imshow("Mask 2", mask2)
cv2.waitKey()

red_mask = cv2.bitwise_or(mask1, mask2)
cv2.imshow("Red Mask", red_mask)
cv2.waitKey()

# erosion followed by dilated to reduce noise in thresholded image
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, dilate_kernel)
red_mask_open = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

cv2.imshow("Open", red_mask_open)
cv2.waitKey()

# find the final red polygon regions falling within hardcoded ranges of area
# and aspect ratio
red_mask_filtered = np.zeros((h,w), dtype = np.uint8)
contours = cv2.findContours(red_mask_open.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
for cnt in contours:
	contour_area = cv2.contourArea(cnt)
	if min_contour_area <= contour_area <= max_contour_area:
		rect = cv2.minAreaRect(cnt)
		rect_center, rect_size, angle = rect
		width, height = rect_size
		if(angle >= angle_thresh and width <= height and bar_width_low <= width <= bar_width_high) or \
			(angle <= angle_thresh and width >= height and bar_width_low <= height <= bar_width_high):
			x,y,w,h = cv2.boundingRect(cnt)
			cv2.drawContours(red_mask_filtered, [cnt], 0, 255, -1)

cv2.imshow("Filtered", red_mask_filtered)
cv2.waitKey()

# filter based on number of red points 
# this will exclude sticks, trees, ect
# filter contours based on min area to exclude red boxes that are obstructed
# first and last boxes are bottom and top respectively

image_copy = image

# empty list of points
points = list()
center_points = list()

# iterate through contours
for num, cnt in enumerate(contours):
	# create minimum area rectangle
	rect = cv2.minAreaRect(cnt)

	# get coordinates of rectangle points
	box = cv2.boxPoints(rect)

	# iterate through points
	for p in box:
		pt = (p[0], p[1])
		print(pt)
		cv2.circle(image_copy, pt, 5, (0,51,255), 2)
		points.append(pt)

	# mark center of top and bottom squares
	if(num == 0 or num == (len(contours) - 1)):
		M = cv2.moments(cnt)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		center_points.append((cX, cY))
		cv2.circle(image_copy, (cX, cY), 5, (0,255,0), 2)

cv2.line(image_copy, center_points[0], center_points[1], (0, 255, 0), 2)
# draw line connecting centres

deltaX = center_points[0][0] - center_points[1][0]
deltaY = center_points[0][1] - center_points[1][1]
angle = math.degrees(math.atan(float(deltaX)/float(deltaY)))

# rotate the image
rotated = imutils.rotate(image_copy, -angle)
rotated_clear = imutils.rotate(image_orig, -angle)
rotated_points = list()

print("---------------------------------")

# update coordinates after rotation
for pt in points:
	x = pt[0]
	y = pt[1]
	x_new = (x * math.cos(math.radians(-angle))) - (y * math.sin(math.radians(-angle)))
	y_new = (y * math.cos(math.radians(-angle))) + (x * math.sin(math.radians(-angle)))
	print(pt)
	rotated_points.append((x_new, y_new))

print("-----------------------------------")

#for p in rotated_points:
#	cv2.circle(rotated, (int(p[0]), int(p[1])), 5, (0,0,200), 2)

# determine crop parameters
max_left = min(rotated_points, key = lambda item:item[0])[0]
max_right = max(rotated_points, key= lambda item:item[0])[0]
max_down = max(rotated_points, key = lambda item:item[1])[1]

print("max left", max_left)
print("max right", max_right)
print("max down", max_down)

# determine bottom right and top right
bottomRight = max(points)
print("Bottom Right:", bottomRight)
_, topRight = min(enumerate(points), key = lambda item: (-item[1][0], item[1][1]))
print("Top Right:", topRight)

cv2.imshow("Marked", image_copy)
cv2.imshow("Rotated", rotated)
cv2.waitKey()

crop_img = rotated_clear.copy()[int(max_down):, int(max_left): int(max_right)]
cv2.imshow("cropped", crop_img)
cv2.waitKey()

gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (5, 5))
cv2.imshow("Thresh", thresh)
cv2.waitKey()

contours2 = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

bottomPoints = list()

for cnt in contours2:
	rc = cv2.minAreaRect(cnt)
	box = cv2.boxPoints(rc)
	for p in box:
		pt = (p[0],p[1])
		#print(pt)
		cv2.circle(crop_img, pt, 5, (0,51,255), 2)
		if(p[1] > 1):
			bottomPoints.append(p)

cv2.imshow("Crop Marked", crop_img)
cv2.waitKey()

for p in bottomPoints:
	print(p)

for pt in bottomPoints:
	cv2.circle(rotated, (int(pt[0]+max_left),int(pt[1]+max_down)), 5, (0,51,255), 2)

cv2.imshow("Final Marked", rotated)
cv2.waitKey()
sys.exit()


'''
crop_img = image[]


import cv2
img = cv2.imread("lenna.png")
crop_img = img[y:y+h, x:x+w]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)
'''