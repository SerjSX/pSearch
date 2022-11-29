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

# Colors used https://www.canva.com/colors/color-palettes/rosy-dew/

root = Tk()
root.title("pSearch")
root.iconbitmap("icon.ico")
root.geometry("1200x600")

search_progress_window = None
search_progress_frame = None
process_chosen_frame = None

result_name_font = tkinter.font.Font(weight = "bold")
title_font = tkinter.font.Font(size=16, weight="bold")

# Used for identifying row position, 1 becauase on 0 there's usually a text
error_count = 1

# Grabs the directory name [BETA TESTING: to prevent file not found error]
path = os.path.dirname(os.path.abspath(__file__))

visit_site_img = Image.open("open_url_button.png")
visit_site_img = visit_site_img.resize((30,30))
visit_site_img = ImageTk.PhotoImage(visit_site_img)

search_img = Image.open("search_button.png")
search_img = search_img.resize((25,25))
search_img = ImageTk.PhotoImage(search_img)

back_img = Image.open("back_button.png")
back_img = back_img.resize((25,25))
back_img = ImageTk.PhotoImage(back_img)

arrow_forward_img = Image.open("arrow_forward_button.png")
arrow_forward_img = arrow_forward_img.resize((25,25))
arrow_forward_img = ImageTk.PhotoImage(arrow_forward_img)

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
    global error_count
    
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
        error_count = error_count + 1
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
                    if main_link_b.startswith("/torrent"):
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

def search_process_signal(chosen_input, search_value):   
    allLinks.clear()
    best_results.clear()
    global search_progress_window

    if search_progress_window:
        search_progress_window.destroy()

    # Create a result window for the frame
    search_progress_window = Toplevel(root)
    search_progress_window.geometry("1200x600")
    
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

    if chosen_input in types_list:
        # for each site in sites
        for site in websites:
            if chosen_input in site[7] or "all" in site[7]:
                # Activate the onlineMethod function with forwarding the site's ID.
                online_method(search_value, site[0], 0, site[8])
                search_progress_window.title("pSearch - " + chosen_input + " results")

    # This runs as the default method, which is when the user types a specific number
    # for a specific software.
    else:
        # Forward it to the online_method function
        for web in websites:
            if web[0] == int(chosen_input):
                online_method(search_value, web[0], 0, web[8])
                search_progress_window.title("pSearch - " + web[1] + " results")

    # At the end, it prints the results if the length of allLinks is greater than 0
    if len(allLinks) > 0 or len(best_results) > 0:
        result_count = 0 
        result_row_count = 1

        if len(allLinks) > 0:
            shuffled_links = [*allLinks.items()]
            shuffle(shuffled_links)
        
        shuffled_best_links = [*best_results.items()]
        shuffle(shuffled_best_links)

        final_links = dict()

        for link in shuffled_best_links:
            final_links[link[0]] = link[1]
        
        if len(allLinks) > 0:
            for link in shuffled_links:
                final_links[link[0]] = link[1]

        for names,link in final_links.items():
            if result_count < 200:
                type = names[0]
                site_name = names[1]
                name = names[2]
                link = link

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
                if len(name) > 60:
                    result_name = Label(result_frame, text=name[:59].strip() + "...")
                else:
                    result_link = Label(result_frame, text=link.strip())
                    result_name = Label(result_frame, text=name.strip())
                
                result_site_name.pack(side=LEFT, fill=BOTH, anchor="w")
                result_name.pack(side=LEFT, expand=TRUE, fill=BOTH, anchor="w")
                result_link.pack(side=LEFT, expand=TRUE, fill=BOTH, anchor="w")
                result_row_count = result_row_count + 3   

                result_name.configure(font = result_name_font)            

                result_count = result_count + 1

    # If it isn't greater than 0, it says No Results
    else:
        noresult = messagebox.showwarning("No results!", "Click Ok to search again.")


