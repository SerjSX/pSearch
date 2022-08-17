import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

# Used as a header when requesting a website
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

# Website library with names
website_library = {
    "1": "FileCR", "2": "monkrus", "3" : "FitGirl Repacks",
    "4": "FTUApps", "5": "VSTorrent", "6": "1337x", "7": "GOG Games",
    "8": "STEAMRIP"
}

# Direct websites used for searching
direct_websites = [
    "https://filecr.com/?s=", "https://w14.monkrus.ws/search?q=",
    "https://fitgirl-repacks.site/?s=", "https://ftuapps.dev/?s=",
    "https://vstorrent.org/?s=", "https://1337x.to/search/", 
    "https://gog-games.com/search/", "https://steamrip.com/?s="
]

# List and default count for best results
bestResults = list()

# allLinks for appending all links at the end 
allLinks = list()

# generalMethod(website,nameInput) is the main function that searching process works in
def generalMethod(website,nameInput):
    bestPos = -1
    # generalUrls is for appending the links from the direct_websites variable in order to search with those
    # URLs only.
    generalUrls = list()

    # tagSoups list is where the contents get pushed in order to extract the links from them afterwards.
    tagSoups = list()

    # Appends the link according to the chosen website to the generalUrls list
    try:   
        generalUrls.append(direct_websites[int(website)-1])
    except:
        print("Not a valid input, quitting program.")
        exit()

    # Starts the process of extracting and appending the links (results)
    # For link in general Urls...
    for url in generalUrls:
        # generalLinks used for appending links within the generalMethod() function
        generalLinks = list()

        # If it starts with https://1337x.to/ then quote it with %20 (space), this is unique for this site 
        # because of its web structure.
        if url.startswith("https://1337x.to/"):
            nameInputFixed = urllib.parse.quote(nameInput)
            # Connect the url with the software name the user put at the beginning
            searchUrl = url + nameInputFixed + "/1/"
        # If it doesn't starts with https://1337x.to/ then quote it with + (it replaces space with +), this is
        # the default method as most sites work this way.
        else:      
            nameInputFixed = urllib.parse.quote_plus(nameInput)
            # Connect the url with the software name the user put at the beginning
            searchUrl = url + nameInputFixed

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
        if website == "1":
            tags = soup('div', {'class': 'product-info'})
            tagSoups.append(tags)
        elif website == "2" or website == "4" or website == "5":
            tags = soup('h2', {'class': 'entry-title'})
            tagSoups.append(tags)
        elif website == "3":
            tags = soup('h1', {'class': 'entry-title'})
            tagSoups.append(tags)
        elif website == "6":
            tags = soup('a')
            tagSoups.append(tags)
        elif website == "7":
            tags = soup('a', {'class': 'block'})
            tagSoups.append(tags)
        elif website == "8":
            tags = soup('div', {'class': 'thumb-content'})
            tagSoups.append(tags)
        
        # For each tag in tagSoups
        for tagS in tagSoups:
            # for each tag WITHIN the tagS (tags from tagSoups)
            for tag in tagS:
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
                            # their href, so the program adds it.
                            if website == "8":
                                generalLinks.append("https://steamrip/" + mainLinkA)
                            # If not, just append as it is. This is the default for most.
                            else: 
                                generalLinks.append(mainLinkA)
                    
                # If Links resulted None, then the following have special conditions. 
                elif links == None:
                    # Get the href from the tag, because at first we grabbed the "a" directly.
                    mainLinkB = tag.get("href")
                    # If it isn't None...
                    if mainLinkB != None:
                        # If it starts with /torrent and the url is 1337x, then append with the URL at first.
                        # similar to the steamrip one above. Will implement a better, automatic method for this.
                        if mainLinkB.startswith("/torrent") and url.startswith("https://1337x"):
                            generalLinks.append("https://1337x" + mainLinkB)          
                        # If it starts with /game and the url is gog-games, then append with the URL at first.              
                        elif mainLinkB.startswith("/game") and url.startswith("https://gog-games.com"):
                            generalLinks.append("https://gog-games.com" + mainLinkB)                     

        # If the length of generalLinks is greater than 0...
        if len(generalLinks) > 0:
            # Append the link to allLinks list.
            for link in generalLinks:
                allLinks.append(link)
            
            # append the first link to the bestResults list.
            bestResults.append(generalLinks[0])
        # Print that the URL showed no results.
        else:
            print("No results -", searchUrl)


# Checks the chosen number the user input and operates accordingly.
def checkChosenNum(chosenNum,nameInput):
    if chosenNum == '0' or chosenNum == '':
        generalMethod("1",nameInput) # FileCR
        generalMethod("2",nameInput) # monkrus
        generalMethod("3",nameInput) # Fitgirl Repacks
        generalMethod("4",nameInput) # FTUApps
        generalMethod("5",nameInput) # VSTorrent
        generalMethod("6",nameInput) # 1337x
        generalMethod("7",nameInput) # GOG Games
        generalMethod("8",nameInput) # STEAMRIP
    
    elif chosenNum == "-1":
        generalMethod("1",nameInput) # FileCR
        generalMethod("2",nameInput) # monkrus
        generalMethod("4",nameInput) # FTUApps
        generalMethod("5",nameInput) # VSTorrent
        generalMethod("6",nameInput) # 1337x  

    elif chosenNum == "-2":
        generalMethod("3",nameInput) # Fitgirl Repacks
        generalMethod("6",nameInput) # 1337x
        generalMethod("7",nameInput) # GOG Games
        generalMethod("8",nameInput) # STEAMRIP

    else:
        generalMethod(chosenNum,nameInput)    
    
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
    for webnum in website_library:
        print("[", webnum, "] ", website_library[webnum])
    print("[0/empty] All Sites")
    print("[-1] All Software Sites")
    print("[-2] All Game Sites")
    print("[exit/quit] Quits the program")

    chosenNum = input("Where do you want to search? Enter number: ")

    if chosenNum != 'exit':
        nameInput = input("Enter Software Name - ")
        if nameInput != 'exit':
            checkChosenNum(chosenNum,nameInput)
        else:
            print("Exiting Program...")
            exit()
    else:
        print("Exiting Program...")
        exit()

print("\n ---> Welcome to pSearch - Python based Piracy searching tool <--- \n")
askUser()