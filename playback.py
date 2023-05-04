

class Playback(object):
    def __init__(self, app):
        self.app = app
        self.playbackInitialized = False
        self.timeStamp = 0
        self.totalTime = 0
        self.layerPositions = dict()

    def initialize(self):
        self.timeStamp = 0
        self.totalTime = 0
        self.layerPositions = dict()
        self.playbackInitialized = False
        
        # Loop through and compile each layer program
        for layerIndex in range(1, len(self.app.layers)+1):
            prog = self.app.programmerUI.layerPrograms.get(layerIndex, "")
            currLayer = self.app.layers[layerIndex-1]

            currX, currY = currLayer.posOriginal
            currDist = currLayer.distOriginal
            currTime = 0
            
            progTokens = prog.split("|")

            # Iterate through each token and decode it
            while (len(progTokens) >= 2):
                pos = progTokens.pop(0).split(",")
                time = progTokens.pop(0)

                # Verify formatting is good
                if (len(pos) != 3 or not time.isnumeric() or int(time) <= currTime):
                    self.playbackInitialized = False
                    return
                
                posX, posY, dist = int(pos[0]), int(pos[1]), int(pos[2])
                time = int(time)

                deltaX = posX - currX
                deltaY = posY - currY
                deltaDist = dist - currDist
                deltaTime = time - currTime

                newPositions = []
                for i in range(deltaTime):
                    percentMove = i/deltaTime
                    moveFactor = easeInOutQuad(percentMove)
                    newX = currX + moveFactor * deltaX
                    newY = currY + moveFactor * deltaY
                    newDist = currDist + moveFactor * deltaDist

                    newPositions.append((newX, newY, newDist))

                layerPositions = self.layerPositions.get(layerIndex, [])
                layerPositions = layerPositions + newPositions
                self.layerPositions[layerIndex] = layerPositions

                currX, currY = currX + deltaX, currY + deltaY
                currDist = currDist + deltaDist
                currTime = time

                self.totalTime = max(self.totalTime, time)
        
        # Pad each layer with same position if it finishes early
        for layerIndex in range(1, len(self.app.layers)+1):
            if (len(self.layerPositions.get(layerIndex, [])) == 0):
                currLayer = self.app.layers[layerIndex-1]
                origX, origY, = currLayer.posOriginal
                origDist = currLayer.distOriginal
                self.layerPositions[layerIndex] = [(origX, origY, origDist)]
            while (len(self.layerPositions[layerIndex]) < self.totalTime):
                self.layerPositions[layerIndex].append(self.layerPositions[layerIndex][-1])


        self.playbackInitialized = (self.totalTime > 0)



    def update(self):
        for layerIndex in range(1, len(self.app.layers)+1):
            layer = self.app.layers[layerIndex-1]

            newPos = self.layerPositions[layerIndex][self.timeStamp]
            newX, newY, newDist = newPos

            layer.layerPos = (newX, newY)
            layer.dist = newDist

            self.timeStamp = min((self.timeStamp + 1), self.totalTime-1)
    
    def draw(self, canvas):
        # Draw background
        canvas.create_rectangle(0,0,self.app.width,self.app.height,
                                fill=self.app.view.bgColor, width=0)
        # Draw each layer
        for layer in self.app.layers:
            layer.drawLayerPayback(canvas)

    def resetLayers(self):
        for layer in self.app.layers:
            layer.layerPos = layer.posOriginal
            layer.dist = layer.distOriginal

#################################################
# Helper Functions
#################################################

# SOURCE: https://easings.net/#easeInOutQuad
def easeInOutQuad(x):
    if (x < 0.5):
        return 2*(x**2)
    else:
        return 1 - ((-2*x + 2)**2)/2