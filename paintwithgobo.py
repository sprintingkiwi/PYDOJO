from actor import *

#create game display
SCREEN(800, 600)

gobo = Actor("library/gobo.png")
gobo.scale(0.2)


while True:

    gobo.goto(MOUSE)

    gobo.right(5)

    gobo.draw()

    if keydown(C):
        schermo.fill(black)

    #update screen and events queue
    UPDATE()

    #wait
    sleep(0.01)