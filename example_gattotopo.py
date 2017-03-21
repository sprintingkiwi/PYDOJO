from pydojo import *

screen(800, 600)

background('example_library/carpet.png')

topo = Actor('example_library/mouse.png')
topo.scale(0.1)
topo.goto(400, 300)

gatto = Actor('example_library/cat.png')
gatto.scale(0.2)
gatto.goto(200, 100)

#MAIN LOOP
gameover = False
while not gameover:

    #CAT MOVEMENT
    gatto.point(topo)
    gatto.forward(1)

    #MOUSE (the animal) MOVEMENT
    if not topo.collidepoint(MOUSE):
        topo.point(MOUSE)
        topo.forward(4)

    if gatto.collide(topo):
        quit()

    #DRAW ACTORS
    # sfondo.draw()
    # topo.draw()
    # gatto.draw()

    #update screen and events queue
    update()

    #wait
    sleep(0.01)
