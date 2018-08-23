from pydojo.main import *

screen(800,600)

testo = Text(fontsize=20)
testo.goto(210, 20)

sulfrum = Actor()
sulfrum.scale(0.5)
sulfrum.setpencolor(GREEN)
sulfrum.setpensize(0)
sulfrum.gorand()
sulfrum.pendown()

angolo = 5
dritto = 1

r = 0
g = 0
b = 0


while True:

    fill([r,g,b])
    testo.write("(keys:ASDXCIOP) Angle: "+str(angolo)+" forward: "+str(dritto) )

    sulfrum.forward(dritto)
    sulfrum.left(angolo)

    if keydown(A):
        sulfrum.gorand()

    if keydown(S):
        angolo+=1

    if keydown(D):
        dritto+=1

    if keydown(X):
        angolo-=1

    if keydown(C):
        dritto-=1

    if keydown(I):
        r+=20
        if r>255:
            r=0

    if keydown(O):
        g+=20
        if g>255:
            g=0

    if keydown(P):
        b+=20
        if b>255:
            b=0

    update()
