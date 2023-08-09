# This program is used for checking if the sites have a valid page return code.
# Can be used from within the main program.
import urllib.parse
import urllib.request
import urllib.error
import sqlite3
from tkinter import messagebox
from tkinter import * 
import os
import sys

# Grabs the directory name
path = sys.path[0]

# Used as a header when requesting a website
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}

# Connects to the websites database
conn = sqlite3.connect(path + '/others/websitesdb')
# Asigns cursor to execute database functions
cur = conn.cursor()

# db_checker is used for checking if all sites from the database are healthy.
def db_checker():
    db_checker_confirm = messagebox.askyesno("Database Checking Operation",
    '''This operation is used for checking if all of the sites in the database return healthy page codes. It might take some time and you won't be able to use the program until it's done.\n
    Click Yes if you want to proceed; progress will be displayed via message boxes like this, and errored sites will be printed in the command line terminal.\n
    Click No if you want to return to the program.''')

    if db_checker_confirm == 1:
        # Used for selecting all content from the Websites table
        websites = cur.execute("SELECT * FROM Websites")

        # This dictionary will contain the sites that resulted errors
        errored_sites = dict()

        messagebox.showinfo("Database Checking Operation", "The process is being run in the background on each site, once it's done there will be another message box stating the result. You can also check the command line for progress.")

        for site in websites:
            print("Starting operation on " + site[2])

            page_code = -1
    
            # Send a request to connect to the site with the header.
            req = urllib.request.Request(url=site[2], headers=header)

            # Try to open the URL to read
            try:
                page_connect = urllib.request.urlopen(req)
                page_code = page_connect.getcode()
            except:
                errored_sites[site[2]] = page_code

            if page_code != 200:
                errored_sites[site[2]] = page_code

        if len(errored_sites) > 0:
            print("\n\nThe following sites resulted an error:")
            messagebox.showinfo("Database Checking Operation - " + str(len(errored_sites)) + "errors", 
                                "Check command line/terminal for list")
            for site,code in errored_sites.items():
                print(site + ", with code: " + str(code))
                
            val = messagebox.askyesno("Delete or Keep", "Do you want to delete the ones that resulted an error?")
            
            if val == 1:
            	for site,code in errored_sites.items():
            		print("Deleting", site)
            		cur.execute("DELETE FROM Websites WHERE url = ?", (site,))
            		
            	print("Done Deleting")
            	conn.commit()
						
				
        else:
            messagebox.showinfo("Database Checking Operation", "The operation resulted no errors.")

        print("Database Checking Operation is done, it is recommended to reload program in case of deleted sites.")

    
