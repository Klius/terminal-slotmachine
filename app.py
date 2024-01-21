import time
import os
import sys
import tty
import termios
import fcntl
from colorama import Fore
from slots import terminal_slot
from pyparsing import *


key = ""

# States
XOUT: bool = False
START_SPIN = False
STOP_REEL = 0
CHECKOUT = False
PRIZE = 0

slots: terminal_slot
# TODO implement States:
# start_spin,stop_reel_1,stop_reel_2,stop_reel_3,no_credits.


def main():
    global slots
    global XOUT
    global key
    slots = terminal_slot()
    while not XOUT:
        key = input_read()
        update()
        draw()
        time.sleep(0.04)


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
    except IOError:
        pass

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    return c


def update():
    global key
    global XOUT
    global START_SPIN
    global STOP_REEL
    global PRIZE
    global slots
    global CHECKOUT
    if START_SPIN and STOP_REEL == 3:
        # the reels have stopped
        START_SPIN = False
        STOP_REEL = 0
        CHECKOUT = True
        PRIZE = slots.checkout()
    if CHECKOUT:
        if PRIZE <= 0:
            CHECKOUT = False
            return
        PRIZE -= 1
        slots.CREDITS += 1
    elif not START_SPIN:
        if key == 'x':
            XOUT = True
            return
        elif key == ' ':
            slots.start()
            START_SPIN = True
            STOP_REEL = 0

    else:
        if key == " ":
            STOP_REEL += 1
        slots.update(STOP_REEL)

def length_ansi_string(string:str):
    ESC = Literal('\x1b')
    integer = Word(nums)
    escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) + 
                    oneOf(list(alphas)))

    nonAnsiString = lambda s : Suppress(escapeSeq).transformString(s)

    unColorString = nonAnsiString(string)
    return len(unColorString)


def clean():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def end_msg_box(msg:str,padding:int=32):
    pad = " "*(padding-length_ansi_string(msg))+"┃"
    return msg+pad
    

def draw():
    # Clear previous frame and draw next
    print('\033[20A\033[2K', end='')
    print(" ")
    screen_lines:list = list()
    screen_lines = slots.draw(STOP_REEL)
    screen_lines.append("┏━🞓 STATUS 🞓"+"━"*20+"┓")
    if CHECKOUT:
        screen_lines.append(end_msg_box(f"┃ {Fore.BLUE}You won!!{Fore.RESET}"))
        screen_lines.append(end_msg_box(f"┃ {Fore.YELLOW}🪙 {Fore.GREEN}{slots.CREDITS} + {PRIZE} {Fore.YELLOW}🪙{Fore.RESET}"))
    else:
        if START_SPIN == False:
            screen_lines.append(end_msg_box(f"┃ Press {Fore.BLUE}SPACE{Fore.RESET} to spin, {Fore.RED}X{Fore.RESET} to quit"))
        if START_SPIN:
            screen_lines.append(end_msg_box(f"┃ Press {Fore.BLUE}SPACE{Fore.RESET} to stop Reel"))
        screen_lines.append(end_msg_box(f"┃ {Fore.YELLOW}🪙 {Fore.GREEN}{slots.CREDITS}{Fore.RESET}"))
    screen_lines.append("┗"+"━"*31+"┛")
    print("\n".join(screen_lines))
    #Return cursor up https://stackoverflow.com/questions/34828142/cmd-console-game-reduction-of-blinking
    print('\033[4B', end='')


try:
    clean()
    main()
except (KeyboardInterrupt, SystemExit):
    os.system('stty sane')
    print('stopping.')
