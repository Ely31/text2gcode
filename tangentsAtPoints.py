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

img = cv2.imread("./sources/w.jpg")
img = cv2.blur(img, (15,15))
display = img
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1200, 800)

img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)[1]

contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
i=0
pointCounter = 0
pointsToSkip = 10
print("drawing lines...")
while i < len(contours[0])-2*pointsToSkip-1:
     # AAAAAHHHHH
    point0 = (contours[0][i][0][0], contours[0][i][0][1])
    point1 = (contours[0][i + pointsToSkip][0][0], contours[0][i + pointsToSkip][0][1])
    point2 = (contours[0][i + 2*pointsToSkip][0][0], contours[0][i + 2*pointsToSkip][0][1])

    cv2.line(display, point0, point1, green, 1)
    # calc slope of the line
    slope = calcslope(point0, point2)
    #print(slope)
    # make the line at the middle point of the three
    startpoint = point1
    intstartpoint = pointToIntPoint(startpoint)


    lineLength = 10
    # Draw the perpendicular lines
    if slope != 0:
         perpSlope = -1/slope
    else: perpSlope = 99 # Avoid divide by 0 problems
    secondLinePoint = (intstartpoint[0] + calcXFromLengthAndSlope(lineLength, perpSlope), intstartpoint[1] + calcYFromLengthAndSlope(lineLength, perpSlope))
    cv2.line(display, intstartpoint, pointToIntPoint(secondLinePoint), red, 1)

    # Probe to the left and right of the point along the perpendicular line to find which way we need to search
    directionProbePoint = ((startpoint[0]+ calcXFromLengthAndSlope(3, perpSlope)), (startpoint[1]+ calcYFromLengthAndSlope(3, perpSlope)))

    # I spent an hour trying to figure this out and it turns out that when accessing a single pixel, the input is y,x not x,y. WHAT THE FRICK OPENCV
    print(img[pointToIntPoint(directionProbePoint)[1], pointToIntPoint(directionProbePoint)[0]])
    print(pointToIntPoint(directionProbePoint))

    probeDirection = 1
    if (img[pointToIntPoint(directionProbePoint)[1], pointToIntPoint(directionProbePoint)[0]] == 255):
        probeDirection = 1
        cv2.circle(display, pointToIntPoint(directionProbePoint), 1, blue)
    else:
        probeDirection = -1

    


    i += pointsToSkip
    pointCounter += 1
# Close the thing with the last line
cv2.line(display, (contours[0][i][0][0], contours[0][i][0][1]), (contours[0][0][0][0], contours[0][0][0][1]), green, 1)

print()
print(f"contour length: {len(contours[0])}")
print(f"points computed: {pointCounter}")


cv2.imshow("image", display)

# Stolen from stack overflow because I needed to take a screenshot
# Only exit the window if you press escape
while True:
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break