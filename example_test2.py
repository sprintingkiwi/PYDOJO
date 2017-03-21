from pydojo import *

# CREATE GAME DISPLAY
screen(1280, 720)

background('example_library/citynight.png')

uga = Actor()
uga.pendown()

pyco = Actor('example_library/pyco2.png')
pyco.scale(0.5)
pyco.load('example_library/pyco4.png')
pyco.load('example_library/pyco5.png')
pyco.load('example_library/pyco6.png')

passi = 1

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

    # UPDATE SCREEN
    update()
    # WAIT
    wait(100)