from pydojo.main import *

screen(800,600)

tempo = ticks()

#arma
nemico = Actor("example_asset/characters/KeyMoon.png")
nemico.scale(2)
nemico.goto(0, 50)
nemico.roll(-90)
speed = 5

#proiettili
proiettili = []
proiettile = Actor()
proiettile.hide()
proiettile.scale(0.5)
intervallo = 1000 # un secondo
#contatore = 0

#personaggio
pg = Actor("example_asset/characters/LightStar.png")
pg.goto(100, 550)

while True:

    # Movimenti pg
    if key(LEFT):
        pg.setdirection(-90)
        pg.forward(4)

    if key(RIGHT):
        pg.setdirection(90)
        pg.forward(4)

    # Movimenti nemico
    nemico.forward(speed)
    if nemico.getx()>= 800:
        nemico.left(180)
        nemico.roll(90)
    if nemico.getx()<=0:
        nemico.right(180)
        nemico.roll(-90)

    # Spawn proiettili
    if ticks() - tempo > intervallo:
    #if contatore < 5 and ticks() - tempo > intervallo:
        p = clone(proiettile)
        #contatore = contatore + 1
        p.goto(nemico)
        p.right(90)
        p.show()
        proiettili.append(p)
        tempo = ticks()

    # Movimento proiettili
    for p in proiettili:
        p.forward(2)

    # Collisioni
    for p in proiettili:
        if p.collide(pg):
            p.hide()
            proiettili.remove(p)
            p.kill()

    update()
