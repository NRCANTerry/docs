-----------------------------------------------------------------

# Loading and displaying an image

image = cv2.imread("jp.png")
(h, w, d) = image.shape

# images are represented as multi-dimensional NumPy array
# with shape no. rows (height) x no. colums (width) x 
# no.channels (depth) --> image is NumPy array

-----------------------------------------------------------------

# Display an Image with Matplotlib
# matplotlib is plotting library for Python

img = cv2.imread("jp.jp", 0)
mathplotlib.pyplot.imshow(img, cmap = "gray", interpolation = "bicubic")
mathplotlib.pyplot.xticks([]), mathplotlib.pyplot.yticks([]) # hide ticks
mathplotlib.pyplot.show()

-----------------------------------------------------------------

# Write an image

cv2.imwrite("jp.png", img)

# use the function cv2.imwrite() to save an image
# first argument is the file name, second argument is the image you
# want to save

-----------------------------------------------------------------

# Accessing Individual Pixels

(B, G, R) = image[100, 50]

# access RGB pixel located at x = 50, y = 100

-----------------------------------------------------------------

# Array Slicing and Cropping

roi = image[60: 160, 320: 420]
cv2.imshow("ROI", roi)
cv2.waitKey(0)

# array slicing has format:     image[startY:endY, startX:endX]
# display until key pressed

-----------------------------------------------------------------

# Resizing Images

resized = cv2.resize(image, (200,200))

# resize image to 200 x 200 pixels

resized = imutils.resize(image, width = 300)

# resize with same aspect ratio using imutils library

-----------------------------------------------------------------

# Rotating Images

rotated = imutils.rotate(image, -45)
rotated = imutils.rotate_bound(image, 45)

# rotate_bound prevents openCV from clipping the image during a rotation

-----------------------------------------------------------------

# Smoothing an Image
# blur an image to reduce high frequency noise, making it easier for
# algorithms to detect and understand image contents

blurred = cv2.GaussianBlur(image, (11,11), 0)

# Gaussian blur with an 11x11 kernel
	# larger kernel leads to a more blurred image
	# kernel is arbirary size of M x N pixels, provided M and N are odd

-----------------------------------------------------------------

# Drawing an Image

output = image.copy()
cv2.rectangle(output, (320,60), (420, 160), (0,0,255), 2)

# draw a 2px thick rectangle
# format:
	# destination image
	# starting pixel (top left)
	# ending pixel (bottom right)
	# colour (BGR tuple)
	# line thickness

output = image.copy()
cv2.circle(output, (300,150), 20, (255, 0, 0), -1)

# draw a blue 20px filled circle centred at x = 300, y = 150
# format:
	# destination image
	# center coordinate
	# radius
	# colour
	# thickness (negative is filled in)

output = image.copy()
cv2.line(output, (60,20), (400,200), (0,0,255), 5)

# draw a red 5px thick line from x = 60, y = 20 to x = 400, y = 200

output = image.copy()
cv2.putText(output, "openCV", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

# draw green text on image
# format:
	# destination image
	# text string
	# starting point
	# font
	# scale (font size multiplier)
	# text colour
	# thickness

-----------------------------------------------------------------

# Converting an Image to Grayscale

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", image)

-----------------------------------------------------------------

# Edge Detection
# useful for finding boundaries of objects in an image

edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)

# using Canny algorithm we can find the edges in the image
# format:
	# gray image
	# minimum threshold (30)
	# maximum threshold (150)
	# aperture size (sobel kernel size) - default is 3

-----------------------------------------------------------------

# Thresholding
# remove lighter or darker regions and contours of images

thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)

# grabbing all pixels in gray image greater than 225 and setting
# them to 0 (black) which corresponds to background
# setting pixel values less than 225 to 255 (white) which 
# corresponds with foreground

-----------------------------------------------------------------

# Detecting and Drawing Contours

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
output = image.copy()

# use cv2.findContours to detect contours in the image
# finding all foreground (white) pixels in the thresh.copy() image

for c in cnts:
	cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
	cv2.imshow("Contours", output)
	cv2.waitKey(0)

# draw each c for cnts list on the image using cv2.drawCountours

-----------------------------------------------------------------

# Erosions and dilations
# typically used to reduce noise in binary images (side effect of thresholding)
# to reduce the size of foreground objects we can erode away pixels given
# a number of iterations

mask = thresh.copy()
mask = cv2.erode(mask, None, iterations = 5)
cv2.imshow("Eroded", mask)

# using cv2.erode we proceed to reduce the contour sizes with 5 iterations

mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations = 5)
cv2.imshow("Dilated", mask)

# usnig cv2.dilate we proceed to increase the contour sizes with 5 iterations

-----------------------------------------------------------------

# Masking and bitwise operations
# masks allow us to "mask out" regions of an image we don't care about
# a typical operation we may want to apply is to take our mask and apply a
# bitwise AND to our input image, keeping only the masked regions

mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask = mask)
cv2.imshow("Output", output)

