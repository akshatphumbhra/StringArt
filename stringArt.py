from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.draw import line
import numpy as np 
from PIL import Image, ImageDraw
import math
from parameters import Parameters
import helpers
from postscript import PostScript


def getImage():
    size = (Parameters.size+1, Parameters.size+1)
    img = Image.open(Parameters.image).convert("L")
    img = img.resize(size)
    output = np.transpose(np.array(img))
    return output

# Contrast stretches images for better results
def processImage(img):
    def sigmoid(x, L=1, k=1, m=0):
        return L/(1+np.exp(-k*(x-m)))
    
    # sigmoid_img = sigmoid(img/255, k=13, m=0.5)*255
    sigmoid_img = sigmoid(img/255, k=Parameters.contrast, m=0.5)*255
    # helpers.imshow(sigmoid_img)
    return sigmoid_img


def generateHooks():
    radius = Parameters.size/2
    n = Parameters.numHooks
    hooks = np.array([[math.cos(np.pi*2*i/n), math.sin(np.pi*2*i/n)] for i in range(n)])
    hooks = (radius*hooks)
    hooks = hooks + radius 
    return hooks.astype(int)

# This is growOldWithMe but avoids duplicates to speed up a little
def growOldWithMeButFaster(img, hooks):
    lines = []
    allPairs = set()
    hookSkip = Parameters.hookSkip
    hookNums = [n for n in range(len(hooks))]
    for j in range(len(hookNums)):
        for k in range(j + 1 + hookSkip, j + len(hookNums) - hookSkip):
            k = k % len(hookNums)
            pair = (j, k)
            anti_pair = (k, j)
            if anti_pair not in allPairs:
                allPairs.add(pair)

    for i in range(Parameters.numStrings):
        bestLine = None
        bestHooks = None
        maxDarkness = 100000
        for pair in allPairs:
            newLine = helpers.bresenhamLine(hooks[pair[0]], hooks[pair[1]])
            numPoints = len(newLine)
            darkness = 0

            for p in range(numPoints):
                darkness += img[newLine[p][0], newLine[p][1]]

            avgDarkness = darkness/numPoints
            if avgDarkness < maxDarkness:
                bestLine = newLine
                bestHooks = pair
                maxDarkness = avgDarkness

        for point in bestLine:
            img[point] = 255

        lines.append((hooks[bestHooks[0]], hooks[bestHooks[1]]))
        allPairs.remove((bestHooks))
        helpers.printProgressBar(i, Parameters.numStrings - 1)

    return lines

# This brute forces every possible string combination to find the darkest
# It does not maintain hook order and may not be possible to recreate with a single length of string
def growOldWithMe(img, hooks):
    lines = []
    hookSkip = Parameters.hookSkip
    for i in range(Parameters.numStrings):
        bestLine = None
        bestHooks = None
        maxDarkness = 100000
        start1 = 1 + hookSkip
        end1 = 1 + len(hooks) - hookSkip
        for h1 in range(start1, end1):
            h1 = h1 % len(hooks)
            start2 = 1 + hookSkip
            end2 = 1 + len(hooks) - hookSkip
            for h2 in range(start2, end2):
                h2 = h2 % len(hooks)
                if h1 == h2:
                    continue
                newLine = helpers.bresenhamLine(hooks[h1], hooks[h2])
                numPoints = len(newLine)
                darkness = 0

                for p in range(numPoints):
                    darkness += img[newLine[p][0], newLine[p][1]]

                avgDarkness = darkness/numPoints
                if avgDarkness < maxDarkness:
                    bestLine = newLine
                    bestHooks = (h1, h2)
                    maxDarkness = avgDarkness

        for point in bestLine:
            img[point] = 255
        
        lines.append((hooks[bestHooks[0]], hooks[bestHooks[1]]))
        helpers.printProgressBar(i, Parameters.numStrings - 1)
    
    return lines

def generateLinesFromHooks(img, hooks):
    curHook = 1
    hookSkip = Parameters.hookSkip
    size = Parameters.size
    lines = []
    hookOrder = []
    hookOrder.append(curHook)
    # Loop for each string we want to add
    for i in range(Parameters.numStrings):
        bestLine = None
        newHook = None 
        points = set()
        maxDarkness = 100000
        start = curHook + 1 + hookSkip
        end = curHook + len(hooks) - hookSkip
        # Loop for each hook that we are checking to find best string to add
        for j in range(start, end):
            j = j % len(hooks)
            newLine = helpers.bresenhamLine(hooks[curHook], hooks[j])
            numPoints = len(newLine)

            darkness = 0 
            # Loop to sum over values in our current string
            for k in range(numPoints):
                darkness += img[newLine[k][0], newLine[k][1]]
            
            avgDarkness = darkness/numPoints
            if avgDarkness < maxDarkness:
                bestLine = newLine
                newHook = j
                maxDarkness = avgDarkness
        
        # Create set of points of chosen string to implement thickness using dilation mask
        points = set(bestLine)

        # Loop for dilation mask algorithm, that increases lineWeight
        for _ in range(Parameters.lineWeight):
            addPoints = set()
            for point in points:
                img[point] = 255
                if point[0] + 1 < size:
                    addPoints.add((point[0]+1, point[1]))
                if point[1] + 1 < size:
                    addPoints.add((point[0], point[1]+1))
                if point[0] - 1 >= 0:
                    addPoints.add((point[0]-1, point[1]))
                if point[1] - 1 >= 0:
                    addPoints.add((point[0], point[1]-1))
            points = addPoints
        
        lines.append((hooks[curHook], hooks[newHook]))
        hookOrder.append(newHook)
        curHook = newHook 
        helpers.printProgressBar(i, Parameters.numStrings - 1)
    
    return lines, hookOrder

def readLinesFromFile(filename, hooks):
    lines = []
    with open(filename, 'r') as f:
        temp = f.readlines()
    hookOrder = list(map(int, temp[0].split(',')))
    for i in range(len(hookOrder)-1):
        lines.append((hooks[hookOrder[i]], hooks[hookOrder[i+1]]))
    return lines
        
def generateHookOrder(hookOrder):
    with open ("hookOrder.txt", 'w') as f:
        order = hookOrder.join(' ')
        f.write(order)

def createStringImage(lines, filename='-string'):
    size = (Parameters.size+1, Parameters.size+1)
    output = Image.new('L', size, color=255)
    for line in lines:
        addLine = ImageDraw.Draw(output)
        addLine.line((line[0][0], line[0][1], line[1][0], line[1][1]), fill=0, width=0)
    output.save(Parameters.image.split('.')[0] + filename + ".png")

def generatePostScriptFile(lines, filename='-string'):
    s = Parameters.size - 1
    file = PostScript(Parameters.image.split('.')[0] + filename + ".eps", Parameters.size, Parameters.size)
    file.setLine(1, 1)
    file.setLineWidth(0.5)
    for line in lines:
        file.makeLine(s - line[0], s - line[1])
    file.createFile()

if __name__ == '__main__':
    img = getImage()
    if Parameters.shouldProcess:
        img = processImage(img)
    hooks = generateHooks()
    if Parameters.readFromFile:
        lines = readLinesFromFile(Parameters.filename, hooks)
    elif Parameters.growOld:
        lines = growOldWithMeButFaster(img, hooks)
    else:
        lines, hookOrder = generateLinesFromHooks(img, hooks)
    # lines = growOldWithMeButFaster(img, hooks)
    if Parameters.output == 'eps':
        generatePostScriptFile(lines)
    elif Parameters.output == 'png':
        createStringImage(lines)
    else:
        generatePostScriptFile(lines)
        createStringImage(lines)
