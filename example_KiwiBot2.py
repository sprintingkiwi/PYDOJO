from pydojo import *

# creo lo schermo
width = 800
height = 600
SCREEN(width, height)

# creo un attore a scopo di debug
gobo = Actor('example_library/gobo.png')
gobo.goto(width/2, height/2)

# trovo la porta
#os.system('sudo rfcomm bind /dev/rfcomm0  00:15:83:35:86:A2 1')
#uno = Arduino('/dev/rfcomm0')
uno = Arduino('COM15')

rightPwm = uno.get_pin('d:5:p')
leftPwm = uno.get_pin('d:6:p')

direction = "forward"

def shutdown():
    rightPwm.write(0)
    leftPwm.write(0)

def power_right_motor(value=1):
    rightPwm.write(value)
    
def power_left_motor(value=1):
    leftPwm.write(value)
    
def shutdown_right_motor():
    rightPwm.write(0)

def shutdown_left_motor():
    leftPwm.write(0)

while True:

    # KEYBOARD CONTROL
    if keydown(ESCAPE):
        shutdown()
        quit()

    if keydown(RIGHT):
        power_right_motor()
        
    if keyup(RIGHT):
        shutdown_right_motor()

    if keydown(LEFT):
        power_left_motor()

    if keyup(LEFT):
        shutdown_left_motor()

    if keydown(UP):
        direction = 'forward'
    if keydown(DOWN):
        direction = 'back'


    # # GAMEPAD CONTROL
    # horizontal = axis('left', 'horizontal')
    #
    # if horizontal > 0.2:
    #     #rightPwm.write(0.9)
    #     pass
    # if horizontal < -0.2:
    #     #leftPwm.write(0.9)
    #     pass
    #
    # if buttondown(0):
    #     if direction == 'forward':
    #         direction = 'back'
    #     elif direction == 'back':
    #         direction = 'forward'
    # if buttondown(4):
    #     power_left_motor()
    # if buttondown(5):
    #     power_right_motor()
    # if not buttondown(4):
    #     shutdown_left_motor()
    # if not buttondown(5):
    #     shutdown_right_motor()


    gobo.draw()
    sleep(0.01)
    UPDATE()
