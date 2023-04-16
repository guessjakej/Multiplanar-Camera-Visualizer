'''
Brief:
This file contains classes for managing and drawing the UI.

Classes include:
-EditorUI
-ProgrammerUI
-PlaybackUI

Note:
Due to the nature of drawing a UI using hard-coded coordinates and allowing it
to be rescalable, much of the code in this file is difficult to understand.
Don't worry too much about the specifics of the calculations.
'''

##############################################################################

# Manages Editor UI data and draws UI on canvas
class EditorUI(object):
    def __init__(self, app):
        self.app = app
        self.leftMenuMargin = app.width * (1/16)
        self.rightMenuMargin = app.width * (3/16)

        # Keep track of these for darkening menu buttons on hover
        self.isCursorHover = False
        self.isColorHover = False
        self.isLineHover = False
        self.isCircleHover = False
        self.isTriangleHover = False
        self.isSquareHover = False
        self.isFreeformHover = False
        self.isEditorHover = False
        self.isProgrammerHover = False
        self.isPlaybackHover = False

    # Called whenever the mouse position changes
    def updateMouse(self, mouseX, mouseY):
        self.isCursorHover = self.mouseInCursorButton(mouseX, mouseY)
        self.isColorHover = self.mouseInColorButton(mouseX, mouseY)
        self.isLineHover = self.mouseInLineButton(mouseX, mouseY)
        self.isCircleHover = self.mouseInCircleButton(mouseX, mouseY)
        self.isTriangleHover = self.mouseInTriangleButton(mouseX, mouseY)
        self.isSquareHover = self.mouseInSquareButton(mouseX, mouseY)
        self.isFreeformHover = self.mouseInFreeformButton(mouseX, mouseY)
        self.isEditorHover = self.mouseInEditorButton(mouseX, mouseY)
        self.isProgrammerHover = self.mouseInProgrammerButton(mouseX, mouseY)
        self.isPlaybackHover = self.mouseInPlaybackButton(mouseX, mouseY)

    def mouseInCursorButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = (self.leftMenuMargin - width)/2 * ((0*7)+1)
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInColorButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = (self.leftMenuMargin - width)/2 * ((1*7)+1)
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInLineButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = (self.leftMenuMargin - width)/2 * ((2*7)+1)
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInCircleButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = (self.leftMenuMargin - width)/2 * ((3*7)+1)
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInTriangleButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = (self.leftMenuMargin - width)/2 * ((4*7)+1)
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInSquareButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = (self.leftMenuMargin - width)/2 * ((5*7)+1)
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInFreeformButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = (self.leftMenuMargin - width)/2 * ((6*7)+1)
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1

    def mouseInEditorButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = self.app.height - self.leftMenuMargin * (3-(3/8))
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInProgrammerButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = self.app.height - self.leftMenuMargin * (2-(2/8))
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1
    
    def mouseInPlaybackButton(self, x, y):
        width = self.leftMenuMargin * (6/8)
        height = width
        x0 = self.leftMenuMargin * (1/8)
        y0 = self.app.height - self.leftMenuMargin * (1-(1/8))
        x1 = x0 + width
        y1 = y0 + height
        return x0 <= x and x <= x1 and y0 <= y and y <= y1

    def draw(self, canvas):
        # Main sections
        self.drawBackground(canvas)
        self.drawDividers(canvas)

        # Left menu draw options
        self.drawCursorButton(canvas)
        self.drawColorButton(canvas)
        self.drawLineButton(canvas)
        self.drawCircleButton(canvas)
        self.drawTriangleButton(canvas)
        self.drawSquareButton(canvas)
        self.drawFreeformButton(canvas)

        # Left menu mode options
        self.drawEditorButton(canvas)
        self.drawProgrammerButton(canvas)
        self.drawPlaybackButton(canvas)

    def drawBackground(self, canvas):
        canvas.create_rectangle(0, 0, self.app.width, self.app.height,
                                fill="#606060", width=0)

    def drawDividers(self, canvas):
        width = self.app.width
        height = self.app.height
        
        # Left menu divider
        canvas.create_line(self.leftMenuMargin, 0, 
                           self.leftMenuMargin, height,
                           fill="black",width=5)
        
        # Left menu 3-menu / tools divider (horizontal)
        threeMenuHeight = self.app.height - self.leftMenuMargin * (3-(2/8))
        canvas.create_line(0, threeMenuHeight,
                           self.leftMenuMargin, threeMenuHeight,
                           fill="black",width=5) 
        
        # Right menu divider
        canvas.create_line(width - self.rightMenuMargin, 0, 
                           width - self.rightMenuMargin, height,
                           fill="black",width=5)
    
    def drawCursorButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - width)/2 * ((0*7)+1)

        # Background
        bgColor = "#808080" if self.isCursorHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Cursor
        canvas.create_polygon(x + width * 0.3, y + height * 0.1,
                              x + width * 0.3, y + height * 0.8,
                              x + width * 0.45, y + height * 0.7,
                              x + width * 0.55, y + height * 0.9,
                              x + width * 0.7, y + height * 0.8,
                              x + width * 0.6, y + height * 0.65,
                              x + width * 0.8, y + height * 0.65,
                              fill="white",outline="black",width=5)

        
    def drawColorButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - width)/2 * ((1*7)+1)

        # Background
        bgColor = "#808080" if self.isColorHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # 3 Colorful Circles
        radius = width * (2/8)
        # Red Circle
        rX, rY = x + width * 0.5, y + height * 0.35
        canvas.create_oval(rX - radius, rY - radius, rX + radius, rY + radius,
                           fill=None,outline="#FF0000",width=6)
        # Green Circle
        gX, gY = x + width * 0.35, y + height * 0.65
        canvas.create_oval(gX - radius, gY - radius, gX + radius, gY + radius,
                           fill=None,outline="#00FF00",width=6)
        # Blue Circle
        bX, bY = x + width * 0.65, y + height * 0.65
        canvas.create_oval(bX - radius, bY - radius, bX + radius, bY + radius,
                           fill=None,outline="#0000FF",width=6)
        
    def drawLineButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - width)/2 * ((2*7)+1)

        # Background
        bgColor = "#808080" if self.isLineHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Line
        canvas.create_rectangle(x + width * 0.2, y + height * 0.5, 
                                x + width * 0.8, y + height * 0.5, 
                                fill="black", width=8)
        
    def drawCircleButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - width)/2 * ((3*7)+1)

        # Background
        bgColor = "#808080" if self.isCircleHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Circle
        radius = width * (5/16)
        cX, cY = x + width * (1/2), y + height * (1/2)
        canvas.create_oval(cX - radius, cY - radius,
                           cX + radius, cY + radius, 
                            fill=None, width=8)
        
    def drawTriangleButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - width)/2 * ((4*7)+1)

        # Background
        bgColor = "#808080" if self.isTriangleHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        #Triangle
        x0, y0 = x + width * 0.2, y + height * 0.8
        x1, y1 = x + width * 0.5, y + height * 0.2
        x2, y2 = x + width * 0.8, y + height * 0.8
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x0, y0,
                              fill=bgColor, width=8, outline="black")
        
    def drawSquareButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - width)/2 * ((5*7)+1)

        # Background
        bgColor = "#808080" if self.isSquareHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Square
        canvas.create_rectangle(x + width * 0.2, y + height * 0.2,
                                x + width * 0.8, y + height * 0.8,
                                fill=None, width=8)
        
    def drawFreeformButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - width)/2 * ((6*7)+1)

        # Background
        bgColor = "#808080" if self.isFreeformHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Polygon
        x0, y0, = x + width * 0.15, y + height * 0.5
        x1, y1 = x + width * 0.5, y + height * 0.85
        x2, y2 = x + width * 0.5, y + height * 0.15
        x3, y3 = x + width * 0.85, y + height * 0.5
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x3, y3,
                              fill=bgColor, width=5, outline="black")
        # Create points
        radius = 7
        canvas.create_oval(x0 - radius, y0 - radius,
                           x0 + radius, y0 + radius,
                           fill="black")
        canvas.create_oval(x1 - radius, y1 - radius,
                           x1 + radius, y1 + radius,
                           fill="black")
        canvas.create_oval(x2 - radius, y2 - radius,
                           x2 + radius, y2 + radius,
                           fill="black")
        canvas.create_oval(x3 - radius, y3 - radius,
                           x3 + radius, y3 + radius,
                           fill="black")
        

        
    def drawEditorButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = self.app.height - self.leftMenuMargin * (3-(3/8))

        # Background
        bgColor = "#d0d0d0" if self.isEditorHover else "white"
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Pencil Tip
        tipX, tipY = x + width * (1/16), y + height * (15/16)
        tipSize = width * (2/8)
        canvas.create_polygon(tipX, tipY,
                              tipX + tipSize/2, tipY - tipSize,
                              tipX + tipSize, tipY - tipSize/2,
                              tipX, tipY,
                              fill="black", width=2, outline="black")
        
        # Pencil Body
        bodySize = width * (4/8)
        canvas.create_polygon(tipX + tipSize/2, tipY - tipSize,
                        tipX + tipSize/2 + bodySize, tipY - tipSize - bodySize,
                        tipX + tipSize + bodySize, tipY - tipSize/2 - bodySize,
                        tipX + tipSize, tipY - tipSize/2,
                        fill="#e3b612", width=2, outline="black")
        
        # Erasor
        erasorSize = width * (1/8)
        canvas.create_polygon(tipX + tipSize/2 + bodySize, 
                             tipY - tipSize - bodySize,
                             tipX + tipSize/2 + bodySize + erasorSize, 
                             tipY - tipSize - bodySize - erasorSize,
                             tipX + tipSize + bodySize + erasorSize, 
                             tipY - tipSize/2 - bodySize - erasorSize,
                             tipX + tipSize + bodySize, 
                             tipY - tipSize/2 - bodySize,
                             fill="#ff8fbe", width=2, outline="black")

    def drawProgrammerButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = self.app.height - self.leftMenuMargin * (2-(2/8))

        # Background
        bgColor = "#808080" if self.isProgrammerHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Colorful numbers
        canvas.create_text(x + width * (2/8), y + height * (2/8),
                           text="1", fill="#FF0000", font="Helvetica 22 bold",)
        canvas.create_text(x + width * (6/8), y + height * (3/8),
                           text="2", fill="#00FF00", font="Helvetica 22 bold")
        canvas.create_text(x + width * (3/8), y + height * (6/8),
                           text="3", fill="#0000FF", font="Helvetica 22 bold")
        
    def drawPlaybackButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = self.app.height - self.leftMenuMargin * (1-(1/8))

        # Background
        bgColor = "#808080" if self.isPlaybackHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + width, y + height, 
                                fill=bgColor, width=3)
        
        # Play Button
        triangleLength = width * (11/16)
        x0 = x + width * (1/4)
        y0 = y + (height - triangleLength)/2
        x1 = x0
        y1 = y + height - (height - triangleLength)/2
        x2 = x0 + ((triangleLength)/2)*(3**0.5)
        y2 = (y0 + y1)/2
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, x0, y0,
                              fill="white", width=3, outline="black")