class Settings:
    ascii_symbols:bool = False
    symbols: list
    def __init__(self,ascii_symbols:bool=False):
        self.ascii_symbols = ascii_symbols 
        self.symbols = ["🍒",""]  
        #cherry, bar, diglet,poliwag,jygglies,lucky7