'''
Brief:
This file contains the Layer and Shape classes. All coordiantes are local to
the layer.
'''

class Layer(object):
    def __init__(self, app, layerName="", dist=10, isVisible=True):
        self.app = app
        self.layerName = layerName
        self.layerPos = (0, 0)
        self.dist = dist
        self.isVisible = isVisible
        self.visMouseHover = False
        self.shapes = [Shape("Square", [(-400, 400), (-200, 200)], "red", True),
                       Shape("Square", [(400, -400), (200, -200)], "green", True),
                       Shape("Square", [(-400, -400), (-200, -200)], "blue", True),
                       Shape("Square", [(400, 400), (200, 200)], "yellow", True)]

    def drawLayer(self, canvas):
        for shape in self.shapes:
            shape.drawShape(self.app, canvas, self.layerPos, self.dist)

class Shape(object):
    def __init__(self, type, vertices, fillColor, showOutline):
        self.type = type
        self.vertices = vertices
        self.fillColor = fillColor
        self.showOutline = showOutline

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
        
        width = 80/adjustedDist if self.showOutline else 0
        if (self.type == "Line"):
            canvas.create_line(newVertices, fill=self.fillColor, width=80/adjustedDist)
        elif (self.type == "Circle"):
            canvas.create_oval(newVertices, fill=self.fillColor, width=width)
        elif (self.type == "Square"):
            canvas.create_rectangle(newVertices, fill=self.fillColor, width=width)
        elif (self.type == "Triangle"):
            v1 = (newVertices[0][0], newVertices[1][1])
            v2 = ((newVertices[0][0] + newVertices[1][0]) / 2, 
                   newVertices[0][1])
            v3 = newVertices[1]
            canvas.create_polygon(v1, v2, v3, fill=self.fillColor, width=width)
