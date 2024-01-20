class Symbol:
    symbol :str
    prize_id:int 

    def __init__(self,symbol:str,prize_id:int):
        self.symbol = symbol
        self.prize_id = prize_id
    
    def __str__(self):
        return self.symbol
    

# x = Symbol("❄",4)
# where to get symbols https://symbl.cc/en/unicode/table/#currency-symbols
# https://symbl.cc/en/unicode/table/#miscellaneous-symbols-and-pictographs
# print(x)