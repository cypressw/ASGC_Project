from __future__ import print_function
import time
from dual_mc33926_rpi import motors, MAX_SPEED
import curses

# This file is modified from example.py (found in dual-mc33926-motor-driver-rpi)
# and code found from www.raspberrypi.org/forums/viewtopic.php?t=225668


# Get the curses window, turn off echoing of keyboard to screen
# turn on instant (no waiting) key response, and use special values
# for cursor keys
screen = curses.initscr()
curses.noecho()
curses.halfdelay(1)     # delay for 0.1s before refreshing char (go easier on processor)    
screen.keypad(True)

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]  


# motor1 = left motor      direction = reverse
# motor2 = right motor     direction = forward
m1_dir = -1
m2_dir = 1



# both motors forward
def forward(pwr=0.6):
    # motor1 negative, motor2 positive
    speed = int (pwr * MAX_SPEED) 
    motors.setSpeeds(speed * m1_dir, speed * m2_dir)

# both motors backward
def backward(pwr=0.6):
    # motor1 positve, motor2 negative
    speed = int (pwr * MAX_SPEED)    
    motors.setSpeeds(-speed * m1_dir, -speed * m2_dir)

# left motor forward, right motor backward
def turn_right(pwr=0.6):
    # motor1 negative, motor2 negative
    speed = int (pwr * MAX_SPEED)  
    motors.setSpeeds(speed * m1_dir, -speed * m2_dir)


# right motor forward, left motor backward
def turn_left(pwr=0.6):
    # motor1 positive, motor2 positive 
    speed = int (pwr * MAX_SPEED) 
    motors.setSpeeds(-speed * m1_dir, speed * m2_dir)

# stop motors
def stop():
    motors.setSpeeds(0,0)

    
# potential actions
actions = {
    curses.KEY_UP:    forward,
    curses.KEY_DOWN:  backward,
    curses.KEY_LEFT:  turn_left,
    curses.KEY_RIGHT: turn_right,
    curses.ERR:       stop
}


try:
    # Initialize motors
    motors.enable()
    motors.setSpeeds(0, 0)

    # Loop until user enters q
    while True:
        # get key 
        char = screen.getch()

        # quit if q
        if char == ord('q'):
            break
        
        # call appropriate robot function
        else:
            action = actions.get(char)
            action()
            


finally:
    # Stop the motors, even if there is an exception
    # or the user presses Ctrl+C to kill the process.
    motors.setSpeeds(0, 0)
    motors.disable()

    # Close down curses properly and turn echo back on
    screen.keypad(0)
    curses.echo()
    curses.endwin()

    # Indicate clean exit
    print ("Program exited cleanly")


