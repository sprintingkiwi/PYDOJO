from pydojo import *

# create game display
SCREEN(800, 600)

# CREATE ACTOR
pyco = Actor('example_library/pyco1.png')
pyco.scale(0.2)

# score variable
presi = 0

# CREATE SCORE TEXT
punti = Text(presi, color=red)
punti.goto(100, 100)

# counter variable
conta = 0

# MAIN LOOP
while True:
    # MOVE RANDOM each 60 cycles
    conta = conta + 1
    if conta > 60:
        pyco.gorand()
        conta = 0

    # ADD 1 POINT when target actor is clicked
    if pyco.click():
        presi = presi + 1
        punti.write(presi)

    # DRAW IMAGES
    fill(black)
    pyco.draw()
    punti.draw()

    # update screen and events queue
    UPDATE()

    # wait
    sleep(0.01)
