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
G0 X1.2259 Y1.8389
G0 Z-1
G1 X1.0508 Y0.0292
G1 X0.7881 Y0.2335
G1 X0.4086 Y0.7881
G1 X0.2043 Y0.8173
G1 X-0.1751 Y0.7589
G1 X-0.9049 Y0.4378
G1 X-0.8757 Y0.0292
G1 X-1.1676 Y-0.3795
G1 X-0.4962 Y-0.8757
G1 X-0.0584 Y-1.4011
G1 X0.4962 Y-1.6346
G1 X0.9924 Y-0.6422
G1 X0.8757 Y0.0584
G1 X1.2551 Y0.5546
G1 X0.8173 Y0.7297
G0 Z1
G0 X0.0 Y-1.3427
; End of letter
""")
        case ' ':
            return (
"""; Space
G0 X7
""")