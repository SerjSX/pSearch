from tkinter import messagebox

def info_message():
    messagebox.showinfo("About pSearch", '''
    pSearch - Piracy Multi-Search Tool\n
    Programmed by SerjSX to ease finding your favorite software for free.\n\n

    Libraries used:\n
    \t- tkinter and customtkinter: for GUI! Like this box, not possible without Tkinter (customtkinter for modern UI).\n
    \t- urllib and BeautifulSoup: for connecting and scraping websites.\n
    \t- os: mainly used for grabbing directory for connecting to files like the database.\n
    \t- sqlite3: used for connecting to the database file and grabbing information from it.\n
    \t- traceback: to print the errors in a messagebox, if any occured during search.\n
    \t- random - shuffle: for showing the results in a random order and for randomly showing a text in the search bar from a list..\n
    \t- PIL: to process images.\n
    \t- math: to calculate how much buttons the program should display if the results are more than the maximum.
    \t- db_checker: to check the health of each site.\n
    \t- callback: to visit the sites.\n
    \t- base64_functions: allows decoding/encoding base64 codes.\n
    \t- Icons from Google Icons, and Github icon from their own site.\n
    \t- pyperclip: for copying links to clipboard\n\n

    Thank you for using pSearch, and I hope it makes things searching for you!\n
    Program is open-source under the GPL-3.0 license, code can be found on Github.
    ''') 