from collections import defaultdict
import os
import sys
import json
from others.html_conn import page_conn
from others.progress_bar import progressBar
from random import shuffle
from tkinter import messagebox
import urllib.request
import requests

# CONTRIBUTORS/DEVELOPERS ONLY: Change to True if you are adding a site,
# that way it doesn't connect to the online database and it uses the offline one
# with your modifications.
testMode = False

# Grabs the directory name
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    path = sys._MEIPASS
else:
    path = os.path.dirname(os.path.abspath(__file__))
    print(path)


class websites:
    """
        Responsible to load, store and operate on websites from JSON file.
    
        Attributes:
            all_websites:       stores all websites loaded based on their types in a dictionary.
                                the key is the type, and the value is the site's information.
            database_file_path: the path to connect to before loading the json file.
            
        Methods and Properties:
            __init__() : initializes the attribute all_websites
            load_json(): downloads and loads the json file, and adds the websites to the all_websites 
                         attribute. The method chooses whether to download the online JSON file or to 
                         use the local JSON file based on the size of both files, whether they have the 
                         same size or different. If different, the online JSON file is downloaded.
                         The path of the JSON file used to load the websites depends on whether testMode variable is True or False and whether there is an internet connection 
                         or no.
            get_all()  : returns all of the websites as a list, without being grouped by the 
                         types.             
            get_types(): returns a list containing the types of the websites stored.        
            get_all_type(chosen_type):
                         returns the websites of a specific type and the type "all".
            get_one_site(name): returns the data of a single site.
            __len__():   returns the length of the all_websites attribute.
            create_web_set(name):
                         prepares the list of websites the program should loop and search at based on
                         the chosen site/type.
            search(chosen_input, search_value, nwindow):
                         Does the searching operation with using methods from html_conn.py.
                            chosen_input is the chosen site/type.
                            search_value is the string to search in the sites.
                            nwindow is to identify if the user already has a results window and the 
                            method was clicked, then it means the user clicked on one of the buttons 
                            that are at the end of the results page if the results are > 30. This way it does not shuffle the websites again.
    
    """
    
    # Initializing the variable to store websites in
    def __init__(self):
        # The following variable will store all of the websites grouped by category
        self.all_websites = defaultdict(list)

    # Loading the JSON file
    def load_json(self):
        # Path to connect to the database file afterwards depending on the localvsonline file, if test mode is enabled or no, and if there is wifi connection.
        self.database_file_path = path

        # If the testMode is off, proceed with the normal checking.
        if testMode == False:
            # Checks if the database file in the default path exists
            # means that it has been already downloaded from online
            # if not sets the program to differenciate the file size online vs local by using the database
            # file from the /others/ folder.
            if os.path.isfile(path + "/online_json/websites.json") == True:
                localCheckPath = path + '/online_json/websites.json'
                print("Found database file from the online_json folder!")

            else:
                localCheckPath = path + '/websites.json'
                print("Using the local database file")

            # This variable stores the size of the local json file.
            localCheckSize = os.path.getsize(localCheckPath)


            # Tries to download the latest database from Github to compare the file sizes
            try:
                database_url = "https://raw.githubusercontent.com/SerjSX/pSearch/master/others/websites.json"

                # Connects to the online database file to check and store its size.
                onlineCheckReq = urllib.request.Request(database_url, method='HEAD')
                onlineCheckURL = urllib.request.urlopen(onlineCheckReq)
                onlineCheckSize = onlineCheckURL.headers['Content-Length']
                print("Online database size is:", onlineCheckSize)
                print("Local database size is:", localCheckSize)
    

                # Checking if the local json file and the online jason file have the same size, if yes then it does not download the online
                # json file.
                # If no, it downloads the online file so the local would be up-to-date.
                if int(localCheckSize) == int(onlineCheckSize):
                    print("The online and local database have the same size, hence no need to download")
                    # Sets the database_file_path to the localCheckPath,which is either /websites.json or /others/websites.json depending on the
                    # previous if-else condition of checking os.path.isfile whether the json file is in the others folder or no.
                    self.database_file_path = localCheckPath  
  
                else:
                    print("The online and local database don't have the same size, the program will automatically download the latest version")
                    print("Downloading database file...")
                    r = requests.get(database_url) # create HTTP response object

                    # creating a new file and writing the content to it from the online json file.
                    with open(path + "/online_json/websites.json",'wb') as f:

                        # Saving received content as a png file in
                        # binary format

                        # write the contents of the response (r.content)
                        # to a new file in binary mode.
                        f.write(r.content)
        
                    print("Done")
                    self.database_file_path += "/online_json/websites.json"

           
        
            # If it fails to connect and download, then uses the database file from the /others/ folder.
            # Which is the default that comes with the program.
            except:
                print("Failed to connect to the server for downloading database, using the local database file")
                # Connects to this database which is the one that came from the release, if
                # it fails to connect to the internet
                self.database_file_path += '/websites.json'

        else:
            print("Connecting to the local database since testMode is enabled")
            self.database_file_path += '/websites.json'       


        print("\n---Database Checking Done---", "Connecting and loading: " + self.database_file_path)

        with open(self.database_file_path) as f:
            file_data = json.load(f)
            for i in file_data:
                self.all_websites[i['type']].append(i)

 
    # Getting all websites as a list
    def get_all(self):
        websites = [web for webs in self.all_websites.values() for web in webs]
        return (websites)
        
    # Getting all the types of sites
    def get_types(self):
        return (self.all_websites.keys())
    
    # Getting all sites in a specific type, including "all"
    def get_all_type(self,chosen_type):
        return (self.all_websites[chosen_type] + self.all_websites['all'])
    
    # Getting one site only based on user input, returns -1 if none found.
    def get_one_site(self,name):
        for web in self.get_all():
            if (web['name'].lower() == name.lower()) or (name.lower() in web['name'].lower()):
                return [web]
        
        return -1
    
    # Allows to do len() on the class
    def __len__(self):
        return (len(self.all_websites))

    # This method creates a list of websites that the program automatically should loop over and 
    # search. First it checks if the passed value, name, is one of the types. Then it checks if it's
    # "all", and at last it finds the specific site since neither of the above two were met.
    def create_web_set(self,name):
        # Gets the specific type sites and all of the sites with "all" type.
        if (name in self.get_types()) and (name != 'all'):
            return self.get_all_type(name)
        # if the name is all, then all sites are going to be searched in
        elif name == 'all':
            return self.get_all()
        # if neither of the above 2, then it's a specific site and the websites variable will just 
        # have one item.
        else:
            return self.get_one_site(name) 
            
            
    # Responsible to search in a specific site.
    def search(self, chosen_input, search_value,nwindow):
        bestResults,allLinks = {},{}
        
        websites = self.create_web_set(chosen_input) # Creates the set of websites to search in
        
        # Only proceed searching if websites is not -1. If it is, then the site name that the 
        # user entered is invalid hence an error is thrown.
        if websites != -1:
            progress_bar = progressBar(len(websites)) # Creates the progress bar
        
            for web in websites:       
                # Sets its information to the appropriate variables.
                site_name = web['name']
                site_slink,site_link = web['searchurl'],web['url']
                site_key1,site_key2,site_key3 = web['key1'],web['key2'],web['key3']
                plusorspace,hasmainlink,type_ = web['plusorspace'],web['hasmainlink'],web['type']
                
                print(f"Searching at {site_slink}")
                
                # Initialize page_conn which adjusts the search URL as well
                page_connection = page_conn(search_value,site_name,site_link,site_slink,type_,plusorspace)
            
                # Attempts to get the HTML content based on the previously found URL.
                html,page_code = page_connection.get_html()
                        
                if page_code == 200:
                    scrape_return = page_connection.scrape(html,site_link,site_key1,site_key2,site_key3,hasmainlink)
                    
                    # If scrape return isn't -1, then add the results to bestResults and allLinks.
                    if scrape_return != -1:
                        bestResults.update(scrape_return[0])
                        allLinks.update(scrape_return[1])
                
                # adds a step to the progress bar.
                progress_bar.add_step() 
  
            # If nwindow is false then it shuffles the results, or else 
            # if true then it's a signal for new window, so no need to shuffle to keep
            # order stable and still.
            if nwindow == False:
                # Shuffles the allLinks dictionary items
                shuffled_links = [*allLinks.items()]
                shuffle(shuffled_links)
        
                # Shuffles the best links dictionary items
                shuffled_best_links = [*bestResults.items()]
                shuffle(shuffled_best_links)

                # Creates a new dictionary in order to merge both shuffled links
                final_links = dict()

                # First appends from the best results because it shows best results at first
                # At then it does the same but for the normal links.
                for link in shuffled_best_links:
                    final_links[link[0]] = link[1]    
                for link in shuffled_links:
                    final_links[link[0]] = link[1]
            
            # closes the progress bar window
            progress_bar.close_window()
            
            # returns the results
            return final_links
        
        # Invalid site name input error.
        else:
            messagebox.showerror("Error!", "Invalid site name input, please either put a valid name, choose one from the dropdown list or click on a shortcut button.")  
            return -1