import cv2
import numpy
import math

green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)
black = (0,0,0)

img = cv2.imread("./sources/alphabet.jpg")
img = cv2.blur(img, (15,15))
display = img
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1200, 800)

img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
print("image dimensions:")
print(img.shape)

contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
cv2.drawContours(display, contours, -1, red, 3)

boundingboxes = []
prevbox = [0,0,0,0]
for i in contours:
    contours_poly = cv2.approxPolyDP(i, 3, True)
    boundingbox = cv2.boundingRect(contours_poly)
    correctedbox = (int(boundingbox[0]), int(boundingbox[1]), int(boundingbox[0]+boundingbox[2]), int(boundingbox[1]+boundingbox[3]))
    # Handle i and j, the only letters that aren't one continous shape
    if abs(correctedbox[2] - prevbox[2]) < 100:
        combinedRect = correctedbox
        boundingboxes[i-1] = combinedRect
        print("boxes combined")
    else:
        boundingboxes.append(correctedbox)

    prevbox = correctedbox
    
# Well the sorting was easier than expected
boundingboxes.sort()
print("bounding boxes: ")
print(boundingboxes)

charnumber = 0
for i in boundingboxes:
    cv2.rectangle(display, (boundingboxes[charnumber][0], boundingboxes[charnumber][1]), (boundingboxes[charnumber][2], boundingboxes[charnumber][3]), green, 2)
    cv2.putText(display, f"{charnumber}", (boundingboxes[charnumber][0], boundingboxes[charnumber][1]), 6, 3, black, 3)

    croppedimage = img[boundingboxes[charnumber][1]:boundingboxes[charnumber][3], boundingboxes[charnumber][0]:boundingboxes[charnumber][2]]

    cv2.imwrite(f"./extracted_images/{charnumber}.png", croppedimage)

    charnumber += 1



cv2.imshow("image", display)

# Stolen from stack overflow because I needed to take a screenshot
# Only exit the window if you press escape
while True:
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break