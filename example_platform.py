from pydojo import *

# create game display
screen(1280, 720)

background('example_asset/backgrounds/forest2.png')

framerate(30)

# PYCO INIT
pyco = Actor('example_asset/characters/pyco1.png', 'idle')
print pyco.costume, pyco.cosnumber
pyco.loadfolder('example_asset/characters/pyco_walk')
print pyco.costume, pyco.cosnumber
pyco.goto(100, 600)
pyco.speed = 5
pyco.rotate('flip')
pyco.bullets = []
pyco.jumping = False
pyco.scale(0.9)

# BAT INIT
bat = Actor('example_asset/characters/bat1.png')
bat.load('example_asset/characters/bat2.png')
bat.rotate('flip')
bat.point(random.randint(0, 360))
bat.tag('enemy')
bat.scale(0.9)

# PY BULLET INIT
py = Actor('example_asset/characters/python.png')
py.scale(50, 50)
py.hide()
py.tag('bullet')
py.tag('test')
py.setpencolor(RED)

# PLATFORMS INIT
platforms = []
for i in range(6):
    a = Actor('example_asset/characters/platform.png', str(i))
    a.tag('support')
    a.scale(200, 50)
    platforms.append(a)
for p in platforms:
    p.gorand()
# print(platforms)

# TERRAIN INIT
terrain = Actor('example_asset/characters/terrain.png')
terrain.goto(CENTER.x, 700)
terrain.scale(1280, 50)
terrain.tag('support')
terrain.tag('prova')
terrain.untag('prova')

gravity = 10

print pyco.costumes_by_number

def pybullet_setup(bullet):
    bullet.tag('custom spawn setup behavior working')
    print bullet.tags

def pybullet_movement(bullet):
    bullet.setdirection(random.randint(int(bullet.direction - 10), int(bullet.direction + 10)))
    bullet.roll(5)
    if distance(pyco, bullet) > 2000:
        bullet.kill()

while True:

    # MOVEMENT
    if key(RIGHT):
        pyco.point(90)
        pyco.forward(pyco.speed)
        pyco.nextcostume(pause=7, costumes=[1, 4])
        # print pyco.cosnumber
    if keyup(RIGHT):
        pyco.setcostume('idle')
    if key(LEFT):
        pyco.point(-90)
        pyco.forward(pyco.speed)
        pyco.play('pyco_walk')
    if keyup(LEFT):
        pyco.setcostume('idle')

    # JUMP
    if keydown(UP):
        if pyco.collide('support'):
            pyco.jumping = True
            t = 0
    if pyco.jumping:
        if t < 15:
            pyco.y -= (2 * gravity)
            t = t + 1

    # SHOOT
    if keydown(SPACE):
        spawn(py,
              direction=pyco.direction,
              speed=10,
              position=pyco,
              setup_behavior=pybullet_setup,
              update_behavior=pybullet_movement)
        # bullet = clone(py)
        # print bullet.tags
        # bullet.rotate(False)
        # bullet.point(pyco.direction)
        # bullet.goto(pyco)
        # bullet.show()
        # # bullet.pendown()
        # print game_info.tagged_actors
        # bullet.untag('test')
        # print bullet.tags
        # print py.tags
        # pyco.bullets.append(bullet)

    if pyco.collide(bat):
        print('preso')
        pyco.hide(2)
    if keydown(P):
        pyco.show()
    if keydown(O):
        pyco.hide()

    # for b in pyco.bullets:
    #     b.forward(10)
    #     b.setdirection(random.randint(b.direction - 10, b.direction + 10))
    #     b.roll(5)
    #     if distance(pyco, b) > 2000:
    #         pyco.bullets.remove(b)

    if key(DOWN):
        pyco.point(180)
        pyco.forward(pyco.speed)

    if not pyco.collide('support'):
        # print('falling')
        pyco.y += gravity

    if pyco.y > 720:
        pyco.y = 500

    # BAT
    bat.nextcostume()
    bat.forward(10)
    bat.bounce()
    if bat.collide('bullet'):
        print('colpito')
        bat.hide(2)
        print COLLISION.point
        print COLLISION.object

    update()
