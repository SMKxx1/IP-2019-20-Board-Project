import pandas as pd 
import numpy as np 
import sqlite3 as sq
# import mysql.connector
import datetime
import hashlib
import fileinput
import sys
import os
import time
import getpass
import user_creation
import Art
import journal

# mydb = mysql.connector.connect(
#     host = "localhost",
#     port = 3310,
#     user = "root",
#     passwd = "1234"
# )

# c = mydb.cursor()

def main():

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


    class Accounts:
        
        def __init__(self, name):

            c.execute(f"""
    CREATE TABLE IF NOT EXISTS {name} (
    Debit_date TEXT DEFAULT '',
    Debit_account_name TEXT DEFAULT '',
    Debit_account_amount INTEGER DEFAULT '',
    Credit_date TEXT DEFAULT '',
    Credit_account_name TEXT DEFAULT '',
    Credit_account_amount INTEGER DEFAULT '');""")
            conn.commit()
            conn.close()



    def acc(entry):
        conn = sq.connect("database.db")
        c = conn.cursor()
        debit_entry = {}
        credit_entry = {}
        currentDT = datetime.datetime.now()

        entry = entry.split(' to ')
        debit, credit = entry[0].split(', '), entry[1].split(', ')

        for i in debit:
            i = i.split(" ")
            account, amount = i[0], i[1]
            debit_entry[account] = amount
            account = Accounts(account)

        for i in credit:
            i = i.split(" ")
            account, amount = i[0], i[1]
            credit_entry[account] = amount
            account = Accounts(account)

        for ckey in credit_entry:
            for dkey in debit_entry:
                command = f"""insert into {dkey} values( '{(str(currentDT.strftime("%Y/%m/%d")))}', '{(str('To ' + ckey))}', '{debit_entry[dkey]}', NULL, NULL, NULL);"""
                c.execute(command)
                
        for dkey in debit_entry:
            for ckey in credit_entry:
                command = f"""insert into {dkey} values(NULL, NULL, NULL, '{str(currentDT.strftime("%Y/%m/%d"))}', '{str('By ' + dkey)}', '{debit_entry[dkey]}');"""
                c.execute(command)
                

    def login():
        conn = sq.connect("database.db")
        c = conn.cursor()
        try:
            clear()
            username = input("Please enter your username: ")
            c.execute("SELECT * FROM user WHERE username = ?;", (username,))
            check = c.fetchone()
            if check == None:
                print("Username not found. Please try again.")
                input()
                login()
            else:
                password = getpass.getpass("Please enter your password: ", stream=None)
                password = encoder(password)
                # find_user = ("SELECT * FROM user WHERE username = ?;")
                check = c.fetchone()
                if check == None:
                    print("Invalid Password. Try again")
                    input()
                    login()
                else:
                    command = f"SELECT userid FROM user WHERE username = '{username}' AND password = '{password}';"
                    c.execute(command)
                    userid = str(c.fetchone())
                    userid = userid[1:-2]
                    clear()
                    journal.journal(userid)
                    # print("Press 'ctrl + c' to exit")
                    # print("Enter 1 to add journal entries")
                    # print("Entre 2 to check balances in accounts")
                    # choice = input("> ")
                    # if choice == '1':
                    #     journal.journal(a)
                    # elif choice == '2':
                    #     journal.balance_check(a)
                    conn.commit()
                    conn.close()

        except KeyboardInterrupt:
            main()
        
        conn.close()


    try:
        clear()
        print("Please choose your option below")
        print("Enter 1 to create an user")
        print("Enter 2 to login")
        print("Type 'ext' to exit")
        choice = input("> ")
        if choice == '1':
            clear()
            user_creation.new_user()
            main()
        elif choice == '2':
            clear()
            login()
        else:
            exit()
    
    except KeyboardInterrupt:
        Art.ext("Exiting", ".")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
