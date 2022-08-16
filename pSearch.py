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
    "1": "FileCR", "2": "monkrus", "3" : "FitGirl Repacks",
    "4": "FTUApps", "5": "VSTorrent", "6": "1337x", "7": "GOG Games",
    "8": "STEAMRIP"
}

direct_websites = [
    "https://filecr.com/?s=", "https://w14.monkrus.ws/search?q=",
    "https://fitgirl-repacks.site/?s=", "https://ftuapps.dev/?s=",
    "https://vstorrent.org/?s=", "https://1337x.to/search/", 
    "https://gog-games.com/search/", "https://steamrip.com/?s="
]

static_websites = [
    "https://filecr.com/", "https://w14.monkrus.ws/",
    "https://fitgirl-repacks.site/", "https://ftuapps.dev/",
    "https://vstorrent.org/", "https://1337x.to/", 
    "https://gog-games.com/", "https://steamrip.com/"    
]

bestResults = list()

allLinks = list()
rmmLinks = list()
generalLinks = list()

def generalMethod(website,nameInput):
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
                            if website == "8":
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
    checkChosenNum(chosenNum,nameInput)

askUser()