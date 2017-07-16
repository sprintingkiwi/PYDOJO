from pydojo import *

# create game display
screen(1280, 720)

# CREATE ACTOR
pyco = Actor('example_asset/characters/pyco1.png')

# score variable
presi = 0

# CREATE SCORE TEXT
punti = Text(presi, color=RED)
punti.goto(100, 100)

# counter variable
inizioconta = ticks()

pyco.pendown()

# Point bug?
# prova = Actor()
# print type(180 - pyco.direction)
# pyco.point(90 - prova.direction)

# MAIN LOOP
while True:

    # MOVE RANDOM
    if ticks() - inizioconta > 1000:
        pyco.gorand()
        inizioconta = ticks()

    # ADD 1 POINT when target actor is clicked
    if pyco.click():
        presi = presi + 1
        punti.write(presi)

    if pyco.rightclick():
        print("You must left-click Pyco!")

    # update screen and events queue
    update()
