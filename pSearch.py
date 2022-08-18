import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import json

# Opens the json file which includes the supported sites and its information.
with open('sites.json', 'r') as sites_file:
    # Loads it, sites will be used for representation.
    sites = json.load(sites_file)

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
def generalMethod(nameInput, site_id):
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

    # If it starts with https://1337x.to/ then quote it with %20 (space), this is unique for this site 
    # because of its web structure.
    if siteLink.startswith("https://1337x.to/"):
        nameInputFixed = urllib.parse.quote(nameInput)
        # Connect the url with the software name the user put at the beginning
        searchUrl = siteSLink + nameInputFixed + "/1/"
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
                    if site_id == "8":
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
                if mainLinkB.startswith("/torrent") and siteLink.startswith("https://1337x"):
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
            generalMethod(nameInput, site["id"])
    
    # If user chose -1...
    elif chosenNum == "-1":
        # for each site in sites
        for site in sites:
            # if the site's type is software OR duo (duo means the site results both software
            # and games)...
            if site["type"] == "software" or site["type"] == "duo":      
                # Run generalMethod with forwarding its site["id"]  
                generalMethod(nameInput, site["id"])

    # If user chose -2... 
    elif chosenNum == "-2":
        # for each site in sites
        for site in sites:
            # If the site's type is game or duo...
            if site["type"] == "game" or site["type"] == "duo":     
                # Run generalMethod with forwarding its site["id"]     
                generalMethod(nameInput, site["id"])

    # This runs as the default method, which is when the user types a specific number
    # for a specific software.
    else:
        site_chosen = sites[int(chosenNum)-1]
        generalMethod(nameInput, site_chosen["id"])    
    
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

# Asks user to insert inputs, the beginning of the program.
def askUser():
    # Shows available options to search from
    print("Available websites:")
    for site in sites:
        print("[" + site['id'] + "] " + site['name'])
    print("[0/empty] All Sites")
    print("[-1] All Software Sites")
    print("[-2] All Game Sites")
    print("[exit/quit] Quits the program")

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