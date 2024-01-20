from symbols import Symbol
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

    def update(self):
        self.lines.pop()
        new_line = self.generate_line()
        self.lines.insert(0, new_line)

    def draw(self):
        for l in self.lines:
            print(f"{l[0]} | {l[1]} | {l[2]}")
