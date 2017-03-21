from pydojo import *

#create game display
screen(800, 600)

gobo = Actor('example_library/gobo.png')
gobo.scale(0.2)

while True:

    gobo.goto(MOUSE)

    gobo.right(5)

    if keydown(C):
        fill(BLACK)

    #update screen and events queue
    update()
