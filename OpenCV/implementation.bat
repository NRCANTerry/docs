1) create_dir.bat
- creates folder structure

2) generate.py
- generate red threshold, adaptive threshold, vertical edges (sobel)

	1. gets all images
	2. adapt_thres = aa.adaptive_threshold(img)
	3. vert_thres = aa.get_vertical_edges(adapt_thres)
		1. opening morphological transformation (reduce noise)
		2. removes horizontal edges of certain size
	4. red mask, determines night/day
	5. edges = aa.get_edges(img)
		1. Gaussian blur
		2. Sobel edge detection

	3 IMAGES PRODUCED:
		Red Thershold, Adaptive Threshold, Vertical Edge

3) create_horizon.py
- filter out night images and create a convex hull for the horizon

	1. determine horizon based on location of red blobs
	2. dilates polygons (vert_threshold image)
	3. finds all polygon contours of sufficient area, intersecting red blobs/edges
		1. gets contours from vert_thres_dilate
		2. gets contour area
		3. draws contours
	4. makes convex hull of found edge contours
	5. dilates convex hull
	6. save convex hull

4) check_horizon.py
- lays horizon on original image for debugging

5) create_template.py
- manually create template by labelling stakes

	1. specify base name of template in file (found in images-finale/template/)
	2. makes a mask marking stakes using template with boxes
	3. aa.extract_info_template() gets the centroid and vectors of each stick
	4. processes each stake using standard algorithm
	5. outputs template details in json format

6) pre_match_hough.py
- apply hough transforms to constrain angles and line lengths of adaptive threshold polygons
- filters contours based on edges and angles
- creates two files: one for matching (/pre-match-hough/pre-match/) and one for measuring
		(/pre-match-hough/filtered/)


		1. crop horizon (large block of white that interferes with processing)
		2. filters contours

7) register.m
- registers images based on templates and the observations
- writes to images-final/matched the transformation image where pink is the best template and
   green is observation as well as creates matched.txt which specifies transformation

8) apply_registration_translation.m
- applies matched.txt to original images and the measuring threshold images from pre_match_hough
   and writes them to their respective locations in images-final/calc-snow-depth

9) measure_depth.py
- using images from 'calc-snow-depth' length of stake is calculated