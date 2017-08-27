from pydojo import *

# CREATE GAME DISPLAY
screen(1280, 720)

background('example_asset/backgrounds/field.png')
loadbackground('example_asset/backgrounds/bedroom.png')

uga = Actor()
uga.pendown()

pyco = Actor('example_asset/characters/pyco2.png')
pyco.load('example_asset/characters/pyco4.png')
pyco.load('example_asset/characters/pyco5.png')
pyco.load('example_asset/characters/pyco6.png')

pyco.show()

passi = 1

print(pyco.costumes)

print(pyco.getposition())

write(load("time_dyno"))

# MAIN LOOP
while True:

    # print pyco.direction, pyco.heading

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
    print pyco.direction

    if keydown(B):
        setbackground('bedroom')
        # background('example_library/bedroom.png')
    if keydown(C):
        setbackground('citynight')
    if keydown(F):
        fill(TOMATO)
        print screen_info.backgrounds

    if keydown(H):
        print "flip!"
        pyco.flip('horizontal')
    if keydown(V):
        print "flip!"
        pyco.flip('vertical')

    wait(100)

    # UPDATE SCREEN
    update()