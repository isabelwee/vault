from enum import Enum

class Commands(Enum):
    HELP = 'help'
    QUIT = 'q'
    REGISTER = 'r'          # register for a new vault account
    LOGIN = 'l'
    PREVIEW = 'p'           # preview platform names of password accounts
    VIEW_ACCOUNT = 'v'      # view account (platform or platform and username provided)
    ADD_ACCOUNT = 'a'