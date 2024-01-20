from colorama import Fore


class Settings:
    ascii_symbols: bool = False
    symbols: list
    initial_credits: int

    def __init__(self, ascii_symbols: bool = False):
        self.ascii_symbols = ascii_symbols
        self.symbols = [f"{Fore.RED}🍒{Fore.RESET}",
                        f"{Fore.GREEN}🍀{Fore.RESET}",
                        "🐧",
                        f"{Fore.GREEN}🐊{Fore.RESET}",
                        f"{Fore.BLUE}🐬{Fore.RESET}",
                        f"{Fore.YELLOW}❼ {Fore.RESET}"]
        self.prizes = [8, 100, 50, 16, 25, 300]
        self.initial_credits = 300
        self.credit_symbol = "€"  # FIXME pick something better
        # 🆨
        # cherry, bar, diglet,poliwag,jygglies,lucky7


SETTINGS = Settings()
