from pydojo import *

#create game display
screen(1280, 720)

pyco = Actor('example_library/pyco1.png', 'idle')
pyco.scale(0.2)
pyco.goto(100, 600)
pyco.speed = 5
pyco.rotation = 'flip'

platforms = []

for i in range(6):
    a = Actor('example_library/platform.png', str(i))
    a.tag = 'flying platform'
    platforms.append(a)

terrain = Actor('example_library/terrain.png')
terrain.goto(CENTER.x, 700)
terrain.scale(1280, 50)

print(platforms)

while True:

    if key(RIGHT):
        pyco.point(90)
        pyco.forward(pyco.speed)
    if key(LEFT):
        pyco.point(-90)
        pyco.forward(pyco.speed)
    if key(UP):
        pyco.point(0)
        pyco.forward(pyco.speed)
    if key(DOWN):
        pyco.point(180)
        pyco.forward(pyco.speed)
    if not pyco.collide(terrain):
        pyco.y = pyco.y + 1
        print('falling')
    print(terrain.collide(pyco))

    for p in platforms:
        p.forward(1)

    update()
