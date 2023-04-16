from cmu_112_graphics import *
import ui

#################################################
# App
#################################################

def appStarted(app):
    app.timerDelay = 1000//60
    app.mouseMovedDelay = 1000//100
    app.mode = "editor"

    app.editorUI = ui.EditorUI(app)

#################################################
# Editor
#################################################

def editor_redrawAll(app, canvas):
    app.editorUI.draw(canvas)

def editor_mouseMoved(app, event):
    app.editorUI.updateMouse(event.x, event.y)

#################################################
# main         
#################################################

def main():
    displayScale = 100
    w, h = 16*displayScale, 9*displayScale

    runApp(width=w, height=h) 

if __name__ == '__main__':
    main()