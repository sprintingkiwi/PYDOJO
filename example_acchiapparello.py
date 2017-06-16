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

# MAIN LOOP
while True:

    # MOUSE.hide()

    # print "left: " + str(MOUSE.left)
    # print "leftdown: " + str(MOUSE.leftdown)
    # print "leftup: " + str(MOUSE.leftup)
    # print "central: " + str(MOUSE.central)
    # print "centraldown: " + str(MOUSE.centraldown)
    # print "centralup: " + str(MOUSE.centralup)
    # print "right: " + str(MOUSE.right)
    # print "rightdown: " + str(MOUSE.rightdown)
    # print "rightup: " + str(MOUSE.rightup)
    # print ""

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
