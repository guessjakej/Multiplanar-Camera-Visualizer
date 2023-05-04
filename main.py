from cmu_112_graphics import *
import editor_ui
import programmer_ui
import layer
import view

#################################################
# App
#################################################

def appStarted(app):
    app.timerDelay = 1000//60
    app.mouseMovedDelay = 1000//100
    app.mode = "editor"

    # Controls
    app.heldKeys = set()
    app.choosingColor = False
    app.selectedColor = None
    app.typedColor = "#"
    app.drawOutline = True

    # List containing Layer objects
    app.layers = [layer.Layer(app, "Layer 3", dist=50, isVisible=True),
                  layer.Layer(app, "Layer 2", dist=30, isVisible=True),
                  layer.Layer(app, "Layer 1", dist=10, isVisible=True)]
    app.selectedLayer = 0
    app.undoHistory = dict()
    

    # Display
    app.editorUI = editor_ui.EditorUI(app)
    app.view = view.View(app)
    app.programmerUI = programmer_ui.ProgrammerUI(app)

#################################################
# Editor
#################################################

def editor_redrawAll(app, canvas):
    app.view.drawMainView(canvas)
    app.editorUI.draw(canvas)

def editor_mousePressed(app, event):
    if app.choosingColor:
        app.editorUI.updateMousePressedColor(event.x, event.y)
    else:
        app.editorUI.updateMousePressed(event.x, event.y)

def editor_mouseMoved(app, event):
    if app.choosingColor:
        return
    
    app.editorUI.updateMouseMoved(event.x, event.y)

def editor_keyPressed(app, event):
    # Currently drawing a shape. Ignore inputs
    if app.editorUI.drawingShape:
        if event.key.lower() == "escape":
            app.editorUI.drawingShape = False
            app.layers[app.selectedLayer-1].shapes.pop()

    # Currently in color typing menu
    if app.choosingColor:
        # Confirm selection. Format accordingly.
        if (event.key == "Enter" or event.key == "Return"):
            if (len(app.typedColor) == 7 and strIsHex(app.typedColor)):
                if app.selectedLayer == 0:
                    app.view.bgColor = app.typedColor
                else:
                    app.selectedColor = app.typedColor

                app.choosingColor = False
                app.editorUI.isColorHover = False
                app.editorUI.colorSelectHeader = "Type in Color #Hexcode:"
            else:
                app.editorUI.colorSelectHeader = "Invalid Format (Ex: #ff81EA)"

        # Remove last character
        elif (event.key.lower() == "backspace"):
            if (len(app.typedColor) > 1):
                app.typedColor = app.typedColor[:len(app.typedColor)-1]

        elif (event.key.lower() == "escape"):
            if app.selectedColor != None:
                app.typedColor = app.selectedColor
            app.choosingColor = False
            app.editorUI.isColorHover = False
            app.editorUI.colorSelectHeader = "Type in Color #Hexcode:"

        # Add key to selection.
        else:
            if event.key == "Space":
                return
            charLimit = 7
            if (len(app.typedColor) < charLimit):
                app.typedColor += event.key

    # Undo
    elif (event.key.lower() == "left" and app.selectedLayer > 0):
        currLayer = app.layers[app.selectedLayer-1]
        if len(currLayer.shapes) > 0:
            layerHistory = app.undoHistory.get(app.selectedLayer, [])
            layerHistory.append(currLayer.shapes.pop())
            app.undoHistory[app.selectedLayer] = layerHistory

    # Redo
    elif (event.key.lower() == "right" and app.selectedLayer > 0 and
          len(app.undoHistory.get(app.selectedLayer, [])) > 0):
        currLayer = app.layers[app.selectedLayer-1]
        layerHistory = app.undoHistory.get(app.selectedLayer, [])
        newShape = layerHistory.pop()
        currLayer.shapes.append(newShape)
    
    # Not in color selection menu. Add key to set of held keys
    else:
        app.heldKeys.add(event.key)

def editor_keyReleased(app, event):
    if event.key in app.heldKeys:
        app.heldKeys.remove(event.key)

def editor_timerFired(app):
    dist = 30 # Amount to change distance by
    depth = 1 # Amount to change depth by
    for key in app.heldKeys:
        # Camera Controls
        if (key == "w"):
            app.view.viewPos = (app.view.viewPos[0], app.view.viewPos[1]-dist)
        elif (key == "a"):
            app.view.viewPos = (app.view.viewPos[0]-dist, app.view.viewPos[1])
        elif (key == "s"):
            app.view.viewPos = (app.view.viewPos[0], app.view.viewPos[1]+dist)
        elif (key == "d"):
            app.view.viewPos = (app.view.viewPos[0]+dist, app.view.viewPos[1])
        elif (key == "e"):
            app.view.cameraDepth += depth
        elif (key == "q"):
            app.view.cameraDepth -= depth

        # Layer Controls
        elif (key == "u"):
            if (app.selectedLayer > 0):
                app.layers[app.selectedLayer-1].dist -= depth
                sortLayers(app)
        elif (key == "o"):
            if (app.selectedLayer > 0):
                app.layers[app.selectedLayer-1].dist += depth
                sortLayers(app)

#################################################
# Programmer
#################################################

def programmer_redrawAll(app, canvas):
    app.programmerUI.draw(canvas)

def programmer_mousePressed(app, event):
    app.programmerUI.updateMousePressed(event.x, event.y)

def programmer_mouseMoved(app, event):
    app.programmerUI.updateMouseMoved(event.x, event.y)

def programmer_keyPressed(app, event):
    app.programmerUI.updateKeyPressed(event.key)

#################################################
# Helper Functions
#################################################

# Takes a string and returns whether or not it's a hex number
def strIsHex(s):
    s = s.lower()
    valid = "#0123456789abcdef"
    for char in s:
        if char not in valid:
            return False
        
    return True

# Put layers in reverse-distance order. Update app.selectedLayer
# PRE: Layer list can be sorted with at most one swap
def sortLayers(app):
    index = 1
    while (index < len(app.layers)):
        currLayer = app.layers[index-1]
        nextLayer = app.layers[index]
        if (currLayer.dist < nextLayer.dist):
            app.layers[index-1] = nextLayer
            app.layers[index] = currLayer
            if (app.selectedLayer == index):
                app.selectedLayer += 1
            elif (app.selectedLayer == index + 1):
                app.selectedLayer -= 1
            return
        index += 1


#################################################
# main         
#################################################

def main():
    displayScale = 100
    w, h = 16*displayScale, 9*displayScale

    runApp(width=w, height=h) 

if __name__ == '__main__':
    main()