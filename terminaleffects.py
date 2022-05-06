import os

class tcolors:
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    clear = '\033[0m'
    underline = '\033[4m'
    bold = '\033[1m'

class clearTerminal:
    '''
    Clears the terminal from text when .clear is used
    '''
    def checkOS():
        if os.name == "posix":
            return lambda: os.system('nt')
        else:
            return lambda: os.system('cls')

    CLEAR = checkOS()
    

