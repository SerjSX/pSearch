import urllib.parse
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import os
import sqlite3
import sys
import base64
import traceback

# Grabs the directory name [BETA TESTING: to prevent file not found error]
path = os.path.dirname(os.path.abspath(__file__))

# Connects to the database file 
print("Running in online database.")
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

# ids_list is used in order to print the available options afterwards.
ids_list = ['', '0', '-1', '-2', '-3', '-4', '-5', '-6']

# Used as a header when requesting a website
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}

# List for best results
bestResults = {}

# allLinks for appending all links at the end
allLinks = {}


# onlineMethod(name_input,site_id) is the main function that searching process works in
def online_method(name_input, site_id, chosen_type, main_link):
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

    # for each website in the JSON file...
    for web in websites:
        # If the website from the file matches the user's inserted option...
        if web[0] == site_id:
            # Sets its information to the appropriate variables.
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
            name_input_fixed = urllib.parse.quote(name_input + " android")
            # Connect the url with the software name the user put at the beginning
            search_url = site_slink + name_input_fixed + "/1/"
        else:
            name_input_fixed = urllib.parse.quote(name_input)
            # Connect the url with the software name the user put at the beginning
            search_url = site_slink + name_input_fixed + "/1/"
    # If the site is FileCR and the chosen type is Android, then specifically search it in
    # the android section for accurate results.
    elif site_id == "1" and chosen_type == "android":
        search_url = site_slink + urllib.parse.quote_plus(name_input) + "&subcat_filter=&category-type=23"
    # If it doesn't start with https://1337x.to/ then quote it with + (it replaces space with +), this is
    # the default method as most sites work this way.
    else:
        name_input_fixed = urllib.parse.quote_plus(name_input)
        # Connect the url with the software name the user put at the beginning
        search_url = site_slink + name_input_fixed

    # Inform the user where and what it's searching.
    print("\nSearching", name_input, "at", search_url)

    # Send a request to connect to the site with the header.
    req = urllib.request.Request(url=search_url, headers=header)

    # Try to open the URL to read
    try:
        page_connect = urllib.request.urlopen(req)
        page_code = page_connect.getcode()
    except urllib.error.HTTPError:
        print("\n", traceback.format_exc())
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

        # If the length of result_links is greater than 0...
        if len(result_links) > 0:
            br_bool = False
            # Append the link to allLinks list.
            for link in result_links.items():
                allLinks[link[0]] = link[1]

                if br_bool is False:
                    # append the first link to the bestResults list.
                    bestResults[link[0]] = link[1]
                    br_bool = True
        # If it's less than 0, most probably 0 itself, print that the URL showed no results.
        else:
            print("No results -", search_url)

    else:
        print("This site resulted an ERROR as shown above. Visit the site manually.")
        print("Cannot proceed if HTTP isn't 200. Most probably there's protection on the site.")

# Checks the chosen number the user input and operates accordingly.
def check_chosen_num(chosen_num, name_input):
    # If the user chose Online database...
    # If user chose 0 or empty...
    if chosen_num == '0' or chosen_num == '':
        # for each site in sites
        for site in websites:
            # Activate the onlineMethod function with forwarding the site's ID.
            online_method(name_input, site[0], 0, site[8])

    # If user chose -1...
    elif chosen_num == "-1":
        # for each site in sites
        for site in websites:
            # if the site's type is software OR duo (duo means the site results both software
            # and games)...
            if "software" in site[7] or "all" in site[7]:
                # Run onlineMethod with forwarding its site["id"]
                online_method(name_input, site[0], 0, site[8])

    # If user chose -2...
    elif chosen_num == "-2":
        # for each site in sites
        for site in websites:
            # If the site's type is game or duo...
            if "game" in site[7] or "all" in site[7]:
                # Run onlineMethod with forwarding its site["id"]
                online_method(name_input, site[0], 0, site[8])

    elif chosen_num == "-3":
        for site in websites:
            if "android" in site[7] or "all" in site[7]:
                online_method(name_input, site[0], "android", site[8])

    elif chosen_num == "-4":
        for site in websites:
            if "movieseries" in site[7] or "all" in site[7]:
                online_method(name_input, site[0], 0, site[8])

    elif chosen_num == "-5":
        for site in websites:
            if "courses" in site[7] or "all" in site[7]:
                online_method(name_input, site[0], 0, site[8])

    elif chosen_num == "-6":
        for site in websites:
            if "ebooks" in site[7] or "all" in site[7]:
                online_method(name_input, site[0], 0, site[8])

    # This runs as the default method, which is when the user types a specific number
    # for a specific software.
    else:
        # Forward it to the online_method function
        for web in websites:
            if web[0] == int(chosen_num):
                online_method(name_input, web[0], 0, web[8])

    # At the end, it prints the results if the length of allLinks is greater than 0
    if len(allLinks) > 0 or len(bestResults) > 0:
        if len(allLinks) > 0:
            print("Found", len(allLinks), "results:")
            for link in allLinks.items():
                print(link[0].strip(), "\n", link[1].strip(), "\n")

        # Also prints Best Results.
        print("\n\n-- Best results --")
        for link in bestResults.items():
            print(link[0].strip(), "\n", link[1].strip(), "\n")

    # If it isn't greater than 0, it says No Results
    else:
        print("\nNo results")

    search_ask = input("\nSearch again? [Y/n]")
    if search_ask == "" or search_ask == "Y" or search_ask == "y":
        allLinks.clear()
        bestResults.clear()
        ask_user()
    else:
        print("Quitting program...")
        cur.close()
        sys.exit()


# Asks user to insert inputs, the beginning of the program.
def ask_user():
    # Shows available options to search from
    print("Available websites:")
    for web in websites:
        print("[", web[0], "] " + web[1], " -- Type: " + web[7])
        ids_list.append(str(web[0]))

    print("\n[0/empty] All Sites")
    print("[-1] All Software Sites")
    print("[-2] All Game Sites")
    print("[-3] All Android Sites")
    print("[-4] All Movies and Series Sites")
    print("[-5] All Courses Sites")
    print("[-6] All eBook Sites")
    print("[exit] Quits the program\n")

    chosen_num = input("Where do you want to search? Enter number: ").strip()

    # if the chosen_num is in ids_list...
    if chosen_num in ids_list:
        # If the user didn't type exit, ask the software's name. You can type "exit" to quit the program
        name_input = input("Enter Software Name - ")
        # If the user didn't type exit, run check_chosen_num.
        if name_input != 'exit':
            # forward the chosen_num and name_input to the checking function.
            check_chosen_num(chosen_num, name_input)
        # if it is exit then quit the program.
        else:
            cur.close()
            sys.exit("Exiting Program...")

    # if it is exit then quit the program
    elif chosen_num == "exit":
        cur.close()
        sys.exit("Exiting Program...")

    # If the input is a valid number, say so and quit the program.
    else:
        cur.close()
        sys.exit("Not a valid number! Exiting Program...")


# Welcome message, beginning of program.
print("\n ---> Welcome to pSearch - Python based Piracy searching tool <--- \n")
ask_user()
