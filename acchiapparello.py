from actor import *

#creo la finestra di gioco
schermo = Screen(800, 600)

pico = Actor("library/pyco1.png")
pico.scale(0.2)

presi = 0

punti = Text(presi, color=red)
punti.goto(100, 100)

conta = 0

while True:

    conta = conta + 1

    if conta > 60:
        pico.gorand()
        conta = 0

    if pico.click():
        presi = presi + 1
        punti.write(presi)

    schermo.fill(black)
    pico.draw(schermo)
    punti.draw(schermo)

    #aggiorno lo schermo
    UPDATE()

    #attendo
    time.sleep(0.01)
