import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import bs4.element
import fnmatch

header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

website_library = {
    "1": "FileCR", "2": "monkrus", "3": "Pirated-Games", "4" : "FitGirl Repacks",
    "5": "FTUApps", "6": "VSTorrent", "7": "1337x", "8": "GOG Games",
    "9": "STEAMRIP"
}

direct_websites = [
    "https://filecr.com/?s=", "https://w14.monkrus.ws/search?q=",
    "https://pirated-games.com/?s=", "https://fitgirl-repacks.site/?s=",
    "https://ftuapps.dev/?s=", "https://vstorrent.org/?s=",
    "https://1337x.to/search/", "https://gog-games.com/search/",
    "https://steamrip.com/?s="
]

static_websites = [
    "https://filecr.com/", "https://w14.monkrus.ws/",
    "https://pirated-games.com/", "https://fitgirl-repacks.site/",
    "https://ftuapps.dev/", "https://vstorrent.org/",
    "https://1337x.to/", "https://gog-games.com/",
    "https://steamrip.com/"    
]

bestResults = list()

allLinks = list()
rmmLinks = list()
generalLinks = list()

# FileCR (1) Monkrus (2), Pirated Games (3), FitGirl Repacks (4), FTUApps (5), VSTorrent (6), 1337x (7)
def generalMethod(website):
    generalUrls = list()
    tagSoups = list()

    generalUrls.append(direct_websites[int(website)-1])

    for url in generalUrls:
        if url.startswith("https://1337x.to/"):
            nameInputFixed = urllib.parse.quote(nameInput)
            searchUrl = url + nameInputFixed + "/1/"
        else:      
            nameInputFixed = urllib.parse.quote_plus(nameInput)
            searchUrl = url + nameInputFixed

        print("\nSearching", nameInput, "at", searchUrl)

        generalcount = 0
        req = urllib.request.Request(url=searchUrl, headers=header) 

        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        if website == "1":
            tags = soup('div', {'class': 'product-info'})
            tagSoups.append(tags)
        elif website == "2" or website == "5" or website == "6":
            tags = soup('h2', {'class': 'entry-title'})
            tagSoups.append(tags)
        elif website == "3":
            tags = soup('h3', {'class': 'h4'})
            tagSoups.append(tags)
        elif website == "4":
            tags = soup('h1', {'class': 'entry-title'})
            tagSoups.append(tags)
        elif website == "7":
            tags = soup('a')
            tagSoups.append(tags)
        elif website == "8":
            tags = soup('a', {'class': 'block'})
            tagSoups.append(tags)
        elif website == "9":
            tags = soup('div', {'class': 'thumb-content'})
            tagSoups.append(tags)
        else:
            print("Not a valid option.")
            exit()
        
        for tagS in tagSoups:
            for tag in tagS:
                links = tag.find('a')
                if links != None:
                    mainLinkA = links.get("href")
                    if mainLinkA != None:
                        if not mainLinkA.startswith("https://w14.monkrus.ws/search/label/") or not mainLinkA.startswith("https://w14.monkrus.ws/search?") or mainLinkA != "https://w14.monkrus.ws/":
                            if website == "9":
                                generalLinks.append("https://steamrip/" + mainLinkA)
                            else: 
                                generalLinks.append(mainLinkA)
                    
                elif links == None:
                    mainLinkB = tag.get("href")
                    if mainLinkB != None:
                        if mainLinkB.startswith("/torrent") and url.startswith("https://1337x"):
                            generalLinks.append("https://1337x" + mainLinkB)                        
                        elif mainLinkB.startswith("/game") and url.startswith("https://gog-games.com"):
                            generalLinks.append("https://gog-games.com" + mainLinkB)                     

    noduplLinks = list(dict.fromkeys(generalLinks))
    for link in noduplLinks:
        allLinks.append(link)



def checkChosenNum(chosenNum):
    if chosenNum == '0' or chosenNum == '':
        generalMethod("1") # FileCR
        generalMethod("2") # monkrus
        generalMethod("3") # Pirated-Games
        generalMethod("4") # Fitgirl Repacks
        generalMethod("5") # FTUApps
        generalMethod("6") # VSTorrent
        generalMethod("7") # 1337x
        generalMethod("8") # GOG Games
        generalMethod("9") # STEAMRIP

    
    elif chosenNum == "-1":
        generalMethod("1") # FileCR
        generalMethod("2") # monkrus
        generalMethod("5") # FTUApps
        generalMethod("6") # VSTorrent
        generalMethod("7") # 1337x  

    elif chosenNum == "-2":
        generalMethod("3") # Pirated-Games
        generalMethod("4") # Fitgirl Repacks
        generalMethod("7") # 1337x
        generalMethod("8") # GOG Games
        generalMethod("9") # STEAMRIP

    else:
        generalMethod(chosenNum)    
    
    noduplLinks = list(dict.fromkeys(allLinks))
    if len(noduplLinks) > 0:
        print("Found", len(noduplLinks), "results:")
        for link in noduplLinks:
            print(link)
    else:
        print("No results")

def askUser():
    nameInput = input("Enter Software Name - ")

    print("Available websites:")
    for webnum in website_library:
        print("[", webnum, "] ", website_library[webnum])
    print("[0] All Sites")
    print("[-1] All Software Sites")
    print("[-2] All Game Sites")

    chosenNum = input("Where do you want to search? Enter number: ")
    checkChosenNum(chosenNum)

askUser()