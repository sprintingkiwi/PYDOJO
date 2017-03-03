from pydojo import *

#create game display
SCREEN(800, 600)

#CREATE SHARK ACTOR
shark = Actor('example_library/shark1.png')
shark.scale(0.2)
shark.goto(400, 300)

#CREATE FISH
fish = Actor('example_library/fish1.png')
fish.scale(0.2)
fish.goto(700, 100)
fish.point(30)

#CREATE BACKGROUND
sfondo = Actor('example_library/sea.png')
sfondo.scale(800, 600)
sfondo.goto(400, 300)
#sfondo.point(90)


#MAIN LOOP
while True:

    #SHARK MOVEMENT
    if keydown(RIGHT):
        shark.point(90)
        shark.forward(3)
    if keydown(LEFT):
        shark.point(-90)
        shark.forward(3)
    if keydown(UP):
        shark.point(0)
        shark.forward(3)
    if keydown(DOWN):
        shark.point(180)
        shark.forward(3)

    #FISH MOVEMENT
    if fish.x > 800:
        fish.point(fish.direction +180)
    elif fish.x < 0:
        fish.point(fish.direction +180)
    elif fish.y > 600:
        fish.point(180 - fish.direction)
    elif fish.y < 0:
        fish.point(180 - fish.direction)
    fish.forward(5)

    #DRAW IMAGES
    sfondo.draw()
    shark.draw()
    fish.draw()

    #update screen and events queue
    UPDATE()

    #wait
    sleep(0.01)
