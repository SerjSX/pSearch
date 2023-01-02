from tkinter import * 
from tkinter import messagebox
import customtkinter
import urllib.parse, urllib.request, urllib.error
from bs4 import BeautifulSoup
import os
import sqlite3
import traceback
from random import shuffle
from PIL import  Image
import math
import random
from zipfile import ZipFile
import sys

# Grabs the directory name
path = sys.path[0]

# Extracts the module zip files needed for the program if they are not already there.
if os.path.exists(path + "/bs4") == False and os.path.exists(path + "/customtkinter") == False:
    for zipname in [path + "/bs4.zip", path + "/customtkinter.zip"]:
        # opening the zip file in READ mode
        with ZipFile(zipname, 'r') as zip: 
            # printing all the contents of the zip file
            zip.printdir() 
            # extracting all the files
            print('Extracting all the files now...')
            zip.extractall(path)
            print('Done!')
else:
    print("Folders already exist, starting program...")

# Database Checker py checks the health of the websites in the database
import db_checker as dc

# Callback py redirects user to browser with a defined link
import callback as cb

# Base64 Decoding/Encoding function
import base64_functions as b64f

# About button
import info

# customtkinter.set_appearance_mode("light")

root = customtkinter.CTk()
root.title("pSearch")

# .ico works only on windows, not linux - Thanks to  viggo-wellme  for mentioning it
# https://github.com/SerjSX/pSearch/pull/3
if os.name == "nt":
    root.iconbitmap(path + "/media/icon.ico")

root.geometry("1050x620")

search_progress_window = None
search_progress_frame = None
process_chosen_frame = None

search_img = customtkinter.CTkImage(light_image=Image.open(path + "/media/search_button.png"),
                                    size=(25,25))


github_img = customtkinter.CTkImage(light_image=Image.open(path + "/media/Github/GitHub-Mark-Light-32px.png"), 
                                    dark_image=Image.open(path + "/media/Github/GitHub-Mark-32px.png"),
                                    size=(25,25))

# Used to show images for each type afterwards
type_images = {
    'android': path + '/media/android_image.png',
    'comics_manga': path + '/media/comics_manga_image.png',
    'courses': path + '/media/courses_image.png',
    'ebooks': path + '/media/ebooks_image.png',
    'games': path + '/media/games_image.png',
    'movieseries': path + "/media/movieseries_image.png",
    'software': path + '/media/software_image.png',
    'music': path + '/media/music_image.png',
    'all': path + '/media/all_image.png',
}

# Used as a header when requesting a website
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}

search_text = ["What do you want to search today?",
                "What do you want to search?",
                "Enter what you want to search here!",
                "Try searching in the FMHY starred collections.",
                "Here is where you put what you want to search.",
                "Enter search value here...",
                "Make sure you fill this before clicking the search button!",
                "Searching ALL sites might take some time, so try to avoid it."]

# allLinks for appending all links at the end (used in Online Database)
allLinks = {}

# best results
best_results = {}

# Connects to the websites database
conn = sqlite3.connect(path + '/others/websitesdb')
# Asigns cursor to execute database functions
cur = conn.cursor()

# The websites grabbed from the database are inserted in this list.
websites = list()

# Grabs the information from the Database
for row in cur.execute('''
    SELECT Websites.id, Websites.name, Websites.url, Websites.searchurl, 
    Keys1.name, Keys2.name, Keys3.name, Types.name, Websites.hasmainlink,
    Websites.collection_id
        FROM Websites JOIN Keys1 JOIN Keys2 JOIN Keys3 JOIN Types 
            ON Websites.key1_id = Keys1.id AND Websites.key2_id = Keys2.id 
            AND Websites.key3_id = Keys3.id AND Websites.type_id = Types.id'''):
    # Appends it to the websites list.
    websites.append(row)

print("The terminal will be used for displaying errors. Any error you face report on Github with full details.")

# Used for changing the software's theme - dark or light
def change_theme(current_theme):
    # This removed current results windows, if there is one, to prevent theme bugs.
    if search_progress_window != None:
        search_progress_window.destroy()

    if current_theme == "Light":
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")


# This is used when the user clicks the buttons to search all at once. It adds the value to 
# the option_chosen variable to it would be processed later on.
def apply_to_variable(chosen_input):
    global site_entry_input
    site_entry_input.set(chosen_input)


