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
    "1": "FileCR - https://filecr.com/?s=",
    "2": "monkrus - https://w14.monkrus.ws/search?q=",
    "3": "FTUApps - https://ftuapps.dev/?s=",
    "4": "VSTorrent - https://vstorrent.org/?s="
}

direct_websites = [
    "https://filecr.com/?s=", "https://w14.monkrus.ws/search?q=",
    "https://ftuapps.dev/?s=", "https://vstorrent.org/?s="
]

nameInput = input("Enter Software Name - ")
nameInputFixed = nameInput.replace(' ', '+')
print(nameInputFixed)

print("Available websites:")
for webnum in website_library:
    print("[", webnum, "] ", website_library[webnum])

chosenNum = input("Where do you want to search? Enter number (Default (0) = all): ")

bestResults = list()

fcrLinks = list()
monkrusLinks = list()
rmmLinks = list()

def fileCR():
    fcount = 0
    linkSplit = website_library['1'].split('-')
    webLink = linkSplit[1].strip()

    searchUrl = webLink + nameInputFixed
    print("Searching", nameInput, "at", searchUrl)

    req = urllib.request.Request(url=searchUrl, headers=header) 
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    for tag in tags:
        checkValue = tag.get('class', None)
        if checkValue != None:
            if checkValue[0] == 'product-icon':
                getLink = tag.get("href", None)
                fcrLinks.append(getLink)
                fcount = fcount + 1

                if fcount == 1:
                    bestResults.append(getLink)

    if fcount == 0:
        print("No results")
    else:
        print(fcount, "results found from FileCR:")
        for link in fcrLinks:
            print(link)

def monkrus():
    mcount = 0
    linkSplit = website_library['2'].split('-')
    webLink = linkSplit[1].strip()

    searchUrl = webLink + nameInputFixed
    print("Searching", nameInput, "at", searchUrl)

    mcount = 0
    req = urllib.request.Request(url=searchUrl, headers=header) 
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('h2', {'class': 'post-title entry-title'})
    for tag in tags:
        links = tag.find('a')
        mainLink = links.get("href")
        if links != None:
            if mainLink.startswith('https://w14.monkrus.ws') and not mainLink.startswith("https://w14.monkrus.ws/search/label/") and not mainLink.startswith("https://w14.monkrus.ws/search?") and mainLink != "https://w14.monkrus.ws/":
                monkrusLinks.append(mainLink)
                mcount = mcount + 1
                if mcount == 1:
                    bestResults.append(mainLink)

    if mcount == 0:
        print("No results")
    else:
        print(mcount, "results found from monkrus:")
        for link in monkrusLinks:
            print(link)

def rmMethod(website):
    generalUrls = list()
    if website == "3":
        generalUrls.append(direct_websites[2])
    elif website == "4":
        generalUrls.append(direct_websites[3])
    else:
        for value in direct_websites[2:4]:
            generalUrls.append(value)
    print(generalUrls)

    for url in generalUrls:
        searchUrl = url + nameInputFixed
        print("Searching", nameInput, "at", searchUrl)

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
    else:
        print("\n Results:")
        for link in rmmLinks:
            print(link)

def checkChosenNum():
    if chosenNum == '0' or '':
        fileCR()
        print("\n")
        monkrus()
        print("\n")
        rmMethod(chosenNum)

    elif chosenNum == "1":
        fileCR()

    elif chosenNum == "2":
        monkrus()

    elif chosenNum == "3" or chosenNum == "4":
        rmMethod(chosenNum)        

    print("\n Best Results:")
    for link in bestResults:
        print(link)

checkChosenNum()