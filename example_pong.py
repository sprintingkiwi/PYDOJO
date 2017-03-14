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


while True:

    title = Text("Pong", name="MV Boli", fontsize=96, color=[0, 255, 0])
    title.goto(400, 50)

    timetext = Text("")
    timetext.goto(400, 150)

    edge = Actor("example_library/edge.png")
    edge.goto(width / 2, height / 2)

    bg = Actor("example_library/sea.png")
    bg.goto(width / 2, height / 2)

    playerL = Actor("example_library/fish2.png")
    playerL.point(90)
    playerL.goto(50, 50)

    playerR = Actor("example_library/fish1.png")
    playerR.point(-90)
    playerR.flip("horizontal")
    playerR.goto(width - 50, height - 50)

    players = [playerL, playerR]
    for player in players:
        player.scale(0.2)
        player.rotate = False

    ball = Actor("example_library/seastar1.png")
    ball.scale(0.1)
    ball.goto(width / 2, height / 2)
    roll = random.randint(0, 1)
    if roll == 1:
        ball.point(random.randint(45, 135))
    elif roll == 0:
        ball.point(random.randint(-135, -45))

    speed = 2
    starttime = time()
    counttime = time()

    gameover = False

    while not gameover:

        # draw images
        bg.draw()
        edge.draw()
        title.draw()
        timetext.draw()
        ball.draw()
        playerR.draw()
        playerL.draw()

        # controls
        events()

        # ball movement
        ball.forward(speed)
        ball.heading += 1

        # time management
        actualtime = time() - starttime
        timetext.write(str(int(actualtime)))
        deltatime = time() - counttime
        if deltatime > 3:
            speed += 1
            counttime = time()

        # collisions
        if ball.collide(playerL):
            ball.point(random.randint(45, 135))
        elif ball.collide(playerR):
            ball.point(random.randint(-135, -45))
        # if ball.mcollide(edge):
        #     ball.point(random.randint(-180, 180))
        if ball.y > height or ball.y < 0:
            ball.direction -= 90

        # game over
        if ball.x < -ball.rect.width or ball.x > width + ball.rect.width:
            gameover = True

        # update screen and events queue
        update()

        # wait
        wait(10)

    # draw end-menu images
    title.write("GAME OVER")
    instructions = Text("press START to play again or press ESCAPE to quit the game")
    instructions.goto(width / 2, height / 2)
    bg.draw()
    title.draw()
    timetext.draw()
    instructions.draw()

    endmenu = True
    while endmenu:

        if keydown(ESCAPE):
            terminate()
        if keydown(RETURN):
            endmenu = False

        # update screen and events queue
        update()

        # wait
        wait(10)
