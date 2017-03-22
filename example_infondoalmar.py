from pydojo import *

#create game display
screen(800, 600)

background('example_library/sea.png')

#CREATE SHARK ACTOR
shark = Actor('example_library/shark1.png')
shark.scale(0.2)
shark.rotation = 'flip'

#CREATE FISH
fish = Actor('example_library/fish1.png')
fish.scale(0.2)
fish.point(30)


#MAIN LOOP
while True:

    print(shark.direction)

    #SHARK MOVEMENT
    if key(RIGHT):
        shark.point(90)
        shark.forward(3)
    if key(LEFT):
        shark.point(-90)
        shark.forward(3)
    if key(UP):
        shark.point(0)
        shark.forward(3)
    if key(DOWN):
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

    #update screen and events queue
    update()
