from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import tkinter.font
import urllib.parse
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import os
import sqlite3
import traceback
import webbrowser
from random import shuffle
from PIL import ImageTk, Image
import math

# Colors used https://www.canva.com/colors/color-palettes/rosy-dew/

# Grabs the directory name
path = os.getcwd()

root = Tk()
root.title("pSearch")
root.iconbitmap(path + "\media\icon.ico")
root.geometry("900x500")

search_progress_window = None
search_progress_frame = None
process_chosen_frame = None

result_name_font = tkinter.font.Font(weight = "bold")
title_font = tkinter.font.Font(size=16, weight="bold")

visit_site_img = Image.open(path + "\media\open_url_button.png")
visit_site_img = visit_site_img.resize((30,30))
visit_site_img = ImageTk.PhotoImage(visit_site_img)

search_img = Image.open(path + "\media\search_button.png")
search_img = search_img.resize((25,25))
search_img = ImageTk.PhotoImage(search_img)

back_img = Image.open(path + "\media\_back_button.png")
back_img = back_img.resize((25,25))
back_img = ImageTk.PhotoImage(back_img)

arrow_forward_img = Image.open(path + "\media\_arrow_forward_button.png")
arrow_forward_img = arrow_forward_img.resize((25,25))
arrow_forward_img = ImageTk.PhotoImage(arrow_forward_img)

