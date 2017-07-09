from pydojo import *
# CREATE GAME DISPLAY
screen(800, 600)

# PYCO INIT
pyco = Actor('example_asset/characters/pyco1.png', 'idle')
pyco.loadfolder('example_asset/characters/pyco_walk')
# print pyco.costumes
pyco.goto(CENTER)
pyco.speed = 5
# pyco.roll = False
pyco.rotate('flip')
pyco.bullets = []
pyco.jumping = False
pyco.scale(0.9)
pyco.setlayer(10)

map1_ground = Actor('example_asset/backgrounds/map1/ground.png')


# MAIN LOOP
while True:
    print pyco.direction

    # if not map1_ground.x > map1_ground.width/2:
    CAMERA.follow(pyco, map1_ground)
    # print CAMERA.on_the_edge
    print CAMERA.old_x, CAMERA.old_y
    print CAMERA.hor_position, CAMERA.ver_position
    # MOVEMENT
    if key(RIGHT):
        pyco.point(90)
        pyco.forward(pyco.speed)
        pyco.play('pyco_walk')
        # print pyco.cosnumber
    if keyup(RIGHT):
        pyco.setcostume('idle')
    if key(LEFT):
        pyco.point(-90)
        pyco.forward(pyco.speed)
        pyco.play('pyco_walk')
    if keyup(LEFT):
        pyco.setcostume('idle')
    if key(UP):
        pyco.point(0)
        pyco.forward(pyco.speed)
        pyco.play('pyco_walk')
        # print pyco.cosnumber
    if keyup(UP):
        pyco.setcostume('idle')
    if key(DOWN):
        pyco.point(180)
        pyco.forward(pyco.speed)
        pyco.play('pyco_walk')
    if keyup(DOWN):
        pyco.setcostume('idle')

    # UPDATE SCREEN
    update()