# onlineMethod(search_value,site_id) is the main function that searching process works in
def online_method(search_value, site_id, chosen_type, main_link):    
    # These variables below are for the information necessary for the searching process.
    # site_link has the normal link of the website, useful when the grabbed URL doesn't start with the
    # website URL, so we can just add it easily.
    # site_slink has the search URL.
    # site_key1-2-3 are used for grabbing the content from the website, which afterwards the links would
    # be shown from.

    # for each website from the database file...
    for web in websites:
        # If the website from the file matches the user's inserted option...
        if web[0] == site_id:
            # Sets its information to the appropriate variables.
            site_name = web[1]
            site_slink = web[3]
            site_link = web[2]
            site_key1 = web[4]
            site_key2 = web[5]
            site_key3 = web[6]

    # result_links used for appending links from the results.
    result_links = {}

    # If it starts with https://1337x.to then quote it with %20 (space), this is unique for this site
    # because of its web structure.
    if site_link.startswith("https://1337x.to"):
        # If chosen_type is Android, add the keyword "android" at the end for accurate results.
        if chosen_type == "android":
            search_value_fixed = urllib.parse.quote(search_value + " android")
            # Connect the url with the software name the user put at the beginning
            search_url = site_slink + search_value_fixed + "/1/"
        else:
            search_value_fixed = urllib.parse.quote(search_value)
            # Connect the url with the software name the user put at the beginning
            search_url = site_slink + search_value_fixed + "/1/"
    # If the site is FileCR and the chosen type is Android, then specifically search it in
    # the android section for accurate results.
    elif site_id == "1" and chosen_type == "android":
        search_url = site_slink + urllib.parse.quote_plus(search_value) + "&subcat_filter=&category-type=23"
    # If it doesn't start with https://1337x.to/ then quote it with + (it replaces space with +), this is
    # the default method as most sites work this way.
    else:
        search_value_fixed = urllib.parse.quote_plus(search_value)
        # Connect the url with the software name the user put at the beginning
        search_url = site_slink + search_value_fixed

    # Send a request to connect to the site with the header.
    req = urllib.request.Request(url=search_url, headers=header)

    # Try to open the URL to read
    try:
        page_connect = urllib.request.urlopen(req)
        page_code = page_connect.getcode()
    except:
        messagebox.showerror("Error!", "The following site " + search_url + " resulted the following error (search will continue):\n" + traceback.format_exc())
        page_code = -1

    if page_code == 200:
        html = page_connect.read()
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Souping elements according to the chosen software. Some work the same way, so they have
        # the same souping method.
        # If the site_key2-3 aren't 'null', then use the default method (specific class)
        if site_key2 != "null" and site_key3 != "null":
            tags = soup(site_key1, {site_key2: site_key3})
        # If it is null, then this is done on purpose as the websites have special conditions, for example
        # 1337x and gog-games. Explained further afterwards.
        else:
            # soups without a specific class, the site_key1 is most probably "a".
            tags = soup(site_key1)

        # For each tag in tags...
        for tag in tags:
            # Find the "a" / links
            links = tag.find('a')

            # If it didn't result "None"...
            if links is not None:
                # Get the href (link)
                main_link_a = links.get("href")
                # If it isn't None...
                if main_link_a is not None:
                    # If it doesn't start with the following links... (to prevent unnecessary links)
                    if (
                            not main_link_a.startswith("https://w14.monkrus.ws/search/label/")
                            or not main_link_a.startswith("https://w14.monkrus.ws/search?")
                            or main_link_a != "https://w14.monkrus.ws/"
                    ):
                        # If the website chosen is 8, append it with the link. Some sites don't include the
                        # primary URL within their href, so the program adds it. This is a special condition for site 8.
                        if main_link == 1:
                            result_links[links.get_text(" ",strip=True)] = site_link + main_link_a
                        # If not, just append as it is. This is the default for most.
                        else:
                            result_links[links.get_text(" ",strip=True)] = main_link_a

            # If Links resulted None, then the following have special conditions.
            elif links is None:
                # Get the href from the tag, because at first we grabbed the "a" directly.
                main_link_b = tag.get("href")
                # If it isn't None...
                if main_link_b is not None:
                    # If it starts with /torrent and the url is 1337x, then append with the URL at first.
                    # similar to the steamrip one above.
                    # This is to prevent others being shown and the site's structure doesn't include the
                    # primary URL in the beginning, so we add it first.
                    if main_link_b.startswith("/torrent/"):
                        # uses tag.text because the name/link is already in the looped tag.
                        result_links[tag.get_text(" ",strip=True)] = site_link + main_link_b
                        # If it starts with /game and the url is gog-games, then append with the URL at first.
                    elif main_link_b.startswith("/game") and site_link.startswith("https://gog-games.com"):
                        result_links[tag.get_text(" ",strip=True)] = site_link + main_link_b

        results_count = 0

        # If the length of result_links is greater than 0...
        if len(result_links) > 0:
            # Append the link to allLinks list.
            for link in result_links.items():
                if results_count < 1:
                    best_results[("best", site_name, site_link, link[0])] = link[1]
                    results_count = results_count + 1
                else:
                    allLinks[("default", site_name, site_link, link[0])] = link[1]


