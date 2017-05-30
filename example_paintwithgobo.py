from pydojo import *

#create game display
screen(800, 600)

gobo = Actor('example_asset/characters/gobo.png')
gobo.scale(0.2)

while True:

    gobo.goto(MOUSE)
    gobo.stamp()
    gobo.right(5)

    if keydown(C):
        clear()
    if keydown(L):
        fill(LAVENDER)
    if keydown(P):
        fill(PINK)

    #update screen and events queue
    update()
