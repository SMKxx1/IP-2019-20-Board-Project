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
import user_creation
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


class Accounts:
    def __init__(self, name):

        command = f"""
CREATE TABLE IF NOT EXISTS {name} (
id INT PRIMARY KEY AUTO_INCREMENT,
Debit_date varchar(100) DEFAULT '',
Debit_account_name varchar(100) DEFAULT '',
Debit_account_amount INT DEFAULT 0,
Credit_date varchar(100) DEFAULT '',
Credit_account_name varchar(100) DEFAULT '',
Credit_account_amount INT DEFAULT 0);"""

        c.execute(command)
        c.execute(f"""
    CREATE TABLE IF NOT EXISTS {name} (
    Debit_date TEXT DEFAULT '',
    Debit_account_name TEXT DEFAULT '',
    Debit_account_amount INTEGER DEFAULT '',
    Credit_date TEXT DEFAULT '',
    Credit_account_name TEXT DEFAULT '',
    Credit_account_amount INTEGER DEFAULT '');""")


def acc(entry, userid):
    c = mydb.cursor()
    conn = sq.connect("database.db")
    c = conn.cursor()

    debit_entry = {}
    credit_entry = {}
    currentDT = datetime.datetime.now()
    try:
        entry = entry.split(' to ')
        debit, credit = entry[0].split(', '), entry[1].split(', ')

        for i in debit:
            i = i.split(" ")
            account, amount = i[0], i[1]
            debit_entry[account] = amount
            account = account + userid
            account = Accounts(account)

        for i in credit:
            i = i.split(" ")
            account, amount = i[0], i[1]
            credit_entry[account] = amount
            account = account + userid
            account = Accounts(account)

        for ckey in credit_entry:
            for dkey in debit_entry:
                command = f"""insert into {dkey + userid} (Debit_date, Debit_account_name, Debit_account_amount, Credit_date, Credit_account_name, Credit_account_amount) values('{str(currentDT.strftime("%Y/%m/%d"))}', '{str('To ' + ckey)}', '{debit_entry[dkey]}', NULL, NULL, NULL);"""
                c.execute(command)
                
        for dkey in debit_entry:
            for ckey in credit_entry:
                command = f"""insert into {ckey + userid} (Debit_date, Debit_account_name, Debit_account_amount, Credit_date, Credit_account_name, Credit_account_amount) values(NULL, NULL, NULL, '{str(currentDT.strftime("%Y/%m/%d"))}', '{str('By ' + dkey)}', '{debit_entry[dkey]}');"""
                c.execute(command)
    except IndexError:
        print("Error in entry.")
    conn.commit()
    conn.close()

def balance_check(userid):
    for i in lst:
        a = c.fetchall()
        debit_count = credit_count = 0
        for j in a:
            else:
        balance = debit_count - credit_count
        nature = ''
        if balance > 0:
            nature = 'Debit'
        elif balance < 0:
            balance = balance*-1
            nature = 'Credit'
    input()
    clear()
    journal(userid)


def entries(userid):
    try:
        clear()
        print("Press 'cltr + c' to exit")
        print("Type your entires below")
        while True:
            entry = input("> ")
            entry = entry.lower()
            acc(entry, userid)
    except KeyboardInterrupt:
        clear()
        journal(userid)


def journal(userid):
    print("Press 'ctrl + c' to exit")
    print("Enter 1 to add journal entries")
    print("Entre 2 to check balances in accounts")
    choice = input("> ")
    if choice == '1':
        entries(userid)
    elif choice == '2':
        balance_check(userid)
