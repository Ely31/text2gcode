pagesize = 10

def imgintosvg(imagepath, outputpath):

    file = open(outputpath + ".svg", 'w')
    file.write(
        f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>

<svg
   width="{pagesize}mm"
   height="{pagesize}mm"
   viewBox="0 0 {pagesize} {pagesize}"
   version="1.1"
   id="svg5"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs2" />
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
    <image
       xlink:href="{imagepath}" height="{pagesize}" width="{pagesize}"
       />
  </g>
</svg>""")

    file.close()

imgintosvg("./progress/'perpendicular wonk.png'", "./test")