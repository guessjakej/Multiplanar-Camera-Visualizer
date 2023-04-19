'''
Brief:
This file contains the Layer and Shape classes. All coordiantes are local to
the layer.
'''

class Layer(object):
    def __init__(self, app, layerName="", x=0, y=0, dist=10, isVisible=True):
        self.app = app
        self.layerName = layerName
        self.layerPos = (x, y)
        self.dist = dist
        self.isVisible = isVisible
        self.visMouseHover = False
        self.shapes = [Shape("Rectangle", [(-400, 400), (-200, 200)], "red"),
                       Shape("Rectangle", [(400, -400), (200, -200)], "green"),
                       Shape("Rectangle", [(-400, -400), (-200, -200)], "blue"),
                       Shape("Rectangle", [(400, 400), (200, 200)], "yellow")]

    def drawLayer(self, canvas):
        for shape in self.shapes:
            shape.drawShape(self.app, canvas, self.layerPos, self.dist)

class Shape(object):
    def __init__(self, type, vertices, fillColor):
        self.type = type
        self.vertices = vertices
        self.fillColor = fillColor

    def drawShape(self, app, canvas, layerPos, dist):
        layerX, layerY = layerPos
        newVertices = []
        
        # True distance of layer from camera
        adjustedDist = dist - app.view.cameraDepth
        if (adjustedDist <= 0): # Can't see objects behind camera
            return
        
        for (x, y) in self.vertices:
            newX, newY = app.view.layerPosToCanvas(x+layerX, y+layerY, 
                                                   adjustedDist)
            newVertices.append((newX, newY))
        
        if (self.type == "Rectangle"):
            canvas.create_rectangle(newVertices, fill=self.fillColor, width=80/adjustedDist)
