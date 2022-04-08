from stringArt import *
import parameters

# This lets you decide which parameters to change and what the values should be.
# For each image in paramDict['image'], a simulation will be run by changing each other parameter one at a time.
# Any parameters not being changed will be set to their defaults. 
# These defaults can be changed by changing the default values in the function definition of changeParameters()
paramDict = {
    'size' : [200, 400, 800, 100, 1600],
    'numHooks' : [100, 200, 300, 400, 500],
    'hookSkip' : [0, 10, 20, 40, 80],
    'lineWeight' : [1, 2, 3, 4],
    'numStrings' : [500, 1000, 2000, 3000, 4000],
    'image' : ['cat.jpg', 'bosch.jfif', 'eye.jpg', 'heart.png', 'einstein.png'],
    'contrast' : [5, 7, 9, 11, 13]
}

# Function that sets the parameters for the simulation
def changeParameters(size=1000, numStrings=4000, numHooks=288, lineWeight=1, hookSkip=20, image="bosch.jfif", contrast=13):
    parameters.Parameters.size = size
    parameters.Parameters.numHooks = numHooks
    parameters.Parameters.numStrings = numStrings
    parameters.Parameters.lineWeight = lineWeight
    parameters.Parameters.hookSkip = hookSkip
    parameters.Parameters.image = image
    parameters.Parameters.contrast = contrast

# Function that calls all the necessary methods in order to simulate stringArt.py
def createArt(outputName):
    img = getImage()
    img = processImage(img)
    hooks = generateHooks()
    lines, hookOrder = generateLinesFromHooks(img, hooks)
    # lines = growOldWithMeButFaster(img, hooks)
    generatePostScriptFile(lines, filename=outputName)
    createStringImage(lines, filename=outputName)

def main():
    for img in paramDict['image']:
        for key in paramDict:
            if key == 'image':
                continue
            for val in paramDict[key]:
                # If any changes are made here, it's good to keep in mind that eval() behaves weirdly with string variables.
                eval(f'changeParameters({key}={val}, image=img)')
                eval(f'createArt("-{key}-{val}")')


main()