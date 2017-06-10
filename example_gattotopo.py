from pydojo import *

screen(800, 600)

background('example_asset/backgrounds/carpet.png')

topo = Actor('example_asset/characters/mouse.png')
topo.scale(0.3)
topo.goto(400, 300)
# topo.rotation = 'flip'

gatto = Actor('example_asset/characters/cat.png')
gatto.scale(0.5)
gatto.goto(200, 100)
# gatto.rotation = 'flip'

#MAIN LOOP
gameover = False
while not gameover:

    #CAT MOVEMENT
    gatto.point(topo)
    gatto.forward(1)

    #MOUSE (the animal) MOVEMENT
    if not topo.collidepoint(MOUSE.position):
        topo.point(MOUSE)
        topo.forward(4)

    if gatto.collide(topo):
        # print('preso')
        quit()

    #update screen and events queue
    update()
