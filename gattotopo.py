from actor import *

#creo la finestra di gioco
schermo = Screen(800, 600)

topo = Actor("risorse/mouse.png")
topo.scale(0.1)
topo.goto(400, 300)

gatto = Actor("risorse/cat.png")
gatto.scale(0.1)
gatto.goto(200, 100)

sfondo = Actor("risorse/carpet.png")
sfondo.scale(800, 600)
sfondo.goto(400, 300)


gameover = False
while not gameover:

    if topo.click():
        print("topo")

    if gatto.rclick():
        print("gatto")

    topo.point(mouse)
    gatto.point(topo)

    topo.forward(5)
    gatto.forward(2)

    sfondo.draw(schermo)
    topo.draw(schermo)
    gatto.draw(schermo)

    #aggiorno lo schermo
    UPDATE()

    #attendo
    time.sleep(0.01)
