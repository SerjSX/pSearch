import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

website_library = {
    "1": "FileCR - https://filecr.com/?s=", "2": "monkrus - https://w14.monkrus.ws/search?q=",
    "3": "Pirated-Games - https://pirated-games.com/?s", "4": "FTUApps - https://ftuapps.dev/?s=", 
    "5": "VSTorrent - https://vstorrent.org/?s=",
}

direct_websites = [
    "https://filecr.com/?s=", "https://w14.monkrus.ws/search?q=",
    "https://pirated-games.com/?s=", "https://ftuapps.dev/?s=", 
    "https://vstorrent.org/?s=",
]

nameInput = input("Enter Software Name - ")
nameInputFixed = nameInput.replace(' ', '+')

print("Available websites:")
for webnum in website_library:
    print("[", webnum, "] ", website_library[webnum])
print("[-1] All Software Sites")
print("[-2] All Game Sites")

chosenNum = input("Where do you want to search? Enter number (Default (0) = all): ")

bestResults = list()

rmmLinks = list()
generalLinks = list()

# FileCR (1) Monkrus (2) and Pirated Games (3)
def generalMethod(website):
    generalUrls = list()
    tagSoups = list()


    if website == "1":
        generalUrls.append(direct_websites[0])
    elif website == "2":
        generalUrls.append(direct_websites[1])
    elif website == "3":
        generalUrls.append(direct_websites[2])
    else:
        for value in direct_websites[0:3]:
            generalUrls.append(value)

    oldPos = 0
    for url in generalUrls:
        searchUrl = url + nameInputFixed
        print("\nSearching", nameInput, "at", searchUrl)

        generalcount = 0
        req = urllib.request.Request(url=searchUrl, headers=header) 

        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        if website == "1":
            tags = soup('div', {'class': 'product-info'})
            tagSoups.append(tags)
        elif website == "2":
            tags = soup('h2', {'class': 'entry-title'})
            tagSoups.append(tags)
        elif website == "3":
            tags = soup('h3', {'class': 'cactus-post-title entry-title h4'})
            tagSoups.append(tags)
        else:
            tag1 = soup('div', {'class': 'product-info'})
            tagSoups.append(tag1)
            tag2 = soup('h2', {'class': 'entry-title'})
            tagSoups.append(tag2)
            tag3 = soup('h3', {'class': 'cactus-post-title entry-title h4'})
            tagSoups.append(tag3)
        
        for tagS in tagSoups:
            for tag in tagS:
                links = tag.find('a')
                mainLink = links.get("href")
                if links != None:
                    if mainLink.startswith('https://w14.monkrus.ws') or not mainLink.startswith("https://w14.monkrus.ws/search/label/") and not mainLink.startswith("https://w14.monkrus.ws/search?") and mainLink != "https://w14.monkrus.ws/":
                        generalLinks.append(mainLink)

        noduplLinks = list(dict.fromkeys(generalLinks))

        if len(noduplLinks) == 0:
            print("No results")
        else:        
            fullPos = len(noduplLinks)
            realfullPos = fullPos - 1
            if oldPos == 0:
                lastPos = fullPos - fullPos + 1
                oldPos = fullPos
            else:
                lastPos = oldPos + 1
                oldPos = fullPos
            bestResults.append(noduplLinks[lastPos-1])

# FTUApps (4) and VSTorrent (5)
def rmMethod(website):
    generalUrls = list()
    if website == "4":
        generalUrls.append(direct_websites[3])
    elif website == "5":
        generalUrls.append(direct_websites[4])
    else:
        for value in direct_websites[3:5]:
            generalUrls.append(value)

    for url in generalUrls:
        searchUrl = url + nameInputFixed
        print("\nSearching", nameInput, "at", searchUrl)

        rmmcount = 0
        req = urllib.request.Request(url=searchUrl, headers=header) 
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('a')
        for tag in tags:
            tagContent = tag.contents[0]
            if tagContent != None:
                if tagContent == "Read More »" or tagContent == "Read More":
                    getLink = tag.get('href', None)
                    rmmLinks.append(getLink)
                    rmmcount = rmmcount + 1
                    if rmmcount == 1:
                        bestResults.append(getLink)

    if rmmcount == 0:
        print("No results")

def checkChosenNum():
    if chosenNum == '0' or chosenNum == '':
        generalMethod(chosenNum)
        rmMethod(chosenNum)

    elif chosenNum == "1" or chosenNum == "2" or chosenNum == "3":
        generalMethod(chosenNum)

    elif chosenNum == "4" or chosenNum == "5":
        rmMethod(chosenNum)        
    
    elif chosenNum == "-1":
        generalMethod("2")
        rmMethodSoftware("0")

    elif chosenNum == "-2":
        generalMethod("3")

    noduplLinks = list(dict.fromkeys(generalLinks))

    print("\nAll Results:")
    for link in noduplLinks:
        print(link)

    print("\nBest Results:")
    for link in bestResults:
        print(link)

checkChosenNum()