def search_process_signal(button_num, nwindow, chosen_input, 
                        search_value, start_position, end_position):   
    global search_progress_window

    int_or_str = None

    # Used for collection, need whole chosen text
    actual_chosen_input = chosen_input
    
    try:
        # Splits the chosen_input because when user chooses a specific site it returns the whole name, we
        # needs to just select the ID number of the site.
        chosen_input = chosen_input.split()[0]        
    
        chosen_input = int(chosen_input)
        int_or_str = "int"
    except:
        int_or_str = "str"

    # If the search results window isn't None then most probably there's another one already on-screen,
    # so it destroys it to just have one window.
    if search_progress_window != None:
        search_progress_window.destroy()


    if len(search_value) != 0:

        # if in: is in the search value then a special condition is detected.
        # A special condition is a shortcut to directly search in a website without using the dropdown for selection.
        if int_or_str == "str" and not chosen_input.startswith("C-") and chosen_input not in types_list:
            # foundPing is used for detecting if a matching site has been found, to prevent multiple sites.
            foundPing = False

            # For each website in websites...
            for web in websites:
                # If the chosen_input (lowercased) is in the web's [1] which is the name of the 
                # website (lowercased) then...
                if chosen_input.lower() in web[1].lower():
                    # Asign the site's id to chosen_input
                    chosen_input = str(web[0])
                    # Change the ping to True
                    foundPing = True
                    # Break the loop
                    break

            # if the ping stays False then no matching sites were found, throws an error.
            if foundPing == False:
                messagebox.showerror("Error!", "Invalid site name input, either empty it or put a valid name.")  
                return

        # Create a result window for the frame
        search_progress_window = customtkinter.CTkToplevel(root)
        search_progress_window.geometry("1250x650")
    
        search_progress_frame = customtkinter.CTkFrame(search_progress_window)
        search_progress_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Create a canvas for the frame
        search_progress_canvas = customtkinter.CTkCanvas(search_progress_frame)
        search_progress_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        if customtkinter.get_appearance_mode() == "Light":
            search_progress_canvas.configure(bg="white")
    
        else:
            search_progress_canvas.configure(bg="#302c2c")

        # Add a scrollbar to the canvas
        search_progress_scrollbar = customtkinter.CTkScrollbar(search_progress_frame, orientation=VERTICAL, command=search_progress_canvas.yview)
        search_progress_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the canvas
        search_progress_canvas.configure(yscrollcommand=search_progress_scrollbar.set)
        search_progress_canvas.bind('<Configure>', lambda e: search_progress_canvas.configure(scrollregion = search_progress_canvas.bbox("all")))

        # Creating another frame in the canvas
        search_progress_frame_two = customtkinter.CTkFrame(search_progress_canvas, fg_color="transparent")

        # Adding a new frame to the window
        search_progress_canvas.create_window((0,0), window=search_progress_frame_two, anchor="nw") 

        if nwindow == False:
            # Clears allLinks and best_results to start over with a new search.
            allLinks.clear()
            best_results.clear()

            # in case user chose all sites...
            if chosen_input == "all":
                for site in websites:
                    # Activate the onlineMethod function with forwarding the site's ID.
                    online_method(search_value, site[0], 0, site[8])

            # If chosen_input is in the types_list, indicates that user clicked one of the buttons...
            elif chosen_input in types_list:
                # for each site in sites
                for site in websites:
                    if chosen_input in site[7] or "all" in site[7]:
                        # Activate the onlineMethod function with forwarding the site's ID.
                        online_method(search_value, site[0], 0, site[8])

            elif actual_chosen_input.startswith("C-"):
                split = actual_chosen_input.split("-")
                for site in websites:
                    if int(split[1].strip()) == site[9]:
                        online_method(search_value, site[0], 0, site[8])

            # This runs as the default method, which is when the user selects a specific site
            else:
                # Forward it to the online_method function
                for web in websites:
                    if web[0] == int(chosen_input):
                        online_method(search_value, web[0], 0, web[8])

        # At the end, it prints the results if the length of allLinks OR best results is greater than 0
        if len(allLinks) > 0 or len(best_results) > 0:
            # result_count is used to limit how much results the program is allowed to show.
            result_count = 0 

            # If nwindow is false then it shuffles the results, or else 
            # if true then it's a signal for new window, so no need to shuffle to keep
            # order stable and still.
            if nwindow == False:
                # Shuffles the allLinks dictionary items
                shuffled_links = [*allLinks.items()]
                shuffle(shuffled_links)
        
                # Shuffles the best links dictionary items
                shuffled_best_links = [*best_results.items()]
                shuffle(shuffled_best_links)

                # Creates a new dictionary in order to merge both shuffled links
                global final_links
                final_links = dict()

                # First appends from the best results because it shows best results at first
                for link in shuffled_best_links:
                    final_links[link[0]] = link[1]
        
                # Then it appends from the normal links 
                for link in shuffled_links:
                    final_links[link[0]] = link[1]

                start_position = 0
                end_position = len(final_links)

            # Creates a notice block to always use an adblocker extension
            notice_ublock = customtkinter.CTkLabel(search_progress_frame_two, text="Please use an adblocker extension, such as uBlock Origin, while browsing any of the below links")
            notice_ublock.pack(expand=TRUE, fill=BOTH)

            # Convert dictionary keys and values to list to select accordingly afterwards
            keys = list(final_links.keys())
            values = list(final_links.values())

            for i in range(start_position, end_position):
                if result_count < 50:
                    global result_link
                    global result_name

                    # Assign variables to each necessary information
                    # i = index number according to start_position and end_position
                    type = keys[i][0]
                    site_name = keys[i][1]
                    site_link = keys[i][2]
                    name = keys[i][3]
                    link = values[i]

                    result_primary_frame = customtkinter.CTkFrame(search_progress_frame_two)
                    result_primary_frame.pack(expand=TRUE, fill=BOTH, in_=search_progress_frame_two, pady=20)

                    result_frame = customtkinter.CTkFrame(result_primary_frame)
                    result_frame.pack(expand=TRUE, fill=BOTH, in_=result_primary_frame)

                    result_link_frame = customtkinter.CTkFrame(result_primary_frame)
                    result_link_frame.pack(expand=TRUE, fill=BOTH, side=TOP)

                    if type == "best":
                        result_site_name = customtkinter.CTkButton(result_frame, text=" " + site_name + " ", fg_color="#A8E4A0", hover_color="#D8E4BC", corner_radius=0 ,width=40, text_color="black", command=lambda site_link=site_link: cb.callback(site_link))
                    else:
                        result_site_name = customtkinter.CTkButton(result_frame, text=" " + site_name + " ", fg_color="orange", hover_color="yellow", corner_radius=0, width=40, text_color="black", command=lambda site_link=site_link: cb.callback(site_link))

                    if len(link) > 200:
                        result_link = customtkinter.CTkLabel(result_link_frame, text=link[:199].strip() + "...", cursor="hand2", font=customtkinter.CTkFont(size=12))
                    else:
                        result_link = customtkinter.CTkLabel(result_link_frame, text=link.strip(), cursor="hand2", font=customtkinter.CTkFont(size=12))

                    if len(name) > 110:
                        result_name = customtkinter.CTkLabel(result_frame, text=name[:109].strip() + "...", cursor="hand2", font=customtkinter.CTkFont(size=18, weight="bold"))
                    else:
                        result_name = customtkinter.CTkLabel(result_frame, text=name.strip(), cursor="hand2", font=customtkinter.CTkFont(size=18, weight="bold"))
                
                    result_site_name.pack(side=LEFT, fill=BOTH, anchor="w")
                    result_name.pack(side=LEFT, anchor="w", padx=10)
                    result_link.pack(side=LEFT, anchor="w")
                
                    result_name.bind("<Button-1>", lambda e,link=link: cb.callback(link))
                    result_link.bind("<Button-1>", lambda e,link=link: cb.callback(link))

                    result_count = result_count + 1

            search_progress_window.title("pSearch - " + str(result_count) + " results - Window " + str(button_num))

                # If it's greater than 50
            if len(final_links) > 50:
                # _count is used for counting each number from the input
                several_btn_count = 0
                # _length has the length of the results
                several_btn_length = len(final_links)
                # _list to append the amount for each button
                global several_btn_list
                several_btn_list = list()

                # Divides the input by 50 (to get appx how many buttons it needs)
                btn_count = math.ceil(several_btn_length/50)

                # For b in the range of btn_count...
                for b in range(btn_count):
                    # for i in the range of the input plus one...
                    for i in range(several_btn_length + 1):      
            
                        # If the _count reached 50
                        if several_btn_count == 50:
                            # append it to the list
                            several_btn_list.append(str(b) + "-" + str(several_btn_count))
                            # deduct from _length the appended amount
                            several_btn_length = several_btn_length - several_btn_count
                            # reset the btn count to 0
                            several_btn_count = 0
                            # break and start over
                            break

                        # if the b is the last button count and the _count matches the _length, which means
                        # it's the last button's amount...
                        if b == btn_count - 1 and several_btn_count == several_btn_length:
                            # append _count to the list
                            several_btn_list.append(str(b) + "-" + str(several_btn_count))

                        # Increment several_btn_count by 1
                        several_btn_count += 1

                # For each button in the buttons list
                for button in several_btn_list:
                    # Split the value
                    button_split = button.split("-")
                    # Put the id and value in separate variables
                    button_id = int(button_split[0])
                    button_value = int(button_split[1])

                    # create the button by passing starting position(button_id*50) and ending position(button_id*50+button_value)
                    other_page_btns = customtkinter.CTkButton(search_progress_frame_two, text=button_id, command=lambda button_id=button_id, button_value=button_value: search_process_signal(str(button_id), True, chosen_input, search_value, button_id*50, button_id*50+button_value), width=30, height=30)
                    other_page_btns.pack(side=LEFT, padx=10)

        # If it isn't greater than 0, it says No Results
        else:
            noresult = messagebox.showwarning("No results!", "Click Ok to search again.")
            search_progress_window.destroy()

    else:
        messagebox.showerror("No search input!", "Hmm, you're going to search... Nothing? Try again.")


