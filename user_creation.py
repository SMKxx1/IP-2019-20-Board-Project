import pandas as pd 
import numpy as np 
import sqlite3 as sq
import datetime
import hashlib
import fileinput
import sys
import os
import time
import getpass
import Art

clear = lambda: os.system('cls')

conn = sq.connect("database.db")

c = conn.cursor()

def replace(file, searchexp, replaceexp):
    for line in fileinput.input(file, inplace=1):
        if searchexp in line:
            line = line.replace(searchexp, replaceexp)
        sys.stdout.write(line)

def encoder(password):
    password1 = hashlib.md5(password.encode())
    password = password1.hexdigest()
    return password



def new_user():
    conn = sq.connect("database.db")
    c = conn.cursor()
    clear()
    found = 0
    password = ''
    pass_again = ' '
    print("Press 'ctrl + c' to exit")
    try:
        while found == 0:
            username = input("Please enter a username: ")
            find_user = (f"select * from user where username like '{username}';")
            c.execute(find_user)
            a = c.fetchall()
            if a != []:
                clear()
                print("Username Taken, please try again")
                input()
                clear()
            else:
                found = 1
        firstname = input("Enter your firstname: ")
        surename = input("Enter your surename: ")
        while password != pass_again:
            password = getpass.getpass("Enter your password: ", stream=None)
            pass_again = getpass.getpass("Please re-enter your password: ", stream=None)
            if password != pass_again:
                print("Passwords did not match. Please try again.")
        pass_again = ' '
        password = encoder(password)
        command = f"insert into user values(NULL, '{username}', '{firstname}', '{surename}', '{password}');"
        c.execute(command)
        print("User has been created")
        time.sleep(1)
        conn.commit()
        conn.close()

    except KeyboardInterrupt:
        Art.ext("Exiting", ".")