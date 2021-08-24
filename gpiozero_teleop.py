import curses
from gpiozero import Robot

robot = Robot(left=(12, 24, 22), right=(13, 25, 23))

actions = {
    curses.KEY_UP:    robot.forward,
    curses.KEY_DOWN:  robot.backward,
    curses.KEY_LEFT:  robot.left,
    curses.KEY_RIGHT: robot.right,
    curses.ERR:       robot.stop,
}


screen = curses.initscr()
curses.noecho()
curses.halfdelay(1)       
screen.keypad(True)

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
            action = actions.get(char)
            action()


finally:
    # Stop the motors, even if there is an exception
    # or the user presses Ctrl+C to kill the process.
    robot.stop()

    # Close down curses properly and turn echo back on
    screen.keypad(0)
    curses.echo()
    curses.endwin()

    # Indicate clean exit
    print ("Program exited cleanly")
