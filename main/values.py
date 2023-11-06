from enum import Enum

class Range(Enum):
    MIN_ADD_GEN_ARGS = 2
    MAX_ADD_GEN_ARGS = 3

    MIN_ADD_INPUT = 3
    MAX_ADD_INPUT = 4

class Commands(Enum):
    ADD_GEN = '-a'
    ADD_INPUT = '-i'
    DELETE = '-d'
    UPDATE_APP_NAME = '-uapp'
    UPDATE_USERNAME = '-uusr'
    UPDATE_EMAIL = '-uemail'
    UPDATE_PASSWORD = '-upwd'
    LIST_ACCOUNTS = '-l'
    QUERY_ACCOUNT = '-q'
    HELP = 'help'
    QUIT_PROGRAM = 'quit'

