# Run using command: C:\Users\rfernand\AppData\Local\Continuum\Anaconda2/python.exe test

# Import necessary packages
import cv2
import imutils
import argparse

# Construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to input image")
args = vars(ap.parse_args())

# Load the inupt image and display the image
image = cv2.imread(args["image"])
#cv2.imshow("Image", image)
#cv2.waitKey(0)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

# Applying edge detection we can find the outlines of objects in images
edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

# Threshold the image by setting all pixel values less than 225 to 255 (white:foreground)
# and all pixel values >= 225 to 255 (black: background), segmenting the image
thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

# Find contours (i.e. outlines) of foreground objects in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
output = image.copy()

# Loop over the contours
for c in cnts:
	# draw each contour on the output image with a 3px purle outline
	# then display the output contours one at a time
	cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
	cv2.imshow("Contours", output)
	cv2.waitKey(0)

# Draw the total number of contours found in purple
text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 0, 159), 2)
cv2.imshow("Contours", output)
cv2.waitKey(0)

# Apply erosions to reduce the size of foreground objects
mask = thresh.copy()
mask = cv2.erode(mask, None, iterations = 5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

# Dilations can increase the size of ground objects
mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations = 5)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)

# A typical operation we may want to apply is to take our mask and apply
# a bitwise AND to our input image, keeping only the masked regions
mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask = mask)
cv2.imshow("Output", output)
cv2.waitKey(0)