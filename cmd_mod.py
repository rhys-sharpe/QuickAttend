from enum import Enum

class Cmd(Enum):
    QUIT = 0
    ADD_RECORD = 1
    SET_DATE = 2
    SAVE_RECORD = 3
    DISPLAY_RECORD = 4
    HELP = 5