'''
Brief:
TODO

Note:
Due to the nature of drawing a UI using hard-coded coordinates and allowing it
to be rescalable, much of the code in this file is difficult to understand.
Don't worry too much about the specifics of the calculations.
'''

import layer

##############################################################################

# Manages Editor UI data and draws UI on canvas
class ProgrammerUI(object):
    def __init__(self, app):
        self.app = app
        self.leftMenuMargin = app.width * (1/16)
        self.rightMenuMargin = app.width * (3/16)

        # Keep track of these for darkening menu buttons on hover
        self.isPosHover = False
        self.isTimeHover = False
        self.isEditorHover = False
        self.isProgrammerHover = False
        self.isPlaybackHover = False

        # Dictionary mapping layer numbers to program strings
        self.layerPrograms = dict()

        # Dictionary mapping layer numbers to cursor positions in layer prog
        self.layerCursors = dict()

    def updateMousePressed(self, mouseX, mouseY):
        if self.isEditorHover:
            self.app.mode = "editor"
        else:
            self.updateSelectedLayer(mouseX, mouseY)
            

    # Called whenever the mouse position changes
    def updateMouseMoved(self, mouseX, mouseY):
        self.isPosHover = self.mouseInPosButton(mouseX, mouseY)
        self.isTimeHover = self.mouseInTimeButton(mouseX, mouseY)
        self.isEditorHover = self.mouseInEditorButton(mouseX, mouseY)
        self.isProgrammerHover = self.mouseInProgrammerButton(mouseX, mouseY)
        self.isPlaybackHover = self.mouseInPlaybackButton(mouseX, mouseY)

    def mouseInPosButton(self, mouseX, mouseY):
        size = self.leftMenuMargin * (6/8)
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - size)/2 * ((0*7)+1)
        return (x <= mouseX and mouseX <= x + size and
                y <= mouseY and mouseY <= y + size)
    
    def mouseInTimeButton(self, mouseX, mouseY):
        size = self.leftMenuMargin * (6/8)
        x = self.leftMenuMargin * (1/8)
        y = (self.leftMenuMargin - size)/2 * ((1*7)+1)
        return (x <= mouseX and mouseX <= x + size and
                y <= mouseY and mouseY <= y + size)

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
    
    def updateKeyPressed(self, key):
        if (key.lower() in ["enter", "return"]):
            layerProgram = self.layerPrograms.get(self.app.selectedLayer, "")
            if (layerProgram != "" and layerProgram[-1].isdigit()):
                layerProgram += "|"
                self.layerPrograms[self.app.selectedLayer] = layerProgram
        elif (key == "," or key.isdigit()):
            layerProgram = self.layerPrograms.get(self.app.selectedLayer, "")
            layerProgram += key
            self.layerPrograms[self.app.selectedLayer] = layerProgram
        elif (key.lower() == "backspace"):
            layerProgram = self.layerPrograms.get(self.app.selectedLayer, "")
            if (len(layerProgram) > 0):
                layerProgram = layerProgram[:len(layerProgram)-1]
                self.layerPrograms[self.app.selectedLayer] = layerProgram

    def draw(self, canvas):
        # Draw Background
        canvas.create_rectangle(0, 0, self.app.width, self.app.height,
                                fill="#201c1c",width=0)

        # Main sections
        self.drawDividers(canvas)
        
        # Left menu draw options
        size = self.leftMenuMargin * (6/8)
        self.drawPosButton(canvas, self.leftMenuMargin * (1/8), 
                           (self.leftMenuMargin - size)/2 * ((0*7)+1),
                           size)
        self.drawTimeButton(canvas, self.leftMenuMargin * (1/8),
                            (self.leftMenuMargin - size)/2 * ((1*7)+1),
                            size)

        # Left menu mode options
        self.drawEditorButton(canvas)
        self.drawProgrammerButton(canvas)
        self.drawPlaybackButton(canvas)

        # Right side menu
        self.drawLayerHeader(canvas)
        self.drawLayerList(canvas)

        # Draw layer program lines
        self.drawLayerProgram(canvas)

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
        
    def drawPosButton(self, canvas, x, y, size):

        # Background
        bgColor = "#808080" if self.isPosHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + size, y + size, 
                                fill=bgColor, width=3)
        
        # Cursor
        self.drawTack(canvas, x, y, size)

    def drawTack(self, canvas, x, y, size):
        # Needle line
        canvas.create_line(x + size*0.4,  y + size*0.9,
                           x + size*0.625, y + size*0.325,
                           width=5, fill="#212121")
        # Needle Shine
        canvas.create_line((x + size*0.4)-2,  y + size*0.9,
                           (x + size*0.625)-2, y + size*0.325,
                           width=2, fill="#606060")

        # Ball
        canvas.create_oval(x + size*0.4, y + size*0.1,
                           x + size*0.85, y + size*0.55,
                           fill="#d00000", width=0)
        
        # Ball Shine
        canvas.create_oval(x + size*0.48, y + size*0.18,
                           x + size*0.7, y + size*0.4,
                           fill="#ff7a7a", width=0)
        canvas.create_oval(x + size*0.53, y + size*0.23,
                           x + size*0.65, y + size*0.35,
                           fill="white", width=0)

    def drawTimeButton(self, canvas, x, y, size):

        # Background
        bgColor = "#808080" if self.isTimeHover else "#b0b0b0" 
        canvas.create_rectangle(x, y, x + size, y + size, 
                                fill=bgColor, width=3)
        
        # Cursor
        self.drawClock(canvas, x, y, size)

    def drawClock(self, canvas, x, y, size):
        # Clock Base
        canvas.create_oval(x + size*0.1, y + size*0.1,
                           x + size*0.9, y + size*0.9,
                           fill="white", outline="black", width=3)
        
        # Clock hands
        canvas.create_line(x + size*0.5, y + size*0.5,
                           x + size*0.5, y + size*0.2,
                           fill="black", width=3)
        canvas.create_line(x + size*0.5, y + size*0.5,
                           x + size*0.7, y + size*0.3,
                           fill="black", width=3)
        
    def drawEditorButton(self, canvas):
        width = self.leftMenuMargin * (6/8)
        height = width
        x = self.leftMenuMargin * (1/8)
        y = self.app.height - self.leftMenuMargin * (3-(3/8))

        # Background
        bgColor = "#808080" if self.isEditorHover else "#b0b0b0" 
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
        bgColor = "white"
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
        
    def drawLayerHeader(self, canvas):
        x = self.app.width - (self.rightMenuMargin / 2)
        y = 75
        canvas.create_text(x,y,text="Layers",font="Helvetica 50 bold",
                           fill="#c0c0c0")

    def drawLayerList(self, canvas):
        startX = self.app.width - self.rightMenuMargin*0.95
        startY = 200
        boxSize = 40
        for i in range(len(self.app.layers)+1):
            if (i == 0):
                # Background Layer

                # Draw Visibility Box
                canvas.create_rectangle(startX, startY, 
                                        startX+boxSize, startY+boxSize,
                                        fill="#a0a0a0",outline="black",width=5)
                
                # Draw X in box. BG always visible
                canvas.create_line(startX+7, startY+7,
                                startX+boxSize-7, startY+boxSize-7,
                                fill="black",width=5)
                canvas.create_line(startX+7, startY+boxSize-7,
                                startX+boxSize-7, startY+7,
                                fill="black",width=5)
                
                # Draw layer name text
                canvas.create_text(startX+boxSize*1.3, startY+boxSize*0.5,
                                text="Background",font="Helvetica 25 bold",
                                anchor="w",fill="#a0a0a0")
            else:
                # Regular Layer

                currLayer = self.app.layers[i-1]
                # Draw Visibility Box
                canvas.create_rectangle(startX, startY, 
                                        startX+boxSize, startY+boxSize,
                                        fill="white",outline="black",width=5)
                
                # Draw X in box if layer visible
                if currLayer.isVisible:
                    canvas.create_line(startX+7, startY+7,
                                    startX+boxSize-7, startY+boxSize-7,
                                    fill="black",width=5)
                    canvas.create_line(startX+7, startY+boxSize-7,
                                    startX+boxSize-7, startY+7,
                                    fill="black",width=5)
                
                # Draw layer name text
                layerDist = currLayer.dist - self.app.view.cameraDepth
                textColor = "white" if (layerDist > 0) else "#808080"
                canvas.create_text(startX+boxSize*1.3, startY+boxSize*0.5,
                                text=f"{currLayer.layerName}",font="Helvetica 25 bold",
                                anchor="w",fill=textColor)
            
            # Box the currently selected layer
            if self.app.selectedLayer == i:
                canvas.create_rectangle(startX-10, startY-10,
                                        self.app.width-10, startY+boxSize+10,
                                        fill=None,outline="white",width=5)
            
            startY += 60

    def drawLayerProgram(self, canvas):
        layerProgram = self.layerPrograms.get(self.app.selectedLayer, "")
        posX = self.app.width * 0.11
        timeX = self.app.width * 0.6
        startY = self.app.height * 0.15
        imageSize = 100
        firstLine = True

        # Get list of tokens
        tokenList = layerProgram.split("|")
        if (len(tokenList) > 0):
            tokenList[-1] = tokenList[-1] + "_"
        tokenType = "pos"
        
        # Iterate through each token and draw it
        while (len(tokenList) > 0):
            token = tokenList.pop(0)
            if (tokenType == "pos"):
                self.drawTack(canvas, posX, startY-imageSize, imageSize)
                canvas.create_text(posX + imageSize, startY, text=token,
                                   font="Helvetica 50", fill="white",
                                   anchor="sw")
                tokenType = "time"
                if (not firstLine):
                    canvas.create_line(self.app.width*0.11, startY-130,
                                       self.app.width * 0.79, startY-130,
                                       fill="#bdbdbd", width=4)
            else:
                self.drawClock(canvas, timeX, startY-imageSize, imageSize)
                canvas.create_text(timeX + imageSize, startY, text=token,
                                   font="Helvetica 50", fill="white",
                                   anchor="sw")
                tokenType = "pos"
                startY += 150
            firstLine = False

            
    
    def updateSelectedLayer(self, x, y):
        startX = self.app.width - self.rightMenuMargin*0.95
        startY = 200
        boxSize = 40
        for i in range(len(self.app.layers)+1):
            if (i == 0):
                if (startX-10 <= x and x <= self.app.width-10 and
                    startY-10 <= y and y <= startY+boxSize+10):
                    self.app.selectedLayer = i
            else:
                layer = self.app.layers[i-1]
                if layer.visMouseHover:
                    layer.isVisible = not layer.isVisible
                elif (startX-10 <= x and x <= self.app.width-10 and
                    startY-10 <= y and y <= startY+boxSize+10):
                    self.app.selectedLayer = i
            startY += 60