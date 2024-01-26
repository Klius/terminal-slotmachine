import time
import os
import platform
from colorama import Fore, just_fix_windows_console
from slots import terminal_slot
from pyparsing import *

if platform.system() == "Windows":
    from input.windows_input import read_input
    just_fix_windows_console()
else:
    from input.linux_input import read_input


key = ""

# States
XOUT: bool = False
START_SPIN = False
STOP_REEL = 0
CHECKOUT = False
PRIZE = 0

slots: terminal_slot


def main():
    global slots
    global XOUT
    global key
    slots = terminal_slot()
    while not XOUT:
        key = read_input()
        update()
        draw()
        time.sleep(0.04)


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


def length_ansi_string(string: str):
    ESC = Literal('\x1b')
    integer = Word(nums)
    escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer, ';')) +
                        oneOf(list(alphas)))

    def nonAnsiString(s): return Suppress(escapeSeq).transformString(s)

    unColorString = nonAnsiString(string)
    return len(unColorString)


def clean():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def end_msg_box(msg: str, padding: int = 32):
    pad = " "*(padding-length_ansi_string(msg))+"┃"
    return msg+pad


def draw():
    # Clear previous frame and draw next
    print('\033[20A\033[2K', end='')
    print(" ")
    screen_lines: list = list()
    screen_lines = slots.draw(STOP_REEL)
    screen_lines.append("┏━🞓 STATUS 🞓"+"━"*20+"┓")
    if CHECKOUT:
        screen_lines.append(end_msg_box(f"┃ {Fore.BLUE}You won!!{Fore.RESET}"))
        screen_lines.append(end_msg_box(
            f"┃ {Fore.YELLOW}🪙 {Fore.GREEN}{slots.CREDITS} + {PRIZE} {Fore.YELLOW}🪙{Fore.RESET}"))
    else:
        if START_SPIN == False:
            screen_lines.append(end_msg_box(
                f"┃ Press {Fore.BLUE}SPACE{Fore.RESET} to spin, {Fore.RED}X{Fore.RESET} to quit"))
        if START_SPIN:
            screen_lines.append(end_msg_box(
                f"┃ Press {Fore.BLUE}SPACE{Fore.RESET} to stop Reel"))
        screen_lines.append(end_msg_box(
            f"┃ {Fore.YELLOW}🪙 {Fore.GREEN}{slots.CREDITS}{Fore.RESET}"))
    screen_lines.append("┗"+"━"*31+"┛")
    print("\n".join(screen_lines))
    # Return cursor up https://stackoverflow.com/questions/34828142/cmd-console-game-reduction-of-blinking
    print("\033[1;1H", end="")


try:
    clean()
    main()
    clean()
    print("Thanks for playing!")
except (KeyboardInterrupt, SystemExit):
    os.system('stty sane')
    clean()
