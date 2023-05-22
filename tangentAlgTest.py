import cv2
import numpy
import math

green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)

def calcslope(p1, p2):
    return (p1[1] - p2[1]) / (p1[0] - p2[0])

def calccenterpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

def pointToIntPoint(p):
    return (p[0].astype(int), p[1].astype(int))

def calcXFromLengthAndSlope(l, m):
    return math.sqrt((l*l)/(m*m+1))

def calcYFromLengthAndSlope(l,m):
    return m * calcXFromLengthAndSlope(l, m)

img = cv2.imread("w.jpg")
img = cv2.blur(img, (15,15))
display = img
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1200, 800)

img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]

contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
i=0
pointsToSkip = 10
print("drawing lines...")
while i < len(contours[0])-pointsToSkip-1:
     # AAAAAHHHHH
    point1 = (contours[0][i][0][0], contours[0][i][0][1])
    point2 = (contours[0][i + pointsToSkip][0][0], contours[0][i + pointsToSkip][0][1])

    cv2.line(display, point1, point2, green, 1)
    # calc slope of the line
    slope = calcslope(point1, point2)
    print(slope)
    # calc the center point of each line
    centerpoint = calccenterpoint(point1, point2)
    intcenterpoint = pointToIntPoint(centerpoint)
    cv2.circle(display, intcenterpoint, 1, blue)


    lineLength = 10
    # Draw the perpendicular lines
    if slope != 0:
         perpSlope = -1/slope
    else: perpSlope = 99 # Avoid divide by 0 problems
    secondLinePoint = (intcenterpoint[0] + calcXFromLengthAndSlope(lineLength, perpSlope), intcenterpoint[1] + calcYFromLengthAndSlope(lineLength, perpSlope))
    cv2.line(display, intcenterpoint, pointToIntPoint(secondLinePoint), red, 1)

    i += pointsToSkip
# Close the thing with the last line
cv2.line(display, (contours[0][i][0][0], contours[0][i][0][1]), (contours[0][0][0][0], contours[0][0][0][1]), green, 1)

#cv2.drawContours(display, contours, 0, (255,0,0), 1)

print()
print(len(contours[0]))
print(i/pointsToSkip)


cv2.imshow("image", display)

# Stolen from stack overflow because I needed to take a screenshot
# Only exit the window if you press escape
while True:
    k = cv2.waitKey(0) & 0xFF
    print(k)
    if k == 27:
        cv2.destroyAllWindows()
        break