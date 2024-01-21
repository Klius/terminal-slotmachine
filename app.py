import time
import os, sys,tty,termios, fcntl
from slots import terminal_slot
key = ""

#States
XOUT:bool = False
START_SPIN = False
STOP_REEL = 0
CHECKOUT = False

slots: terminal_slot
# TODO implement States:
# start_spin,stop_reel_1,stop_reel_2,stop_reel_3,no_credits.

# TODO integrate with curses, read input and all that








def main():
    global slots
    global XOUT
    global key
    slots = terminal_slot()
    while not XOUT:
        key = input_read()
        update()
        draw()
        time.sleep(0.03)


def input_read():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    c = None

    try:
        c = sys.stdin.read(1)
    except IOError: pass

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    return c




def update():
    global key
    global XOUT
    global START_SPIN
    global STOP_REEL
    global slots
    
    if CHECKOUT:
        gameover = True
        if key == 'x':
            XOUT = True
            return
        elif key == curses.KEY:
            restart()
    if not START_SPIN:
       if key == " ":
        START_SPIN = True
    else:
        if key == " ":
            STOP_REEL +=1
        slots.update(STOP_REEL)

def clean():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')


def draw():
    # Clear previous frame and draw next
    clean()
    slots.draw()

try:
    main()
except (KeyboardInterrupt, SystemExit):
    os.system('stty sane')
    print('stopping.')