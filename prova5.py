from actor import *

#create game display
SCREEN(1280, 720)

dyno = Actor("library/dinosaur1.png")
dyno.scale(0.2)
dyno.goto(500, 300)

star = Actor("library/seastar1.png")
star.load("library/seastar2.png", 2)
star.scale(100, 200)
star.goto(600, 500)

a = Text("ciao", color=green)
a.setfontsize(48)
a.setbold(True)
a.setitalic(True)
a.goto(100, 100)

#dyno.rotate = False

r = Rect(size=[32, 32], color=blue)
r.goto(400, 250)

c = Circle(radius=64, line_width=20)
c.goto(500, 400)

hey = Sound("library/hey.wav")

while True:

    if dyno.click():
        print("funziona")
        hey.play()
        print(dyno.getcostume())

    if keydown(RIGHT):
        print("destra")
        star.point(90)
        star.forward(5)

    if keydown(LEFT):
        print("sinistra")
        star.point(-90)
        star.forward(5)

    #dyno.direction = 90
    #dyno.left(1)
    r.right(10)
    c.left(5)
    dyno.goto(mouse)
    r.point("mouse")
    dyno.forward(10)
    r.forward(2)
    c.forward(20)
    #dyno.gorand()

    if dyno.collide(star):
        print(dyno.collide(star))
        star.setcostume(2)
        #star.scale(100, 200)
        hey.play()

    if star.costume == 2 and not star.collide(dyno):
        star.setcostume(1)
        #star.scale(100, 200)

    fill(white)
    a.draw()
    star.draw()
    dyno.draw()
    r.draw()
    c.draw()

    #update screen and events queue
    UPDATE()

    #wait
    sleep(0.01)
