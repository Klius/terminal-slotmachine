from .symbols import Symbol
import random


class Reels:
    lines: list = list()
    symbols: list = list()

    def __init__(self, symbols: list):
        prize_id = 0
        for symbol in symbols:
            self.symbols.append(Symbol(symbol, prize_id))
            prize_id += 1
        for i in range(3):
            self.lines.append(self.generate_line())

    def generate_line(self) -> list:
        random.seed()
        line: list = list()
        for i in range(3):
            line.append(self.symbols[random.randint(0, len(self.symbols)-1)])
        return line

    def update(self,start:int = 0):
        """Updates the reels with fresh symbols

        Args:
            start (int, optional): The starting reel to update. Defaults to 0.
        """
        if start > len(self.lines):
            return
        for idx,line in enumerate(self.lines):
            if start > idx:
                continue
            line.pop()
        new_line = self.generate_line()
        for idx,symbol in enumerate(new_line):
            if start > idx:
                continue
            self.lines[idx].insert(0, symbol)

    def draw(self):
        scan_lines = list()
        for i in range(len(self.lines)):
            scan_lines.append(f"{self.lines[0][i]} | {self.lines[1][i]} | {self.lines[2][i]}")
        return scan_lines
