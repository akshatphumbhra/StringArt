class PostScript:
    def __init__(self, filename, width, height):
        self.file = open(filename, 'w')
        self.width = width 
        self.height = height
        self.file.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        self.file.write(f"%%BoundingBox: 0 0 {width} {height}\n\n\n")

    def setLine(self, lineJoin=1, lineCap=1):
        self.file.write(f"{lineJoin} setlinejoin\n")
        self.file.write(f"{lineCap} setlinecap\n\n\n")
    
    def setRGB(self, color):
        self.file.write(f'{color[0]/255} {color[1]/255} {color[2]/255} setrgbcolor\n')
    
    def setGray(self, gray):
        self.file.write(f'{gray} setgray\n')
    
    def setLineWidth(self, lw):
        self.file.write(f'{lw} setlinewidth\n')

    def translate(self, point):
        self.file.write(f'{point[0]} {point[1]} translate\n')

    def makeLine(self, start, end):
        self.file.write(f'{start[0]} {start[1]} moveto\n')
        self.file.write(f'{end[0]} {end[1]} lineto\n')
        self.file.write(f'stroke\n')
    
    def rotate(self, angle):
        self.file.write(f'{angle} rotate\n')

    def makeCircle(self, center, radius, fill=False):
        self.file.write(f'{center[0]} {center[1]} {radius} 0 360 arc closepath\n')
        if fill:
            self.file.write(f'fill\n')
        else:
            self.file.write(f'stroke\n')
    
    def definePath(self, points, close=True, fill=False):
        self.file.write(f'newpath\n')
        self.file.write(f'{points[0][0]} {points[0][1]} moveto\n')
        for point in points[1:]:
            self.file.write(f'{point[0]} {point[1]} lineto\n')
        if close:
            self.file.write(f'closepath\n')
        if fill:
            self.file.write(f'fill\n')
        else:
            self.file.write(f'stroke')

    def createFile(self):
        self.file.write(f'\n\n\n')
        self.file.write(f'showpage\n')
        self.file.write(f'%EOF\n')
        self.file.close()




