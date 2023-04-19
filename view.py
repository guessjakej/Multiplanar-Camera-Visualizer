'''
Brief:
This file provides routines for building and managing the viewing window
'''

#############################################################################

class View(object):
    def __init__(self, app):
        self.app = app
        self.viewPos = (0,0)
        self.cameraDepth = 0
        self.viewX = self.app.width * (2/16)
        self.viewY = self.app.height * (2.5/16)
        self.viewWidth = self.app.width*(10/16)
        self.viewHeight = self.viewWidth*(9/16)
        self.viewDistance = 10 
        self.bgColor = "white"

    def drawMainView(self, canvas):
        x = self.app.view.viewX
        y = self.app.view.viewY
        width = self.app.view.viewWidth
        height = self.app.view.viewHeight

        # Draw background
        canvas.create_rectangle(0, 0, self.app.width, self.app.height,
                                fill=self.bgColor,width=0)

        # Draw each layer
        for layer in self.app.layers[::-1]: # Draw furthest back first
            layer.drawLayer(canvas)

        # Background of UI (with hole in middle for view)
        canvas.create_rectangle(0, 0, self.app.width, y,
                                fill="#606060", width=0)
        canvas.create_rectangle(x+width, y, self.app.width, y+height,
                                fill="#606060", width=0)
        canvas.create_rectangle(0, y+height, self.app.width, self.app.height,
                                fill="#606060", width=0)
        canvas.create_rectangle(0, y, x, y+height,
                                fill="#606060", width=0)
        
        # Border of view
        canvas.create_rectangle(x, y, x+width, y+height,
                                fill=None,outline="black",width=5)

    # Converts raw canvas position to position in layer at given distance
    def canvasToLayerPos(self, x, y, dist):
        viewX, viewY = self.canvasToView(x, y)
        return self.viewToLayerPos(viewX, viewY, dist)

    # Converts raw canvas position to adjusted position in view
    # (Aspect ratio app.width X app.height)
    def canvasToView(self, x, y):
        viewX = ((x - self.viewX)/self.viewWidth)*self.app.width
        viewY = ((y - self.viewY)/self.viewHeight)*self.app.height
        return viewX, viewY

    # Converts view position to position on layer given a distance
    def viewToLayerPos(self, viewX, viewY, dist):
        centerX, centerY = self.viewPos
        viewDistance = self.viewDistance

        # Speed scaling at dist compared to viewDist
        parallaxFactor = viewDistance/dist 

        layerX = (viewX - self.app.width/2)*(1/parallaxFactor) + centerX
        layerY = (viewY - self.app.height/2)*(1/parallaxFactor) + centerY
        return layerX, layerY

    # Converts position in layer at given distance to raw canvas position
    def layerPosToCanvas(self, layerX, layerY, dist):
        viewX, viewY = self.layerPosToView(layerX, layerY, dist)
        return self.viewToCanvas(viewX, viewY)

    # Converts position on layer at given distance to view position
    def layerPosToView(self, layerX, layerY, dist):
        centerX, centerY = self.viewPos
        viewDistance = self.viewDistance

        # Speed scaling at dist compared to viewDist
        parallaxFactor = viewDistance/dist 

        viewX = parallaxFactor*(layerX - centerX) + (self.app.width/2)
        viewY = parallaxFactor*(layerY - centerY) + (self.app.height/2)
        return viewX, viewY

    # Converts adjusted view position to raw canvas position
    def viewToCanvas(self, vX, vY):
        x = vX * (self.viewWidth/self.app.width) + self.viewX
        y = vY * (self.viewHeight/self.app.height) + self.viewY
        return x, y