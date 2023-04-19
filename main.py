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

    # List containing Layer objects
    app.layers = [layer.Layer(app, "Layer 1", x=0, y=0, dist=10, isVisible=True),
                  layer.Layer(app, "Layer 2", x=0, y=0, dist=15, isVisible=False)]
    app.selectedLayer = 0

    app.editorUI = ui.EditorUI(app)
    app.view = view.View(app)

#################################################
# Editor
#################################################

def editor_redrawAll(app, canvas):
    app.view.drawMainView(canvas)
    app.editorUI.draw(canvas)

def editor_mouseMoved(app, event):
    app.editorUI.updateMouse(event.x, event.y)

def editor_mousePressed(app, event):
    pass

#################################################
# Helper Functions
#################################################

#################################################
# main         
#################################################

def main():
    displayScale = 90
    w, h = 16*displayScale, 9*displayScale

    runApp(width=w, height=h) 

if __name__ == '__main__':
    main()