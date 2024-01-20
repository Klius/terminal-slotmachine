from settings import SETTINGS
from reels import Reels

# TODO implement States:
# start_spin,stop_reel_1,stop_reel_2,stop_reel_3,no_credits.

# TODO integrate with curses, read input and all that


class terminal_slot:
    EXIT: bool = False
    CREDITS: int

    def __init__(self):
        CREDITS = SETTINGS.initial_credits
        self.slots = Reels(SETTINGS.symbols)
        while not self.EXIT:
            self.slots.update()
            self.draw()

    def draw(self):
        print("====================================")
        self.slots.draw()


terminal_slot()
