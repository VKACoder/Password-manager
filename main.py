from cryptography.fernet import Fernet
import pickle
import mysql.connector
import time

tries = 3
entry = False
while(tries>0):
    try:
        master_password = input("Enter Master password: ")
        print()
        con = mysql.connector.connect(host = 'localhost', user = 'root', passwd = master_password)
        entry = True
        break
    except:
        tries-=1
        print("Wrong password! You've",tries,"more tries\n")
        if tries == 0:
            print("\nUnauthorized entry\n")
            print("Access denied!")

'''def generate_key():
    Master_key = Fernet.generate_key()
    with open("Secret.dat",'wb') as file:
        pickle.dump(Master_key,file)
generate_key()'''

def retrieve_key():
    global key
    with open("Secret.dat",'rb') as file:
        key = pickle.load(file)

key = ''
retrieve_key()
k = Fernet(key)

def view():
    concursor.execute("SELECT * FROM credentials")
    print("[ USERNAME , PASSWORD ]")
    rec = []
    for record in concursor:
        rec = list(record)
        password = record[1]
        rec[1] = k.decrypt(password.encode()).decode()
        print(rec)
    print()

def add():
    username = input("Enter username: ")
    password = input("Enter password: ")
    encrypt = k.encrypt(password.encode()).decode()
    concursor.execute("INSERT INTO credentials VALUES(%s,%s)",(username,encrypt))
    con.commit()
    print("Succesfully added\n")

def update():
    concursor.execute("SELECT * FROM credentials")
    print("Existing data:")
    print("[ USERNAME , PASSWORD ]")
    rec = []
    for record in concursor:
        rec = list(record)
        password = record[1]
        rec[1] = k.decrypt(password.encode()).decode()
        print(rec)
    else:
        print()

    username = input("Enter username: ")
    concursor.execute("SELECT * FROM credentials WHERE username=%s",(username,))
    flag = False
    while True:
        for rec in concursor:
            flag = True
        break

    if(flag==True):
        new_username = input("Enter new username: ")
        new_password = input("Enter new password: ")
        confirm = input("Please enter 'yes' to confirm the updation: ")
        if confirm.lower() == 'yes':
            encrypt = k.encrypt(new_password.encode()).decode()
            concursor.execute("UPDATE credentials SET username = %s WHERE username = %s",(new_username,username))
            concursor.execute("UPDATE credentials SET password = %s WHERE username = %s",(encrypt,new_username))
            con.commit()
            print("Updation successful\n")
        else:
            print("Updation unsuccessful\n")
    else:
        print("No such username found. Updation unsuccessful")

def delete():
    username = input("\nEnter username: ")

    confirm = input("Please enter 'yes' to confirm the deletion: ")
    try:
        if confirm.lower() == 'yes':
            concursor.execute("DELETE FROM credentials where username=%s",(username,))
            con.commit()
            print("Deletion successful\n")
        else:
            print("Deletion unsuccessful\n")
    except:
        print("No such username found, deletion unsuccessful\n")

concursor = con.cursor()

try:
    concursor.execute("CREATE DATABASE PASSWORDS")
    concursor.execute('USE PASSWORDS')
    concursor.execute("CREATE TABLE credentials(username varchar(200),password varchar(200))")
except:
    concursor.execute('USE PASSWORDS')

while(entry):
    opt = input('Enter\n"view" to list all usernames and passwords,\n"add" to append a new data\n"update" to alter a existing data\n"del" to delete a data\n"q" to quit the portal\nOption: ')
    print()

    if opt.lower() == 'view':
        view()

    elif opt.lower() == 'add':
        add()

    elif opt.lower() == 'update':
        update()

    elif opt.lower() == 'del':
        delete()

    elif opt.lower() == 'q':
        print('quitting')
        con.close()
        break
    else:
        print("Enter a valid option!")
        print()
