from msvcrt import getwch, kbhit


def read_input() -> str:
    """Returns input read by win32api

    Returns:
        str: Char pressed on keyboard
    """
    char = ""
    if kbhit():
        char = getwch()
    return char
