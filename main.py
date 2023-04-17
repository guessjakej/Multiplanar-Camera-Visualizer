from cmu_112_graphics import *
import ui
import layer

#################################################
# App
#################################################

def appStarted(app):
    app.timerDelay = 1000//60
    app.mouseMovedDelay = 1000//100
    app.mode = "editor"

    # Current magnification of view
    app.zoom = 1

    # List containing Layer objects
    app.layers = [layer.Layer(app, "Layer 1", x=0, y=0, dist=10, isVisible=True),
                  layer.Layer(app, "Layer 2", x=0, y=0, dist=15, isVisible=False)]
    app.selectedLayer = 0

    app.editorUI = ui.EditorUI(app)

#################################################
# Editor
#################################################

def editor_redrawAll(app, canvas):
    app.editorUI.draw(canvas)

def editor_mouseMoved(app, event):
    app.editorUI.updateMouse(event.x, event.y)

def editor_mousePressed(app, event):
    app.selectedLayer = (app.selectedLayer + 1) % 2 

#################################################
# main         
#################################################

def main():
    displayScale = 100
    w, h = 16*displayScale, 9*displayScale

    runApp(width=w, height=h) 

if __name__ == '__main__':
    main()