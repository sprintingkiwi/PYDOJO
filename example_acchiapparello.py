from pydojo import *

# create game display
screen(800, 600)

# CREATE ACTOR
pyco = Actor('example_library/pyco1.png')
pyco.scale(0.2)

# score variable
presi = 0

# CREATE SCORE TEXT
punti = Text(presi, color=red)
punti.goto(100, 100)

# counter variable
inizioconta = time()

# MAIN LOOP
while True:
    # MOVE RANDOM each 60 cycles
    if time() - inizioconta > 1:
        pyco.gorand()
        inizioconta = time()

    # ADD 1 POINT when target actor is clicked
    if pyco.click():
        presi = presi + 1
        punti.write(presi)

    # DRAW IMAGES
    fill(black)
    pyco.draw()
    punti.draw()

    # update screen and events queue
    update()

    # wait
    wait(100)