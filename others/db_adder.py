import sqlite3
import os

# Grabs the directory name [BETA TESTING: to prevent file not found error]
path = os.getcwd()
print(path)

# Connects to the websites database
conn = sqlite3.connect(path + '/websitesdb')
# Asigns cursor to execute database functions
cur = conn.cursor()

insert_command = '''INSERT INTO Websites (name, url, searchurl, key1_id, key2_id, 
                key3_id, type_id, hasmainlink)
	            VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

key_1_retr = "SELECT * FROM Keys1"
key_2_retr = "SELECT * FROM Keys2"
key_3_retr = "SELECT * FROM Keys3"
types_retr = "SELECT * FROM Types"

def apply_db(name, link, slink, key1, key2, key3, type, hasmainlink):
    cur.execute(insert_command, (name, link, slink, key1, key2, key3, type, hasmainlink,))
    print("Done")
    conn.commit()
    askUser()

def askUser():
    print("\n\nWelcome to db adder. Used for inserting content in the database")

    print('''\n Make sure the format of the name is good,\n
    for example: FileCR not filecr''')
    name = input("Enter site name: ")

    print('''\n If site in the link href attribute doesn't start with the site's name, make sure 
    what you enter here corresponds to it.\n
    For example: https://view-comic.com/\n
    The program mixes the main link with the retrieved if the retrieved doesn't start with main.\n
    What the program does: link + retrieved = https://view-comic.com/
    category/amory-wars-the-good-apollo-i-m-burning-star-iv/''')
    link = input("Enter main site's link: ")

    print('''\n Search url must be correct, and only + is allowed as mixing two words.\n
    For example: https://view-comic.com/search/?key=star+wars''')
    slink = input("Enter search url: ")

    key1_check = list()
    print('''\n Available key1 ids: ''')
    for key in cur.execute(key_1_retr):
        print(key[0], key[1])
        key1_check.append(int(key[0]))
    try:
        key1 = int(input("\n [1] Enter the id of the key you want to assign: "))
    except: 
        print("You didn't type an id! Start over...\n")
        askUser()

    if key1 not in key1_check:
        print("Not a valid id. If you want to add a new one, use the DB browser. Start over... \n")
        askUser()

    key2_check = list()
    print("\n Available key2 ids: ")
    for key in cur.execute(key_2_retr):
        print(key[0], key[1])
        key2_check.append(int(key[0]))
    try:
        key2 = int(input("\n [2] Enter the id of the key you want to assign: "))
    except: 
        print("You didn't type an id! Start over...\n")
        askUser()

    if key2 not in key2_check:
        print("Not a valid id. If you want to add a new one, use the DB browser. Start over... \n")
        askUser()

    key3_check = list()
    print("\n Available key3 ids: ")
    for key in cur.execute(key_3_retr):
        print(key[0], key[1])
        key3_check.append(int(key[0]))
    try:
        key3 = int(input("\n [3] Enter the id of the key you want to assign: "))
    except: 
        print("You didn't type an id! Start over...\n")
        askUser()

    if key3 not in key3_check:
        print("Not a valid id. If you want to add a new one, use the DB browser. Start over... \n")
        askUser()

    type_check = list()
    print("\n Available type ids: ")
    for type in cur.execute(types_retr):
        print(type[0], type[1])
        type_check.append(int(type[0]))
    try:
        type_usr = int(input("\n Enter the id of the type you want to assign: "))
    except:
        print("You didn't type an id! Start over...\n")
        askUser()

    if type_usr not in type_check:
        print("Not a valid id. If you want to add a new one, use the DB browser. Start over... \n")
        askUser()

    print('''\n Does the site have the main link in the retrieved attribute?
    For example, if retrieved starts with https://view-comic.com/ then you 
    insert 0, because it does have the main link. But if retrieved is 
    category/amory-wars-the-good-apollo-i-m-burning-star-iv/ then 1 so the program
    would mix it with the main link to have a valid url.
    ''')

    hasmainlink = int(input("\n Type either 0 or 1: "))
    if hasmainlink != 0 and hasmainlink != 1:
        print("You have to either type 0 or 1! Start over...")
        askUser()

    print("\n\n Preview:")
    print("Name: " + name)
    print("Link: " + link)
    print("Search link: " + slink)
    print("Key1:", key1)
    print("Key2:", key2)
    print("Key3:", key3)
    print("Type:", type_usr)
    print("Has main link:", hasmainlink)

    usr_proceed = input("Do you want to apply to database or start over? Type 0 for proceed, 1 for start over, 2 for quit: ")

    if usr_proceed == "0":
        apply_db(name, link, slink, key1, key2, key3, type_usr, hasmainlink)
    elif usr_proceed == "2":
        exit()
    else:
        print("Starting over...")
        askUser()
    
    

askUser()
