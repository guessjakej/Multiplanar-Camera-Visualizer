'''
Brief:
This file contains the Layer class as well as any helper functions for managing
perspective calculations
'''

class Layer(object):
    def __init__(self, app, layerName="", x=0, y=0, dist=10, isVisible=False):
        self.app = app
        self.layerName = layerName
        self.x = x
        self.y = y
        self.dist = dist
        self.isVisible = isVisible
        self.visMouseHover = False