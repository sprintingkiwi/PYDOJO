from actor import *

#create game display
SCREEN(800, 600)

#CREATE MOUSE (the animal)
topo = Actor("library/mouse.png")
topo.scale(0.1)
topo.goto(400, 300)

#CREATE CAT
gatto = Actor("library/cat.png")
gatto.scale(0.2)
gatto.goto(200, 100)

#CREATE BACKGROUND
sfondo = Actor("library/carpet.png")
sfondo.scale(800, 600)
sfondo.goto(400, 300)


#MAIN LOOP
gameover = False
while not gameover:

    #SET ACTORS DIRECTION
    topo.point(mouse)
    gatto.point(topo)

    #SET ACTORS MOVEMENT
    topo.forward(4)
    gatto.forward(1)

    #DRAW ACTORS
    sfondo.draw()
    topo.draw()
    gatto.draw()

    #update screen and events queue
    UPDATE()

    #wait
    sleep(0.01)
