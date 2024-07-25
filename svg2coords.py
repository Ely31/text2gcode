import constants as c
# Constants
# S for scale
s = 0.1
# K for kerning (spacing between letters)
k = 0
# V for vertical offset
v = 0
# This one doesn't need a comment
filename = './sources/drawing.svg'

def setfilename(fname):
    global filename
    filename = fname

coordslist = (())
def grabcoords():
    # Scuffed file reading
    svgreader = open(filename, 'r')
    print("reading file...")
    svgstring = svgreader.read()
    svgreader.close()

    splitword = "d=\"m "
    splitstrings = svgstring.partition(splitword)

    coordstring = splitstrings[2].partition("\"")[0]

    global coordslist
    coordslist = list(map(float, coordstring.replace(' ', ',').split(",")))
    # Set the first coord to zeros because they're all relative
    coordslist[0] = 0
    coordslist[1] = 0

grabcoords()

print(coordslist)

# This is scuffed, a better way would be to use the spaces that were there before we took them out
def getorderedpair(index):
    return ((coordslist[index*2]), (coordslist[(index*2)+1]))

# Found out they're already relative so we don't need this
#def calcrelativecdist(p1, p2):
    #return ((p2[0] - p1[0]),(p2[1] - p1[1]))

def coordtomovecommand(coord):
    # Round to 4 places because you get floating point shenannigans when using the scale factor
    return f"G1 X{round(coord[0]*s, 4)} Y{round(-coord[1]*s, 4)}\n"


def calcleftmostpoint():
    i = 0
    leftmostpoint = 0
    accumulation = 0
    while(i < len(coordslist)):
        accumulation += coordslist[i]

        if(accumulation < leftmostpoint):
            leftmostpoint = accumulation

        i += 2
    return(leftmostpoint)

absolutecoordoflastx = 0
def calcrightmostpoint():
    i = 0
    rightmostpoint = 0
    accumulation = 0
    while(i < len(coordslist)):
        accumulation += coordslist[i]

        if(accumulation > rightmostpoint):
            rightmostpoint = accumulation

        i += 2
    
    global absolutecoordoflastx
    absolutecoordoflastx = accumulation
    return(rightmostpoint)

absolutecoordoflasty = 0
def calcbottommostpoint():
    # Start with 1 here because that will be the first y coord
    i = 1
    bottommostpoint = 0
    accumulation = 0
    while(i < len(coordslist)):
        accumulation += coordslist[i]

        if(accumulation > bottommostpoint):
            bottommostpoint = accumulation

        i += 2
    
    global absolutecoordoflasty
    absolutecoordoflasty = accumulation
    return(bottommostpoint)

print()
print("leftmost point: " + str(calcleftmostpoint()))
print("rightmost point: " + str(calcrightmostpoint()))
print("bottommost point: " + str(calcbottommostpoint()))

charwidth = (calcrightmostpoint() - calcleftmostpoint())
print("character width: " + str(charwidth))
print()
print(f'abslastx: {absolutecoordoflastx}')
print(f'abslasty: {absolutecoordoflasty}')

def makegcode():
    outstr = f'G0 X{round(-calcleftmostpoint()*s, 4)} Y{round(((calcbottommostpoint()+v)*s), 4)}\nG0 Z{-c.liftHeight}\n'
    # Start at 1 to skip the first one because it's just 0,0 so it does nothing
    i = 1
    while (i < (len(coordslist))/2):
        outstr += coordtomovecommand(getorderedpair(i))
        i += 1
    # Move back to the baseline after we're done so we can do the next character
    # Have to do some funny stuff because y positive is up in gcode and down in svg
    outstr += f"G0 Z{c.liftHeight}\nG0 X{round((calcrightmostpoint() - absolutecoordoflastx + k)*s, 4)} Y{round((-calcbottommostpoint() + absolutecoordoflasty - v)*s, 4)}\n"
    outstr += f"; End of letter"

    return outstr

print()
print("Gcode:")
print(makegcode())
