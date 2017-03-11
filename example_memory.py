from pydojo import *

#create game display
screen(800, 600)

bug = Actor('example_library/bug1.png')
bug.scale(200, 200)
bug.goto(100, 100)

while True:

    bug.draw()

    #update screen and events queue
    update()

#wait
sleep(1)
