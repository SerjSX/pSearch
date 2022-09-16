import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import json

# Sites list in JSON. Originally had it in a separate file but that caused issues.
sites_json = ''' [
    {
        "id": "1",
        "name": "FileCR",
        "link": "https://filecr.com/",
        "slink": "https://filecr.com/?s=",
        "skey1": "div",
        "skey2": "class",
        "skey3": "product-info",
        "type": ["software", "android"],
        "mainlink": "yes"
    },
    {
        "id": "2",
        "name": "monkrus",
        "link": "https://w14.monkrus.ws/",
        "slink": "https://w14.monkrus.ws/search?q=",
        "skey1": "h2",
        "skey2": "class",
        "skey3": "entry-title",
        "type": ["software"],
        "mainlink": "yes"
    },
    {
        "id": "3",
        "name": "FitGirl Repacks",
        "link": "https://fitgirl-repacks.site/",
        "slink": "https://fitgirl-repacks.site/?s=",
        "skey1": "h1",
        "skey2": "class",
        "skey3": "entry-title",
        "type": ["game"],
        "mainlink": "yes"
    },
    {
        "id": "4",
        "name": "FTUApps",
        "link": "https://ftuapps.dev/",
        "slink": "https://ftuapps.dev/?s=",
        "skey1": "h2",
        "skey2": "class",
        "skey3": "entry-title",
        "type": ["software"],
        "mainlink": "yes"
    },
    {
        "id": "5",
        "name": "VSTorrent",
        "link": "https://vstorrent.org/",
        "slink": "https://vstorrent.org/?s=",
        "skey1": "h2",
        "skey2": "class",
        "skey3": "entry-title",
        "type": ["software"], 
        "mainlink": "yes"
    },    
    {
        "id": "6",
        "name": "1337x",
        "link": "https://1337x.to",
        "slink": "https://1337x.to/search/",
        "skey1": "a",
        "skey2": "null",
        "skey3": "null",
        "type": ["software", "game", "android", "movieseries"],
        "mainlink": "no"
    },    
    {
        "id": "7",
        "name": "GOG Games",
        "link": "https://gog-games.com/",
        "slink": "https://gog-games.com/search/",
        "skey1": "a",
        "skey2": "class",
        "skey3": "block",
        "type": ["game"],
        "mainlink": "no"
    },    
    {
        "id": "8",
        "name": "STEAMRIP",
        "link": "https://steamrip.com/",
        "slink": "https://steamrip.com/?s=",
        "skey1": "div",
        "skey2": "class",
        "skey3": "thumb-content",
        "type": ["game"],
        "mainlink": "yes"
    },
    {
        "id": "9",
        "name": "FlsAudio",
        "link": "https://flsaudio.com/new/",
        "slink": "https://flsaudio.com/new/?s=",
        "skey1": "h2",
        "skey2": "null",
        "skey3": "null",
        "type": ["software"],
        "mainlink": "yes"
    },
    {
        "id": "10",
        "name": "revdl",
        "link": "https://www.revdl.com/",
        "slink": "https://www.revdl.com/?s=",
        "skey1": "h3",
        "skey2": "class",
        "skey3": "post-title entry-title",
        "type": ["android"],
        "mainlink": "yes"   
    },
    {
        "id": "11",
        "name": "APKMB",
        "link": "https://apkmb.com/",
        "slink": "https://apkmb.com/?s=",
        "skey1": "div",
        "skey2": "class",
        "skey3": "bloque-app",
        "type": ["android"],
        "mainlink": "yes"
    },
    {
        "id": "12",
        "name": "scnlog",
        "link": "https://scnlog.me/",
        "slink": "https://scnlog.me/search/",
        "skey1": "div",
        "skey2": "class",
        "skey3": "title",
        "type": ["movieseries"],
        "mainlink": "yes"
    },
    {
        "id": "13",
        "name": "RELEASE BB",
        "link": "http://rlsbb.ru/",
        "slink": "https://search.rlsbb.ru/?s=",
        "skey1": "h1",
        "skey2": "class",
        "skey3": "entry-title",
        "type": ["movieseries"],
        "mainlink": "yes"
    },
    {
        "id": "14",
        "name": "downloadly",
        "link": "https://downloadly.ir/",
        "slink": "https://downloadly.ir/?s=",
        "skey1": "h2",
        "skey2": "class",
        "skey3": "w-post-elm",
        "type": ["software"],
        "mainlink": "yes"
    },
    {
        "id": "15",
        "name": "yasdl",
        "link": "https://www.yasdl.com/",
        "slink": "https://www.yasdl.com/?s=",
        "skey1": "h2",
        "skey2": "class",
        "skey3": "col",
        "type": ["software"],
        "mainlink": "yes"
    }
]'''

