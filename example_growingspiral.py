from pydojo import *

screen(1280, 720)
fill(WHITE)

uga = Actor()
uga.pendown()
# uga.setpencolor(CYAN)

dimensione = 1
passi = 1

while True:
    uga.setpensize(dimensione)
    uga.forward(passi)
    uga.right(10)

    dimensione = dimensione + 1
    passi = passi + 1

    if keydown(ESCAPE):
        quit()
    if keydown(C):
        clear()
        dimensione = 1
        passi = 1
        uga.goto(CENTER)

    update()
