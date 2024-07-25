# A program to convert a text file into gcode movements for a pen slapped onto a 3d printer,
# drawing one symbol for each character in the text file.
import charset
import constants as c

startX = 5
startY = 200

input = open("./sources/input.txt", "r")
inputString = input.read()
print("input text:")
print(inputString)

output = open("output.gcode", "w")
# Prep all the stuff at the beginning of the gcode
output.write(
f"""G90 ; absolute coords
G28 ; home
G0 F{c.travelSpeed} ; set speed
G1 F{c.drawSpeed} ; set speed
\n; move to the starting position
G0 Z{c.restHeight}
G0 X{startX} Y{startY}
G0 Z{c.liftHeight}

G91 ; relative coords
; Start drawing stuff
""")
output.close()

output = open("output.gcode", "a")
print("parsing characters...")
# Write all the symbols
for char in inputString:
    output.write(charset.charToGcode(char))

# Lift up the pen and move it out of the way at the end
output.write(
f"""; Done. Pick up the pen and move it out of the way
G0 Z{c.restHeight - c.liftHeight}
G28 X""")

input.close()
output.close()
print("done.")