# Used to show images for each type afterwards
type_images = {
    'android': path + '\media\_android_image.png',
    'comics_manga': path + '\media\_comics_manga_image.png',
    'courses': path + '\media\_courses_image.png',
    'ebooks': path + '\media\_ebooks_image.png',
    'games': path + '\media\_games_image.png',
    'movieseries': path + "\media\_movieseries_image.png",
    'software': path + '\media\_software_image.png',
    'all': path + '\media\_all_image.png',
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

# allLinks for appending all links at the end (used in Online Database)
allLinks = {}

# best results
best_results = {}

#getting screen width and height of display
width= root.winfo_screenwidth()
height= root.winfo_screenheight()

print("The terminal will be used for displaying errors. Any error you face report on Github with full details.")

# Used when clicking on the results to visit link
def callback(link):
    webbrowser.open_new(link)

# onlineMethod(search_value,site_id) is the main function that searching process works in
def online_method(search_value, site_id, chosen_type, main_link):    
    # These variables below are for the information necessary for the searching process.
    # site_link has the normal link of the website, useful when the grabbed URL doesn't start with the
    # website URL, so we can just add it easily.
    # site_slink has the search URL.
    # site_key1-2-3 are used for grabbing the content from the website, which afterwards the links would
    # be shown from.
    site_link = None
    site_slink = None
    site_key1 = None
    site_key2 = None
    site_key3 = None

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
                            result_links[links.text] = site_link + main_link_a
                        # If not, just append as it is. This is the default for most.
                        else:
                            result_links[links.text] = main_link_a

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
                        result_links[tag.text] = site_link + main_link_b
                        # If it starts with /game and the url is gog-games, then append with the URL at first.
                    elif main_link_b.startswith("/game") and site_link.startswith("https://gog-games.com"):
                        result_links[tag.text] = site_link + main_link_b

        results_count = 0

        # If the length of result_links is greater than 0...
        if len(result_links) > 0:
            # Append the link to allLinks list.
            for link in result_links.items():
                if results_count < 3:
                    best_results[("best", site_name, link[0])] = link[1]
                    results_count = results_count + 1
                else:
                    allLinks[("default", site_name, link[0])] = link[1]

def search_process_signal(button_num, nwindow, chosen_input, 
                        search_value, start_position, end_position):   
    global search_progress_window

    # Splits the chosen_input because when user chooses a specific site it returns the whole name, we
    # needs to just select the ID number of the site.
    chosen_input = chosen_input.split()[0]

    # If the search results window isn't None then most probably there's another one already on-screen,
    # so it destroys it to just have one window.
    if search_progress_window != None:
        search_progress_window.destroy()

    # Create a result window for the frame
    search_progress_window = Toplevel(root)
    search_progress_window.geometry("1250x650")
    
    # Create a canvas for the frame
    search_progress_canvas = Canvas(search_progress_window)
    search_progress_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Add a scrollbar to the canvas
    search_progress_scrollbar = ttk.Scrollbar(search_progress_window, orient=VERTICAL, command=search_progress_canvas.yview)
    search_progress_scrollbar.pack(side=RIGHT, fill=Y)

    # Configure the canvas
    search_progress_canvas.configure(yscrollcommand=search_progress_scrollbar.set)
    search_progress_canvas.bind('<Configure>', lambda e: search_progress_canvas.configure(scrollregion = search_progress_canvas.bbox("all")))

    # Creating another frame in the canvas
    search_progress_frame_two = Frame(search_progress_canvas)

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
        notice_ublock = Label(search_progress_frame_two, text="Please use an adblocker extension, such as uBlock Origin, while browsing any of the below links")
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
                name = keys[i][2]
                link = values[i]

                result_primary_frame = Frame(search_progress_frame_two)
                result_primary_frame.pack(expand=TRUE, fill=BOTH, in_=search_progress_frame_two)

                result_button = Button(result_primary_frame, image=visit_site_img, command=lambda link=link: callback(link), pady=10, padx=10, cursor="hand2")
                result_button.pack(side=LEFT, padx=10)

                result_frame = Frame(result_primary_frame, bd=1, relief=SUNKEN)
                result_frame.pack(expand=TRUE, fill=BOTH, in_=result_primary_frame, pady=20)

                if type == "best":
                    result_site_name = Label(result_frame, text=site_name, bg="#FADCD9", pady=5, padx=5)
                else:
                    result_site_name = Label(result_frame, text=site_name, bg="#F9F1F0", pady=5, padx=5)

                if len(link) > 50:
                    result_link = Label(result_frame, text=link[:49].strip() + "...")
                if len(name) > 70:
                    result_name = Label(result_frame, text=name[:69].strip() + "...")
                else:
                    result_link = Label(result_frame, text=link.strip())
                    result_name = Label(result_frame, text=name.strip())
                
                result_site_name.pack(side=LEFT, fill=BOTH, anchor="w")
                result_name.pack(side=LEFT, expand=TRUE, fill=BOTH, anchor="w")
                result_link.pack(side=LEFT, expand=TRUE, fill=BOTH, anchor="w")

                result_name.configure(font = result_name_font)            

                result_count = result_count + 1

        search_progress_window.title("pSearch - " + str(result_count) + " results - Window " + str(button_num))

            # If it's greater than 100
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
            
                    # If the _count reached 100
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
                other_page_btns = Button(search_progress_frame_two, text=button_id, command=lambda button_id=button_id, button_value=button_value: search_process_signal(str(button_id), True, chosen_input, search_value, button_id*50, button_id*50+button_value), padx=10, pady=5)
                other_page_btns.pack(side=LEFT, padx=10)


    # If it isn't greater than 0, it says No Results
    else:
        noresult = messagebox.showwarning("No results!", "Click Ok to search again.")
        search_progress_window.destroy()

# This is used when the user clicks the buttons to search all at once. It adds the value to 
# the option_chosen variable to it would be processed later on.
def apply_to_variable(chosen_input):
    global option_chosen
    option_chosen.set(chosen_input)


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

    # Top text in the program, introducing the program name
    wlcmsg = Label(root, text="---> pSearch - Piracy Multi-Search Tool <---", bg="#FADCD9")
    wlcmsg.pack(side=TOP, expand=TRUE, fill=BOTH)

    # Applies the title font to the label
    wlcmsg.configure(font = title_font)

    if search_progress_frame != None:
        search_progress_frame.destroy()

    # types_list is used to check if chosen_input is one of the buttons or not.
    types_list = list()
    
    # Connects to the websites database
    conn = sqlite3.connect(path + '/websitesdb')
    # Asigns cursor to execute database functions
    cur = conn.cursor()

    # The websites grabbed from the database are inserted in this list.
    websites = list()

    # Grabs the information from the Database
    for row in cur.execute('''
        SELECT Websites.id, Websites.name, Websites.url, Websites.searchurl, 
        Keys1.name, Keys2.name, Keys3.name, Types.name, Websites.hasmainlink 
            FROM Websites JOIN Keys1 JOIN Keys2 JOIN Keys3 JOIN Types 
                ON Websites.key1_id = Keys1.id AND Websites.key2_id = Keys2.id 
                AND Websites.key3_id = Keys3.id AND Websites.type_id = Types.id'''):
        # Appends it to the websites list.
        websites.append(row)

    # Creates a list for storing the available sites from the database, to be put in dropdown menu afterwards
    websites_list_dropdown = list()

    # For each web in websites, append the id, name and type to websites_list_dropdown to use in dropdown menu
    for web in websites:
        websites_list_dropdown.append(str(web[0]) + " --- " + web[1] + "- Type: " + web[7])

    # Create a StringVar to insert the chosen value in it (either by clicking one of the buttons or from dropdown menu)
    option_chosen = StringVar()

    # Sets the first item in the list as the default chosen input.
    option_chosen.set(websites_list_dropdown[0])

    # Creates a frame to put the search bar, dropdown menu, and search button in it.
    process_chosen_frame = LabelFrame(root, padx=10, pady=10, bd=0)
    process_chosen_frame.pack(padx=10, pady=40) 

    # Create the options dropdown menu
    options_available = OptionMenu(process_chosen_frame, option_chosen, *websites_list_dropdown)
    options_available.pack(side=LEFT) 

    # Creates entry for user input space with width 60        
    search_entry_input = Entry(process_chosen_frame, width=60)

    # Creates the search button widget, with the on-click command heading towards search_process_signal function
    # with passing the option chosen and the search entry.
    search_submit_btn = Button(process_chosen_frame, image=search_img, command=lambda: search_process_signal(0, False, option_chosen.get(), search_entry_input.get(), 0, 0), cursor="hand2")
    search_entry_input.pack(side=LEFT)

    # Focus on the search entry so the user directly starts typing
    search_entry_input.focus_set()

    search_submit_btn.pack(side=RIGHT, padx=10)

    # Bind the keyboard function Enter to the entry so user can directly click Enter to search.
    search_entry_input.bind("<Return>", lambda e: search_process_signal(0, False, option_chosen.get(), search_entry_input.get(), 0, 0))

    # Creates an outer frame for displaying all-in-one types search
    types_outer_frame = LabelFrame(root, bd=0, bg="#F9F1F0")
    types_outer_frame.pack(pady=20)

    # Gets the types from the database in order to display them afterwards
    get_types = cur.execute("SELECT * FROM Types")

    # For each type in the grabbed types (get_types variable)...
    for type in get_types:
        # Save the name of the type in a separate variable, [0] is the id, [1] is the name
        type_name = type[1]

        # Create a frame to insert image and name under it
        type_frame = Frame(types_outer_frame, cursor="hand2", bd=0.5, relief=SUNKEN)
        type_frame.pack(side=LEFT, pady=10, padx=10)

        # Generates the image for the type.
        # The variable has a specific name to prevent errors, and it grabs the directory from the dictionary 
        # according to the type's name.
        type_images["{0}".format(type_name)] = Image.open(type_images[type_name])
        type_images["{0}".format(type_name)] = ImageTk.PhotoImage(type_images["{0}".format(type_name)])
        type_img_btn = Button(type_frame, image=type_images["{0}".format(type_name)], command=lambda type_name=type_name: apply_to_variable(type_name), bd=0)
        type_img_btn.pack(side=TOP)

        # Creates the buttons for each type to display type name
        type_btns = Button(type_frame, text=type_name.capitalize() + " sites", command=lambda type_name=type_name: apply_to_variable(type_name), bd=0)
        type_btns.pack(side=TOP)
            
        # Appends the type name to types_list list to be used for button click identification afterwards
        types_list.append(type[1])

# The beginning program runs beginProgram() function
beginProgram()

# Running loop for Tkinter
root.mainloop()