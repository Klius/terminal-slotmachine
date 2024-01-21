from .settings import SETTINGS
from .reels import Reels

class terminal_slot:
    CREDITS: int

    def __init__(self):
        CREDITS = SETTINGS.initial_credits
        self.slots = Reels(SETTINGS.symbols)

    def draw(self):
        reel_lines = self.slots.draw()
        for l in reel_lines:
            print(l)

    def update(self,current_reel:int=0):
        self.slots.update(current_reel)
