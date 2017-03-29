from pydojo import *

#create game display
screen(1280, 720)

pyco = Actor('example_library/pyco1.png', 'idle')
pyco.loadfolder('example_library/pyco_walk/')
print pyco.costumes
pyco.scale(0.2)
pyco.goto(100, 600)
pyco.speed = 5
# pyco.rotate = False
pyco.rotation = 'flip'
pyco.bullets = []

py = Actor('example_library/python.png')
py.scale(50, 50)
py.hide()

platforms = []

for i in range(6):
    a = Actor('example_library/platform.png', str(i))
    a.tag = 'flying platform'
    platforms.append(a)

terrain = Actor('example_library/terrain.png')
terrain.goto(CENTER.x, 700)
terrain.scale(1280, 50)

print(platforms)

for p in platforms:
    p.gorand()

pyco.jumping = False

gravity = 10

while True:

    if key(RIGHT):
        pyco.point(90)
        pyco.forward(pyco.speed)
        pyco.nextcostume(pause=7, costumes=[1, 4])
    if keyup(RIGHT):
        pyco.setcostume('idle')
    if key(LEFT):
        pyco.point(-90)
        pyco.forward(pyco.speed)
        pyco.nextcostume()
    if keydown(UP):
        if pyco.collide(terrain) or pyco.collide(platforms):
            pyco.jumping = True
            t = 0
    if keydown(SPACE):
        bullet = clone(py)
        bullet.point(pyco.direction)
        bullet.goto(pyco)
        bullet.show()
        pyco.bullets.append(bullet)
        print pyco.bullets
        # for b in pyco.bullets:
        #     print distance(pyco, b)

    for b in pyco.bullets:
        b.forward(10)
        if distance(pyco, b) > 2000:
            pyco.bullets.remove(b)

    if pyco.jumping:
        if t < 15:
            pyco.y -= (2 * gravity)
            t = t + 1

    if key(DOWN):
        pyco.point(180)
        pyco.forward(pyco.speed)


    if not pyco.collide(terrain) and not pyco.collide(platforms):
        # print('falling')
        pyco.y += gravity

    update()
