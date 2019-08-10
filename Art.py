import os
import time


clear = lambda: os.system('cls')


def login_art():
    print('''
 __          __  _                          _ _ _ 
 \ \        / / | |                        | | | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___| | | |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | | |
    \  /\  /  __/ | (_| (_) | | | | | |  __/_|_|_|
     \/  \/ \___|_|\___\___/|_| |_| |_|\___(_|_|_)
     ''')

def ext(x,y):
    for i in range (4):
        b = x + y * i
        print (b, end="\r")
        time.sleep(0.4)