# Asks user to insert inputs, the beginning of the program.
def beginProgram():
    # Variables required to be global in order to function properly
    global option_chosen
    global websites
    global cur
    global wlcmsg
    global types_list
    global search_progress_frame
    global process_chosen_frame
    global get_collections
    global site_entry_input

    # This frame includes other buttons with small functions
    top_functions_frame = customtkinter.CTkFrame(root)
    top_functions_frame.pack(side=TOP, fill=BOTH)

    # theme changer button
    toggle_theme_btn = customtkinter.CTkButton(top_functions_frame, text=" Change Theme ", command=lambda: change_theme(customtkinter.get_appearance_mode()), width=40, corner_radius=0)
    toggle_theme_btn.pack(side=LEFT, padx=5)

    # db_checker button
    db_checker_btn = customtkinter.CTkButton(top_functions_frame, text=" DB Checker ", command=dc.db_checker, width=40, corner_radius=0)
    db_checker_btn.pack(side=LEFT)

    # base64_functions button
    base64_functions_btn = customtkinter.CTkButton(top_functions_frame, text=" Base64 Encode/Decode ", command=b64f.start_base64, width=40, corner_radius=0)
    base64_functions_btn.pack(side=LEFT, padx=5)

    # about/info button
    about_btn = customtkinter.CTkButton(top_functions_frame, text=" About pSearch ", command=info.info_message, width=40, corner_radius=0)
    about_btn.pack(side=RIGHT, padx=5)

    wlcmsg = customtkinter.CTkLabel(root, text="pSearch - Piracy Multi-Search Tool", font=customtkinter.CTkFont(size=24, weight="bold"))
    wlcmsg.pack(side=TOP, pady=100)

    if search_progress_frame != None:
        search_progress_frame.destroy()

    # types_list is used to check if chosen_input is one of the buttons or not.
    types_list = list()

    # collection_list is used for storing collection names and ids from the database
    collection_list = list()

    # Creates a list for storing the available sites from the database, to be put in dropdown menu afterwards
    websites_list_dropdown = list()

    # For each web in websites, append the id, name and type to websites_list_dropdown to use in dropdown menu
    for web in websites:
        websites_list_dropdown.append(str(web[0]) + " --- " + web[1] + "- Type: " + web[7])

    # Create a StringVar to insert the chosen value in it (either by clicking one of the buttons or from dropdown menu)
    option_chosen = StringVar()

    # Sets the first item in the list as the default chosen input.
    option_chosen.set("all")

    # Creates a frame to put the search bar, dropdown menu, and search button in it.
    process_chosen_frame = customtkinter.CTkFrame(root, fg_color="transparent")
    process_chosen_frame.pack(padx=10, pady=10) 

    # Creates entry for user input space with width 300      
    search_entry_input = customtkinter.CTkEntry(process_chosen_frame, height=30, width=350, placeholder_text=random.choice(search_text))

    # Creates entry for user input space with width 300      
    site_entry_input = customtkinter.CTkComboBox(process_chosen_frame, variable=option_chosen, values=websites_list_dropdown, height=30, width=200, command=lambda e: apply_to_variable(site_entry_input.get()))
    site_entry_input.set("Enter site name here")

    # Creates the search button widget, with the on-click command heading towards search_process_signal function
    # with passing the option chosen and the search entry.
    search_submit_btn = customtkinter.CTkButton(process_chosen_frame, 
                                                text="", 
                                                image=search_img, 
                                                command=lambda: search_process_signal(0, False, site_entry_input.get(), search_entry_input.get(), 0, 0), 
                                                width=10,
                                                height=10)

    site_entry_input.pack(side=LEFT, padx=5)
    search_entry_input.pack(side=LEFT)

    search_submit_btn.pack(side=RIGHT, padx=10)

    # Bind the keyboard function Enter to the entry so user can directly click Enter to search.
    search_entry_input.bind("<Return>", lambda e: search_process_signal(0, False, site_entry_input.get(), search_entry_input.get(), 0, 0))


    tabview = customtkinter.CTkTabview(root, height=40)
    tabview.pack(pady=20)

    tabview.add("Types")
    tabview.add("Collections")


    # Creates an outer frame for displaying all-in-one types search
    types_outer_frame = customtkinter.CTkFrame(tabview.tab("Types"), fg_color="transparent")
    types_outer_frame.pack(pady=20)

    # Gets the types from the database in order to display them afterwards
    get_types = cur.execute("SELECT * FROM Types")

    # For each type in the grabbed types (get_types variable)...
    for type in get_types:
        # Save the name of the type in a separate variable, [0] is the id, [1] is the name
        type_name = type[1]

        # Create a frame to insert image and name under it
        type_frame = customtkinter.CTkFrame(master=types_outer_frame)
        type_frame.pack(side=LEFT, pady=10, padx=5)

        # Generates the image for the type.
        # The variable has a specific name to prevent errors, and it grabs the directory from the dictionary 
        # according to the type's name.
        type_images["{0}".format(type_name)] = customtkinter.CTkImage(light_image=Image.open(type_images[type_name]),
                                                                    size=(48,48))

        # Creates the buttons for each type to display type name
        type_btns = customtkinter.CTkButton(master=type_frame, 
                                            width=70,
                                            height=32,
                                            text=type_name.capitalize() + " sites", 
                                            command=lambda type_name=type_name: apply_to_variable(type_name),
                                            image=type_images["{0}".format(type_name)],
                                            compound="top")
        type_btns.pack(side=TOP)

        # Appends the type name to types_list list to be used for button click identification afterwards
        types_list.append(type[1])

    # Used for collection buttons
    get_collections = cur.execute("SELECT * FROM Collections")

    for collection in get_collections:
        # Save the name of the type in a separate variable, [0] is the id, [1] is the name
        collection_name = collection[1]
        collection_id = collection[0]

        # Appends the type name to types_list list to be used for button click identification afterwards
        collection_list.append("C-" + str(collection_id) + " - " + collection_name)

    collection_text = customtkinter.CTkLabel(master=tabview.tab("Collections"), text="Sites that are in collections are starred in a popular megathread. For example, the sites in the FMHY collections have a star in their megathread.")
    collection_text.pack()

    segemented_button_var = customtkinter.StringVar(value="None")  # set initial value

    segemented_button = customtkinter.CTkOptionMenu(master=tabview.tab("Collections"),
                                                    values=collection_list,
                                                    variable=segemented_button_var,
                                                    command=lambda e: apply_to_variable(segemented_button.get())
                                                )
    
    segemented_button.pack(pady=10)

    like_text = customtkinter.CTkLabel(master=root, text="Did you like the program? Star it on Github!").pack()
    github_button = customtkinter.CTkButton(master=root, text="", height=30, width=0, corner_radius=0, image=github_img, command=lambda: cb.callback("https://github.com/SerjSX/pSearch/")).pack(pady=5)

    

# The beginning program runs beginProgram() function
beginProgram()

# Running loop for Tkinter
root.mainloop()