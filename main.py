from cmu_112_graphics import *
import ui
import layer
import view

#################################################
# App
#################################################

def appStarted(app):
    app.timerDelay = 1000//60
    app.mouseMovedDelay = 1000//100
    app.mode = "editor"

    # Current magnification of view
    app.zoom = 1

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
    app.editorUI = ui.EditorUI(app)
    app.view = view.View(app)

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
    elif (event.key.lower() == "q" and app.selectedLayer > 0):
        currLayer = app.layers[app.selectedLayer-1]
        if len(currLayer.shapes) > 0:
            layerHistory = app.undoHistory.get(app.selectedLayer, [])
            layerHistory.append(currLayer.shapes.pop())
            app.undoHistory[app.selectedLayer] = layerHistory

    # Redo
    elif (event.key.lower() == "e" and app.selectedLayer > 0 and
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
    dist = 30
    for key in app.heldKeys:
        if (key == "w"):
            app.view.viewPos = (app.view.viewPos[0], app.view.viewPos[1]-dist)
        elif (key == "a"):
            app.view.viewPos = (app.view.viewPos[0]-dist, app.view.viewPos[1])
        elif (key == "s"):
            app.view.viewPos = (app.view.viewPos[0], app.view.viewPos[1]+dist)
        elif (key == "d"):
            app.view.viewPos = (app.view.viewPos[0]+dist, app.view.viewPos[1])
        elif (key == "Up"):
            app.view.cameraDepth += 1
        elif (key == "Down"):
            app.view.cameraDepth -= 1


    
    

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


#################################################
# main         
#################################################

def main():
    displayScale = 100
    w, h = 16*displayScale, 9*displayScale

    runApp(width=w, height=h) 

if __name__ == '__main__':
    main()