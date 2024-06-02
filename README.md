![pSearch on version 1.6.7](https://i.ibb.co/7Q8BnnD/image.png)

<p align="center">
  <img src="https://img.shields.io/github/downloads/SerjSX/pSearch/total" alt="Downloads"/>
  <img src="https://img.shields.io/github/downloads/SerjSX/pSearch/latest/total" alt="Latest Downloads"/>
  <img src="https://img.shields.io/github/downloads/SerjSX/pSearch/latest/pSearch-windows-standalone.zip" alt="Latest Standalone Downloads"/>
  <img src="https://img.shields.io/github/downloads/SerjSX/pSearch/latest/pSearch-windows-onefile-standalone.zip" alt="Latest Onefile Downloads"/>
  <img src="https://img.shields.io/github/license/SerjSX/pSearch" alt="License"/>
  <img src="https://img.shields.io/github/languages/top/SerjSX/pSearch" alt="Top Language"/>
</p>


# pSearch
 Searching tool written in Python for Piracy related websites. You choose where you want to search, and the program does its own work and shows you the results. It is similar to normal search engines, however the program searches the site on-spot rather than having a database with different results.

~ If you see a terminal/command line opening when you run the program, don't worry about it! It's for showing errors, that way you and I can see the error easily (if there is one). 

## Three launching methods
|*Title*|**Source Code**|**Windows Standalone**|**Windows Onefile Standalone**|
|:-|:-|:-|:-|
|**Descripton**|Running pSearch from the source code requires BeautifulSoup and CustomTkinter. This is the fastest way you can run the program (if familiar with Python), as it isn't built in any way and it's just it.|This is a standalone build of the program meant for distribution in .exe form. The program is built with Nuitka. You may face errors, if you do so please let me know about them.|This is similar to the Windows Standalone method, but you won't see the other modules in the folder as they are embedded in the .exe file (that's why it's Onefile). There are two folders, "others" and "media", and two zip files, "bs4" and "customtkinter", in the package so the program would run in a correct way. The program unzips the zip files for module usage. Launching the program may take a long time with this method.|
|**Health**|*Runs Fast*|*Runs Fast*|*Runs Slow*|
|**Button Name on Site**|<a href="https://github.com/SerjSX/pSearch/releases/latest" alt="latest release">View Latest Release GitHub</a>|<a href="https://github.com/SerjSX/pSearch/releases/latest/download/pSearch-windows-standalone.zip" alt="download latest standalone exe">Download Latest .EXE for Windows</a>|<a href="https://github.com/SerjSX/pSearch/releases/latest/download/pSearch-windows-onefile-standalone.zip" alt="download latest onefile exe">Download Latest .EXE Onefile for Windows</a>|

***Source Code and Onefile seem to be efficient enough, because both extract customtkinter and bs4.zip. If you face errors let me know immediately about it. Version 1.6.4 will have console enabled, that way you can see the error from the command line and send it to me here or on Github Issues.***
&#x200B;

## Using the program
||**Description**|
|:-|:-|
|**Using site input box -** ***choosing where to search, has a smaller input in size in the program with the text "Enter site name here"***|You can either \[1\] type a site's name, the program checks if the site is in the database and proceeds with the search, \[2\] choose a site from the dropdown options shown by clicking the upside down arrow next to the site input box, \[3\] click one of the Shortcuts buttons, which allows you to search immediately in multiple sites within a category|
|**Using search input box -** ***typing what you want to search in the chosen site(s)***|You can type anything you want in the input box, and then you can either \[1\] click the search button, or \[2\] click the Enter button from your keyboard, in order to start searching|
|**Browsing the results page**|\[1\] You can click on the title / link of the result to visit the site, \[2\] you can click on the site's name to visit the normal homepage of the site, \[3\] if the results count is greater than 30 you can browse other pages by clicking the number buttons at the bottom of the page|

#### Additional Note
Searching in ALL sites is time consuming, especially with slow wifi connections. I removed the button All from the Shortcuts, since it would be more efficient to strategically search in a category. However, you can still use "all" in the site input box to search everywhere since it is also a good way to test if all sites are working properly.

## Requirements and Running
This software uses <a href="https://pypi.org/project/beautifulsoup4/" target="_blank">BeautifulSoup</a> and <a href="https://pypi.org/project/customtkinter/" target="_blank">CustomTkinter</a>. Use this command within the extracted folder to install everything from the requirements.txt file, or you can manually from PyPI:
 
    pip install -r requirements.txt

Make sure you have pip and Python installed. 
Keep in mind, running it with native Python will always be faster than with a UI/web version, once you install Python and the requirements it's easy and fast to run it.

    Open terminal in the program's folder (from Linux point) and run
        python3 pSearch.py
        
But as an alternative and a faster method, I also build the program in a standalone executable file which you can download from every release.

## There are some not-so-important functionalities at the top...
- **DB Checker** checks the health (page code) of all of the sites in the database then prints it in the command line. Make sure to run the .exe via command line to see the actual results because I have disabled the console while building the program. Please note that overtime I have noticed this method to be not fully efficient, since some sites can change their URL or key names, which returns no results and no errors. But, it's still good for quick analysis, though the "all" search is more useful for detecting errors.
- **Base64 Encode/Decode** is for decoding/encoding base64. I added this because FMHY has a base64 database so you can directly use this to decode them (that's the main reason I added it for but of course it can be used for its primary functionality).

## From where do I get the websites?
Piracy Megathread and a mix of the "Other Treasures": https://www.reddit.com/r/Piracy/wiki/megathread/#wiki_.1FA99_.279C_other_treasures

Note: I don't use ALL megathreads. I add sites based on:
- the database amount, for example if there aren't enough links for Android then I start to search for Android related websites in the various trusted megathreads.
- removed content. If I remove a site from a category, I search for another replacement from the trusted megathreads.

 ## Notice
- This tool doesn't let you download files. Simply just a search tool. It doesn't grab direct download links, it just searches and gives you the original pages of the website. 
- You may face errors when using the standalone version for Windows. If you do face any errors please report it in the Issues section so I would know.
- Please use an adblocker in your browser to stay safe when visiting a website!
 
 ### Violation Notes
 This program shouldn't violate any ToS's of the websites included as it doesn't grab the download links. It still forwards to the original website, just the software's page of it.

#### Contribution 
Can be directly done by using https://sqlitebrowser.org/ and opening the database file, you can also check the Wiki page for contribution. Though, you have to inform me of the websites added/removed, and if added from which megathread you have taken it.
