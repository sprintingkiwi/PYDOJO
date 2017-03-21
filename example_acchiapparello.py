from pydojo import *

# create game display
screen(1920, 1080)

# CREATE ACTOR
pyco = Actor('example_library/pyco1.png')
pyco.scale(0.2)

# score variable
presi = 0

# CREATE SCORE TEXT
punti = Text(presi, color=RED)
punti.goto(100, 100)

# counter variable
inizioconta = time()

# MAIN LOOP
while True:
    # MOVE RANDOM
    if time() - inizioconta > 0:
        pyco.gorand()
        inizioconta = time()

    # ADD 1 POINT when target actor is clicked
    if pyco.click():
        presi = presi + 1
        punti.write(presi)

    # update screen and events queue
    update()