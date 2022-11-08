import sqlite3
import sys
import re
import urllib.parse
import urllib.request
import urllib.error
import traceback


conn = sqlite3.connect('offlinedb')
cur = conn.cursor()

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}

print("You are about to use a search tool built for the specific text files included within the folder. Any external text file might result error.")

files_list = list()
file_input = input("Enter the file names you want to scan, separate by space and don't forget the extension! Enter: ")
files_split = file_input.split()

for file in files_split:
    count = 0
    try: 
        handle = open(file, encoding='utf8')
    except:
        sys.exit("Not a valid file.")

    print("\n-- Process on file:", file, "--\n")

    type_grab = 'SELECT * FROM Types'
    types_id = list()

    for type in cur.execute(type_grab):
        print("ID:", type[0], "-", type[1])
        types_id.append(type[0])

    try:
        type_input = int(input("Enter input id from above: "))
    except:
        sys.exit("Invalid input")

    order_input = input('Enter line order, 0 = name, 1 = link. Put a space between them. Input in database depends on this, enter: ')
    order_split = order_input.split()

    if type_input in types_id:
        separator_input = input('User needs to enter separator. It is what separates the link and name, it can be - or just spaces. Enter separator: ')
        for line in handle:
            if len(line.split()) == 0 or line.startswith('FROM:'):
                continue
            if separator_input == "":
                name_output = re.findall("(.*)https", line)
                name_format = re.sub(r'\t', '', name_output[0])
                link = re.findall("https.+", line)
                cur.execute('INSERT INTO Websites (name, link, type_id) VALUES (?, ?, ?)', (name_format, link[0], type_input,))
            else:
                linespl = line.split(separator_input)
                cur.execute('INSERT INTO Websites (name, link, type_id) VALUES (?, ?, ?)', (linespl[int(order_split[0])], linespl[int(order_split[1])], type_input))
            count = count + 1
        print("Found", count, "links")
        conn.commit()

    else:
        sys.exit('invalid type id')

print('Done!')
conn.close()
