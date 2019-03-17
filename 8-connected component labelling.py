import cv2
import numpy as np
import random

label = []
label_dict = {}

def getLabel(neighbours):

	# If the 8 connected neighbouring pixels are 0 i.e black assign a new label to the pixel
	if all(x==0 for x in neighbours):
		if len(label) == 0:
			label.append(1)
			return max(label)
		else:
			label.append(max(label) + 1)
			return max(label)

	# If all the 8 connected neighbouring pixels are not 0 i.e black
	# case 1: If there are no conflicting labels assign the label to the pixel
	# case 2: If there are conflicting labels assign the smallest label and add an entry in the label dictionary
	else:
		max_label = 0
		min_label = 0

		neighbours = [x for x in neighbours if x != 0]
		neighbours.sort()

		min_label = neighbours[0]
		max_label = neighbours[len(neighbours)-1]

		if max_label == min_label:
			return min_label
		else:
			label_dict[max_label] = min_label
			return min_label


img = cv2.imread('Image_01.png', 0)

ret,binary_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

row, column = binary_img.shape

v = 255
new_img = np.array(binary_img)


# First Pass
for i in range(row):
	for j in range(column):

		# Only interested in pixels with value v [255] i.e white pixels
		if new_img[i,j] == v:

			# Checking for different positions of pixels
			if i == 0 and j == 0:
				new_img[i,j] = getLabel([])

			elif i == 0 and j > 0:
				new_img[i,j] = getLabel([new_img[i,j-1]])

			elif i > 0 and j == 0:
				new_img[i,j] = getLabel([new_img[i-1,j], new_img[i-1,j+1]])

			elif i > 0 and j == (column-1):
				new_img[i,j] = getLabel([new_img[i-1,j-1], new_img[i-1,j], new_img[i,j-1]])

			elif i > 0 and j > 0:
				new_img[i,j] = getLabel([new_img[i-1,j-1], new_img[i-1,j], new_img[i-1,j+1], new_img[i,j-1]])


# Second Pass
for k in range(len(label_dict)):
	for i in range(row):
	    for j in range(column):
	        if new_img[i][j] in label_dict:
	            new_img[i][j] = label_dict[new_img[i][j]]




# Colorizing the labels
output_img = np.zeros((row, column, 3), int)
labelColor = {0: (0, 0, 0)}
for i in range(row):
    for j in range(column):
        label = new_img[i,j]
        if label not in labelColor:
            labelColor[label] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        output_img[i, j, :] = labelColor[label]


cv2.imwrite('output_img.png', output_img)
