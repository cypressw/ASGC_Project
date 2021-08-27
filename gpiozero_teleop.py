import curses
from gpiozero import LED, PhaseEnableRobot

# Specify motor enable GPIO pins, MC33926 is a PHASE/ENABLE motor driver.
en_motor1 = LED(22) # Make GPIO mode as output using LED class
en_motor2 = LED(23) # In case you wan to set GPIO mode as input, go with Button class

robot = PhaseEnableRobot(left=(24, 12), right=(25, 13)) # (Motor PWM, Motor DIR)

actions = {
    curses.KEY_UP:    robot.forward,
    curses.KEY_DOWN:  robot.backward,
    curses.KEY_LEFT:  robot.left,
    curses.KEY_RIGHT: robot.right,
}

# Initialize curses functionality
screen = curses.initscr()
curses.noecho()
curses.halfdelay(1)       
screen.keypad(True)

# Enable motors
en_motor1.on()
en_motor2.on()

try:

# Loop until user enters q
    while True:
        # get key 
        char = screen.getch()

        # quit if q
        if char == ord('q'):
            break
        
        # call appropriate robot function
        else:
            if not char in actions:
                robot.stop()
            else:
                action = actions.get(char)
                if action is not None:
                    action(.6) # to safely use a 7.4V battery on a 6V nominal motor, full duty cycle is not recommended


finally:
    # Stop the motors, even if there is an exception
    # or the user presses Ctrl+C to kill the process.
    en_motor1.off()
    en_motor2.off()
    robot.stop()

    # Close down curses properly and turn echo back on
    screen.keypad(0)
    curses.echo()
    curses.endwin()

    # Indicate clean exit
    print ("Program exited cleanly")