sites = json.loads(sites_json)

# Used as a header when requesting a website
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

# List for best results
bestResults = list()

# allLinks for appending all links at the end 
allLinks = list()

# generalMethod(nameInput,site_id) is the main function that searching process works in
def generalMethod(nameInput, site_id, chosen_type, main_link):
    # These variables below are for the information necessary for the searching process.
    # siteLink has the normal link of the website, useful when the grabbed URL doesn't start with the
    # website URL, so we can just add it easily.
    # siteSLink has the search URL. 
    # siteKey1-2-3 are used for grabbing the content from the website, which afterwards the links would
    # be shown from.
    siteLink = None
    siteSLink = None
    siteKey1 = None
    siteKey2 = None
    siteKey3 = None

    # for each website in the JSON file...
    for site in sites:
        # If the website from the file matches the user's inserted option...
        if site["id"] == site_id:
            # Sets its information to the appropriate variables.
            siteSLink = site["slink"]
            siteLink = site["link"]
            siteKey1 = site["skey1"]
            siteKey2 = site["skey2"]
            siteKey3 = site["skey3"]

    # resultLinks used for appending links from the results.
    resultLinks = list()

    # If it starts with https://1337x.to then quote it with %20 (space), this is unique for this site 
    # because of its web structure.
    if siteLink.startswith("https://1337x.to"):
        # If chosen_type is Android, add the keyword "android" at the end for accurate results.
        if chosen_type == "android":
            nameInputFixed = urllib.parse.quote(nameInput + " android")
            # Connect the url with the software name the user put at the beginning
            searchUrl = siteSLink + nameInputFixed + "/1/"
        else:
            nameInputFixed = urllib.parse.quote(nameInput)
            # Connect the url with the software name the user put at the beginning
            searchUrl = siteSLink + nameInputFixed + "/1/"
    # If the site is FileCR and the chosen type is Android, then specifically search it in 
    # the android section for accurate results.
    elif site_id == "1" and chosen_type == "android":
        searchUrl = siteSLink + urllib.parse.quote_plus(nameInput) + "&subcat_filter=&category-type=23"
    # If it doesn't starts with https://1337x.to/ then quote it with + (it replaces space with +), this is
    # the default method as most sites work this way.
    else:      
        nameInputFixed = urllib.parse.quote_plus(nameInput)
        # Connect the url with the software name the user put at the beginning
        searchUrl = siteSLink + nameInputFixed

    # Inform the user where and what it's searching. 
    print("\nSearching", nameInput, "at", searchUrl)

    # Send a request to connect to the site with the header.
    req = urllib.request.Request(url=searchUrl, headers=header) 

    # Open the URL to read        
    html = urllib.request.urlopen(req).read()
    
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
        
    # Souping elements according to the chosen software. Some work the same way so they have
    # the same souping method.
    # If the siteKey2-3 aren't 'null', then use the default method (specific class)
    if siteKey2 != "null" and siteKey3 != "null":
        tags = soup(siteKey1, {siteKey2: siteKey3})
    # If it is null, then this is done on purpose as the websites have special conditions, for example
    # 1337x and gog-games. Explained further afterwards.
    else:
        # soups without a specific class, the siteKey1 is most probably "a".
        tags = soup(siteKey1)
        
    # For each tag in tags...
    for tag in tags:
        # Find the "a" / links
        links = tag.find('a')

        # If it didn't result "None"...
        if links != None:
            # Get the href (link) 
            mainLinkA = links.get("href")
            # If it isn't None...
            if mainLinkA != None:
                # If it doesn't start with the following links... (to prevent unneccessary links)
                if not mainLinkA.startswith("https://w14.monkrus.ws/search/label/") or not mainLinkA.startswith("https://w14.monkrus.ws/search?") or mainLinkA != "https://w14.monkrus.ws/":
                    # If the website chosen is 8, append it with the link. Some sites don't include the primary URL within 
                    # their href, so the program adds it. This is a special conditon for site 8.
                    if main_link == "no":
                        resultLinks.append(siteLink + mainLinkA)
                    # If not, just append as it is. This is the default for most.
                    else: 
                        resultLinks.append(mainLinkA)
                    
        # If Links resulted None, then the following have special conditions. 
        elif links == None:
            # Get the href from the tag, because at first we grabbed the "a" directly.
            mainLinkB = tag.get("href")
            # If it isn't None...
            if mainLinkB != None:
                # If it starts with /torrent and the url is 1337x, then append with the URL at first.
                # similar to the steamrip one above.
                # This is to prevent others being shown and the site's structure doesn't include the
                # primary URL in the beginning, so we add it first.
                if mainLinkB.startswith("/torrent"):
                    resultLinks.append(siteLink + mainLinkB)          
                # If it starts with /game and the url is gog-games, then append with the URL at first.              
                elif mainLinkB.startswith("/game") and siteLink.startswith("https://gog-games.com"):
                    resultLinks.append(siteLink + mainLinkB)                     

    # If the length of resultLinks is greater than 0...
    if len(resultLinks) > 0:
        # Append the link to allLinks list.
        for link in resultLinks:
            allLinks.append(link)
            
        # append the first link to the bestResults list.
        bestResults.append(resultLinks[0])
    # If it's less than 0, most probably 0 itself, print that the URL showed no results.
    else:
        print("No results -", searchUrl)


