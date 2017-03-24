from pydojo import *

# CREATE GAME DISPLAY
screen(1280, 720)

background('example_library/citynight.png')
loadbackground('example_library/bedroom.png')

print(screenInfo.background.costumes)

uga = Actor()
uga.pendown()

pyco = Actor('example_library/pyco2.png')
pyco.scale(0.5)
pyco.load('example_library/pyco4.png')
pyco.load('example_library/pyco5.png')
pyco.load('example_library/pyco6.png')

passi = 1

print(pyco.costumes)

print(pyco.getposition())

# MAIN LOOP
while True:

    # Move the Turtle
    for colore in COLORS:
        uga.forward(passi)
        uga.right(10)
        uga.pensize += 1
        passi += 1
        uga.pencolor = colore

    # Loop Pyco's costumes
    pyco.nextcostume()

    if keydown(B):
        setbackground('bedroom')
        # background('example_library/bedroom.png')
        print(screenInfo.background.costumes)
    if keydown(C):
        setbackground('citynight')
    if keydown(F):
        fill(TOMATO)

    if keydown(H):
        pyco.flip('horizontal')
    if keydown(V):
        pyco.flip('vertical')

    wait(100)

    # UPDATE SCREEN
    update()