from .settings import SETTINGS
from .reels import Reels
from colorama import Fore
import math
import os
import time


class terminal_slot:
    CREDITS: int

    def __init__(self):
        self.CREDITS = SETTINGS.initial_credits
        self.slots = Reels(SETTINGS.symbols)

    def draw(self, current_reel):
        reel_lines = self.slots.draw()
        # flash = math.floor(math.sin(time.process_time_ns()))
        flash = abs(math.sin(time.process_time_ns()))
        marquee = "SLOTS"
        if flash > 0.8:
            marquee = Fore.YELLOW + marquee + Fore.RESET
        print(f"   ┏━━🞓 {marquee} 🞓━━━┓")
        for l in reel_lines:
            print(f"   ┃ {l} ┃")
        print("   ┗━━━━━━━━━━━━━━┛")
        # Draw buttons
        print("   ┏━━━━━━━━━━━━━━┓")
        button_pressed = f"{Fore.YELLOW}🔳{Fore.RESET}   "
        button = f"{Fore.YELLOW}🔲{Fore.RESET}   "
        button_row = "   ┃ " + button_pressed * \
            current_reel + button*(3-current_reel)
        print(button_row.rstrip()+" ┃")
        print("   ┗━━━━━━━━━━━━━━┛")
        # Draw prizes:
        half = len(SETTINGS.symbols)/2
        prize_line = "┃ "
        print(f"┏{'━'*5}🞓 PRIZES 🞓{'━'*5}┓")
        for idx, symbol in enumerate(self.slots.symbols, start=1):
            prize_line += f"{symbol}-{SETTINGS.prizes[symbol.prize_id]} "
            if half == idx:
                print(f"{prize_line} ┃")
                prize_line = "┃ "

        print(f"{prize_line}┃")
        print(f"┗{'━'*20}┛")

    def update(self, current_reel: int = 0):
        self.slots.update(current_reel)

    def start(self):
        self.CREDITS -= 3

    def checkout(self):
        prize_id = -1
        prize = 0
        for idx, line in enumerate(self.slots.lines):
            if self.slots.lines[0][idx] == self.slots.lines[1][idx] \
                    and self.slots.lines[1][idx] == self.slots.lines[2][idx]:
                prize_id = self.slots.lines[0][idx].prize_id
                break
        if self.slots.lines[0][0] == self.slots.lines[1][1] \
                and self.slots.lines[1][1] == self.slots.lines[2][2]:
            prize_id = self.slots.lines[0][0].prize_id
        if self.slots.lines[0][2] == self.slots.lines[1][1] \
                and self.slots.lines[1][1] == self.slots.lines[2][0]:
            prize_id = self.slots.lines[0][2].prize_id
        if prize_id != -1:
            prize = SETTINGS.prizes[prize_id]

        return prize
