from pydojo import *
from pyfirmata import *

# inizializzo
pygame.init()
width = 800
height = 600
SCREEN(width, height)

gobo = Actor('example_library/gobo.png')
gobo.goto(width/2, height/2)

os.system('sudo rfcomm bind /dev/rfcomm0  00:15:83:35:86:A2 1')
uno = Arduino('/dev/rfcomm0')
#uno = Arduino('COM6')

rightPwm = uno.get_pin('d:5:p')
leftPwm = uno.get_pin('d:10:p')
RF = uno.get_pin('d:7:o')
RB = uno.get_pin('d:6:o')
LF = uno.get_pin('d:9:o')
LB = uno.get_pin('d:8:o')
clacson = uno.get_pin('d:3:p')

RF.write(True)
RB.write(False)
LF.write(True)
LB.write(False)

direction = 'forward'

def complete_shutdown():
    RF.write(False)
    RB.write(False)
    LF.write(False)
    LB.write(False)
    rightPwm.write(0)
    leftPwm.write(0)


def power_right_motor(value=1):
    if direction == 'forward':
            RF.write(True)
            RB.write(False)
    elif direction == 'back':
            RF.write(False)
            RB.write(True)
    rightPwm.write(value)


def power_left_motor(value=1):
    if direction == 'forward':
        LF.write(True)
        LB.write(False)
    elif direction == 'back':
        LF.write(False)
        LB.write(True)
    leftPwm.write(value)


def shutdown_right_motor():
    rightPwm.write(0)
    RF.write(False)
    RB.write(False)


def shutdown_left_motor():
    leftPwm.write(0)
    LF.write(False)
    LB.write(False)


def honk(value=1):
    clacson.write(value)


high_level_control = False
counter = 0

while True:

    # KEYBOARD CONTROL
    if keydown(ESCAPE) or buttondown(6):
        complete_shutdown()
        terminate()

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

    # GAMEPAD CONTROL
    horizontal = axis('left', 'horizontal')
    left_trigger = trigger('left')
    right_trigger = trigger('right')

    # reverse gear
    if buttondown(0):
        direction = 'back'
    else:
        direction = 'forward'

    # low-level motor control
    if buttondown(4):
        power_left_motor()
    if buttondown(5):
        power_right_motor()
    if not buttondown(4):
        shutdown_left_motor()
    if not buttondown(5):
        shutdown_right_motor()
    #if buttondown(1):
        #if  left_trigger > 0.2:
            #power_left_motor(left_trigger)
            #print left_trigger
        #if  right_trigger > 0.2:
            #power_right_motor(right_trigger)
            #print right_trigger

    # button B pressed
    if buttondown(1):
        high_level_control = True
        counter += 1

    # high-level motor control
    if high_level_control and (counter % 10 == 0):
        if  right_trigger > 0.2:
            right_power = right_trigger
            left_power = right_trigger
            if horizontal > 0.2:
                right_power *= (1 - abs(horizontal))
            elif horizontal < 0.2:
                left_power *= (1 - abs(horizontal))

            if right_power > 1:
                right_power = 1
            elif right_power < 0.1:
                right_power = 0
            if left_power > 1:
                left_power = 1
            elif left_power < 0.1:
                left_power = 0

            power_left_motor(left_power)
            power_right_motor((right_power) * 0.8)
            print(left_power, right_power)

    #clacson
    if buttondown(2):
        honk(1)
    else:
        honk(0)

    gobo.transform_rotate_image()
    sleep(0.01)
    UPDATE()