def process_chosen_input(chosen_input):

    # if the chosen_input is in info_list...
    if chosen_input in id_list or chosen_input in types_list:   
        global search_progress_frame
        global process_chosen_frame

        if search_progress_frame != None:
            search_progress_frame.destroy()

        ask_user_frame.destroy()
        process_chosen_frame = LabelFrame(root, text="Enter what you want to search below, then click the Search button", padx=10, pady=10)
        process_chosen_frame.pack(side=TOP, padx=10, pady=30)          
        search_entry_input = Entry(process_chosen_frame, width=40)
        search_submit_btn = Button(process_chosen_frame, image=search_img, command=lambda: search_process_signal(chosen_input, search_entry_input.get()), cursor="hand2")
        search_return_btn = Button(process_chosen_frame, image=back_img, command=lambda: beginProgram(True), cursor="hand2")
        search_return_btn.pack(side=LEFT, padx=10, pady=10)
        search_entry_input.pack(side=LEFT)
        search_entry_input.focus_set()
        search_submit_btn.pack(side=LEFT, padx=10)
        
        # Creates a another frame in root for results
        search_progress_frame = Frame(root)
        search_progress_frame.pack(fill=BOTH, expand=True)
        

    # If the input is a valid number, ask the user to start over.
    else:
        cur.close()
        invalid_input = messagebox.showerror("No input!", "Click OK to start over")
        
        if invalid_input == "ok":
            beginProgram(True)


# Asks user to insert inputs, the beginning of the program.
def beginProgram(doublesession):
    global ask_user_frame
    global chosen_id
    global websites
    global cur
    global info_list
    global id_list
    global error_count
    global wlcmsg
    global types_list

    wlcmsg = Label(root, text="---> pSearch - Piracy Multi-Search Tool <---", bg="#FADCD9", padx=10, pady=10)
    wlcmsg.pack(side=TOP, expand=TRUE, fill=BOTH)
    wlcmsg.configure(font = title_font)

    error_count = 1

    if doublesession == True:
        ask_user_frame.destroy()
        wlcmsg.destroy()
        
        if search_progress_frame != None:
            search_progress_frame.destroy()

        if process_chosen_frame != None:
            process_chosen_frame.destroy()

        if search_progress_window != None:
            search_progress_window.destroy()

    ask_user_frame = LabelFrame(root, bd=0)
    ask_user_frame.pack(padx=10, pady=30)
    chosen_id = StringVar()
    chosen_id.set('ID')

    # info_list is used to print the available options afterwards.
    info_list = list()
    id_list = list()
    types_list = list()
    
    conn = sqlite3.connect(path + '/websitesdb')
    cur = conn.cursor()
    # The websites list
    websites = list()

    # Grabs the information from the Database
    for row in cur.execute('''
        SELECT Websites.id, Websites.name, Websites.url, Websites.searchurl, 
        Keys1.name, Keys2.name, Keys3.name, Types.name, Websites.hasmainlink 
            FROM Websites JOIN Keys1 JOIN Keys2 JOIN Keys3 JOIN Types 
                ON Websites.key1_id = Keys1.id AND Websites.key2_id = Keys2.id 
                AND Websites.key3_id = Keys3.id AND Websites.type_id = Types.id'''):
        # Appends it to the websites var list.
        websites.append(row)

    # webcount and columncount will be used in the grid while printing websites, to prevent a long list of texts.
    webcount = 0
    columncount = 0
    for web in websites:
        info_list.append((str(web[0]), web[1], web[7]))
        id_list.append(str(web[0]))

    for info_id, info_name, info_type in info_list:
        # Creates a text label for it.
        websites_rbutton = Radiobutton(ask_user_frame, text = "[" + info_id + "] " + info_name + " -- Type: " + info_type, variable=chosen_id, value=info_id, cursor="hand2")
        # Adds it to ask_user_frame Frame,and the row and column are adjusted in a way to prevent a one column long list.
        websites_rbutton.grid(row=webcount, column=columncount)
        webcount = webcount + 1
        # If webcounts exceeds 8, it resets webcount to 0 and increases columncount by 1.
        if webcount > 8:
            columncount = columncount + 1
            webcount = 0

    get_types = cur.execute("SELECT * FROM Types")

    type_count = 0
    type_row_count = 10
    type_column_count = 0

    for type in get_types:
        type_name = type[1]

        if type_name != "all":
            type_btns = Button(ask_user_frame, text=type[1] + " sites", command=lambda type_name=type_name: process_chosen_input(type_name), padx=20, pady=20, bg="#F9F1F0", bd=0.5, cursor="hand2")
            type_btns.grid(row=type_row_count, column=type_column_count, pady=30)
            type_count = type_count + 1
            type_column_count = type_column_count + 1
            types_list.append(type[1])

            if type_count > 3:
                type_row_count = type_row_count + 1
                type_column_count = 0
                type_count = 0

    user_choice_btn = Button(ask_user_frame, image=arrow_forward_img, command=lambda: process_chosen_input( chosen_id.get()), pady=10, padx=10, cursor="hand2")
    user_choice_btn.grid(row=11, column=3, pady=5)



beginProgram(False)
root.mainloop()