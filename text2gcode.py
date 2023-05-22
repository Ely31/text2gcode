# A program to convert a text file into gcode movements for a pen slapped onto a 3d printer,
# drawing one symbol for each character in the text file.

startX = 5
startY = 200

# Hardcoding these in is probably not the best way
def charToGcode(char):
    match char:
        case 'a':
            return (
"""; Square
G0 Z-1
G1 X5
G1 Y5
G1 X-5
G1 Y-5
G0 Z1
G0 X7
"""
)
        case 'b':
            return (
"""; Triangle
G0 Z-1
G1 X5
G1 X-2.5 Y5
G1 X-2.5 Y-5
G0 Z1
G0 X7
""")
        case 'e':
            return (
"""; E
G0 Z-1
G1 X0.0 Y0.0
G1 X1.05081 Y0.029189
G1 X0.7881100000000001 Y0.233514
G1 X0.40864700000000004 Y0.7881070000000001
G1 X0.204325 Y0.8172990000000001
G1 X-0.175134 Y0.758918
G1 X-0.904867 Y0.437838
G1 X-0.875676 Y0.029189
G1 X-1.1675674 Y-0.37946
G1 X-0.4962151000000001 Y-0.8756750000000001
G1 X-0.058377700000000005 Y-1.401081
G1 X0.49621540000000003 Y-1.6345939999999999
G1 X0.9924328 Y-0.6421640000000001
G1 X0.875676 Y0.05838
G1 X1.255133 Y0.5545950000000001
G1 X0.8172990000000001 Y0.72973
""")
        case ' ':
            return (
"""; Space
G0 X7
""")

input = open("./sources/input.txt", "r")
inputString = input.read()
print("input text:")
print(inputString)

output = open("output.gcode", "w")
# Prep all the stuff at the beginning of the gcode
output.write(
f"""G90 ; absolute coords
G28 ; home
G0 F3000 ; set speed
G1 F3000 ; set speed
\n; move to the starting position
G0 Z10
G0 X{startX} Y{startY}
G0 Z1

G91 ; relative coords
; Start drawing stuff
""")
output.close()

output = open("output.gcode", "a")
print("parsing characters...")
# Write all the symbols
for char in inputString:
    output.write(charToGcode(char))

# Lift up the pen and move it out of the way at the end
output.write(
"""; Done. Pick up the pen and move it out of the way
G0 Z9
G28 X""")

input.close()
output.close()

print("done.")