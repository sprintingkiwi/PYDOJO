from pydojo import *


def terminate():
    subprocess.Popen(["python", "/home/pi/PYGB_OS/pygbOS.py"], cwd="/home/pi/")
    pygame.quit()
    quit()


# create game display
width = 800
height = 480
screen(width, height)


def events():
    if key(UP) or buttondown(4, 0):
        playerR.point(0)
        playerR.forward(5)
    if key(DOWN) or buttondown(5, 0):
        playerR.point(180)
        playerR.forward(5)
    if key(Z) or buttondown(0, 0):
        playerL.point(0)
        playerL.forward(5)
    if key(X) or buttondown(1, 0):
        playerL.point(180)
        playerL.forward(5)
    if key(ESCAPE):
        terminate()
    if keydown(A):
        music.volumeup(10)
        print('music volume up')
        print music.volume
        print music.get_volume()
    if keydown(S):
        music.volumedown(10)
        print('music volume down')
        print music.volume
        print music.get_volume()


title = Text("Pong", name="MV Boli", fontsize=96, color=[0, 255, 0])
title.goto(400, 50)

timetext = Text("")
timetext.goto(400, 150)

instructions = Text("press START to play again or press ESCAPE to quit the game")
instructions.goto(width / 2, height / 2)

background("example_asset/backgrounds/sea.png")

edge = Actor("example_asset/backgrounds/edge.png")
edge.goto(width / 2, height / 2)

playerL = Actor("example_asset/characters/fish2.png")
playerL.goto(50, 50)

playerR = Actor("example_asset/characters/fish1.png")
playerR.flip("horizontal")
playerR.goto(width - 50, height - 50)

players = [playerL, playerR]
for player in players:
    player.scale(0.7)
    player.rotation = False

ball = Actor("example_asset/characters/seastar1.png")
ball.scale(0.4)

music = Sound("example_asset/sounds/littlesong.wav")
# music.setvolume(50)
# music.set_volume(0.5)
music.play(-1)

while True:

    title.write('Pong')

    instructions.hide()

    ball.goto(width / 2, height / 2)

    roll = random.randint(0, 1)
    if roll == 1:
        ball.point(random.randint(45, 135))
    elif roll == 0:
        ball.point(random.randint(-135, -45))

    speed = 2
    starttime = ticks()
    counttime = ticks()
    gameover = False

    while not gameover:

        # controls
        events()

        # ball movement
        ball.forward(speed)
        ball.roll(1)

        # time management
        actualtime = ticks() - starttime
        timetext.write(str(int(actualtime)))
        deltatime = ticks() - counttime
        if deltatime > 3000:
            speed += 1
            counttime = ticks()

        # collisions
        if ball.collide(playerL):
            ball.point(random.randint(45, 135))
        elif ball.collide(playerR):
            ball.point(random.randint(-135, -45))
        # if ball.mcollide(edge):
        #     ball.point(random.randint(-180, 180))
        if ball.y > height or ball.y < 0:
            ball.direction -= random.randint(45, 135)

        # game over
        if ball.x < -ball.rect.width or ball.x > width + ball.rect.width:
            gameover = True

        # update screen and events queue
        update()

        # wait
        wait(10)

    # transform_image end-menu images
    title.write("GAME OVER")
    instructions.show()

    endmenu = True
    while endmenu:

        if keydown(ESCAPE):
            terminate()
        if keydown(RETURN):
            endmenu = False

        # update screen and events queue
        update()