# Checks the chosen number the user input and operates accordingly.
def checkChosenNum(chosenNum,nameInput):
    # If user chose 0 or empty...
    if chosenNum == '0' or chosenNum == '':
        # for each site in sites
        for site in sites:
            # Activate the generalMethod function with forwarding the site's ID.
            generalMethod(nameInput, site["id"], 0, site["mainlink"])
    
    # If user chose -1...
    elif chosenNum == "-1":
        # for each site in sites
        for site in sites:
            # if the site's type is software OR duo (duo means the site results both software
            # and games)...
            if "software" in site["type"]:      
                # Run generalMethod with forwarding its site["id"]  
                generalMethod(nameInput, site["id"], 0, site["mainlink"])

    # If user chose -2... 
    elif chosenNum == "-2":
        # for each site in sites
        for site in sites:
            # If the site's type is game or duo...
            if "game" in site["type"]:     
                # Run generalMethod with forwarding its site["id"]     
                generalMethod(nameInput, site["id"], 0, site["mainlink"])

    elif chosenNum == "-3":
        for site in sites:
            if "android" in site["type"]:
                generalMethod(nameInput, site["id"], "android", site["mainlink"])
            
    elif chosenNum == "-4":
        for site in sites:
            if "movieseries" in site["type"]:
                generalMethod(nameInput, site["id"], 0, site["mainlink"])

    # This runs as the default method, which is when the user types a specific number
    # for a specific software.
    else:
        site_chosen = sites[int(chosenNum)-1]
        generalMethod(nameInput, site_chosen["id"], 0, site_chosen["mainlink"])    
    
    # At the end, it prints the results if the length of allLinks is greater than 0
    if len(allLinks) > 0:
        print("Found", len(allLinks), "results:")
        for link in allLinks:
            print(link)
        
        # Also prints Best Results.
        print("\n-- Best results --")
        for link in bestResults:
            print(link)

    # If it isn't greater than 0, it says No Results
    else:
        print("\nNo results")

    searchAsk = input("\nSearch again? [Y/n]")
    if searchAsk == "" or searchAsk == "Y" or searchAsk == "y":  
        allLinks.clear()
        bestResults.clear()
        askUser()
    else: 
        print("Quitting program...")
        quit()

# Asks user to insert inputs, the beginning of the program.
def askUser():
    # Shows available options to search from
    print("Available websites:")
    for site in sites:
        print("[" + site['id'] + "] " + site['name'], site['type'])
    print("\n[0/empty] All Sites")
    print("[-1] All Software Sites")
    print("[-2] All Game Sites")
    print("[-3] All Android Sites")
    print("[-4] All Movie/Series Sites")
    print("[exit] Quits the program\n")

    chosenNum = input("Where do you want to search? Enter number: ")

    # If the user didn't type exit, ask the software's name. You can type "exit" to quit the program
    if chosenNum != 'exit':
        nameInput = input("Enter Software Name - ")
        # If the user didn't type exit, run checkChosenNum.
        if nameInput != 'exit':
            checkChosenNum(chosenNum,nameInput)
        else:
            print("Exiting Program...")
            exit()
    else:
        print("Exiting Program...")
        exit()

# Welcome message, beginning of program.
print("\n ---> Welcome to pSearch - Python based Piracy searching tool <--- \n")
askUser()