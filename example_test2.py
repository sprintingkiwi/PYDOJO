from pydojo import *

# CREATE GAME DISPLAY
screen(1280, 720)

background('example_asset/backgrounds/citynight.png')
loadbackground('example_asset/backgrounds/bedroom.png')

print(screen_info.background.costumes)

uga = Actor()
uga.pendown()

pyco = Actor('example_asset/characters/pyco2.png')
pyco.scale(0.5)
pyco.load('example_asset/characters/pyco4.png')
pyco.load('example_asset/characters/pyco5.png')
pyco.load('example_asset/characters/pyco6.png')

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
    pyco.nextcostume(pause=1)
    pyco.right(10)

    if keydown(B):
        setbackground('bedroom')
        # background('example_library/bedroom.png')
        print(screen_info.background.costumes)
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