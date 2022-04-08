from matplotlib import pyplot as plt


def bresenhamLine(start, end):
    start = list(start)
    end = list(end)
    path = []
    steep = abs(end[1]-start[1]) > abs(end[0]-start[0])

    def swap(n1,n2):
        return [n2,n1]

    if steep:
        start = swap(start[0],start[1])
        end = swap(end[0],end[1])

    if start[0] > end[0]:
        _x0 = int(start[0])
        _x1 = int(end[0])
        start[0] = _x1
        end[0] = _x0

        _y0 = int(start[1])
        _y1 = int(end[1])
        start[1] = _y1
        end[1] = _y0

    dx = end[0] - start[0]
    dy = abs(end[1] - start[1])
    error = 0
    derr = dy/float(dx)

    ystep = 0
    y = start[1]

    if start[1] < end[1]: ystep = 1
    else: ystep = -1

    for x in range(start[0],end[0]+1):
        if steep:
            path.append((y,x))
        else:
            path.append((x,y))

        error += derr

        if error >= 0.5:
            y += ystep
            error -= 1.0

    return path

def bresenhamCircle(radius):
    # init vars
    switch = 3 - (2 * radius)
    points = set()
    x = 0
    y = radius
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        # first quarter first octant
        points.add((x,-y))
        # first quarter 2nd octant
        points.add((y,-x))
        # second quarter 3rd octant
        points.add((y,x))
        # second quarter 4.octant
        points.add((x,y))
        # third quarter 5.octant
        points.add((-x,y))
        # third quarter 6.octant
        points.add((-y,x))
        # fourth quarter 7.octant
        points.add((-y,-x))
        # fourth quarter 8.octant
        points.add((-x,-y))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
    return points

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# imshow with better defaults
def imshow(img, scale=1):
    plt.figure(figsize=(scale*8,scale*8))
    plt.imshow(img, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    plt.axis('off')
    plt.show()