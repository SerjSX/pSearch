![pSearch on version 1.6.2](https://i.ibb.co/2cVk43b/Capture.png)

<p align="center">
  <img src="https://img.shields.io/github/downloads/SerjSX/pSearch/total" alt="Downloads"/>
  <img src="https://img.shields.io/github/downloads/SerjSX/pSearch/latest/total" alt="Latest Downloads"/>
  <img src="https://img.shields.io/github/license/SerjSX/pSearch" alt="License"/>
  <img src="https://img.shields.io/github/languages/top/SerjSX/pSearch" alt="Top Language"/>
</p>


# pSearch
 Searching tool written in Python for Piracy related websites. You choose where you want to search, and the program does its own work and shows you the results. It is similar to normal search engines, however the program searches the site on-spot rather than having a database with different results.

~ If you see a terminal/command line opening when you run the program, don't worry about it! It's for showing errors, that way you and I can see the error easily (if there is one). 

## Version Differences
1. Source Code: running pSearch from the source code requires BeautifulSoup and CustomTkinter (check Requirements and Running). This is the fastest way you can run the program, as it isn't built in any way and it's just it.
2. Windows Standalone: this is a standalone .exe build of the program meant for distribution. The builds are done with Nuitka. You may face errors, if you do so please let me know about them. From version 1.6.3 I will build them with console enabled, that way you can see an error by running the program from the command prompt. (You open the command prompt in the folder and type pSearch.exe)
3. Windows Onefile Standalone: this is a onefile standalone .exe build of the program. It is similar to the standalone, but there are less files for the modules because they are built within the program. Only the others and media folders are included, and bs4 and customtkinter zip files which the program extracts to use. This version may start the program slower, but it may show less errors. If you do face an error let me know about it.

## Requirements and Running
This software uses <a href="https://pypi.org/project/beautifulsoup4/" target="_blank">BeautifulSoup</a> and <a href="https://pypi.org/project/customtkinter/" target="_blank">CustomTkinter</a>. Use this command within the extracted folder to install everything from the requirements.txt file, or you can manually from PyPI:
 
    pip install -r requirements.txt

Make sure you have pip and Python installed. 
Keep in mind, running it with native Python will always be faster than with a UI/web version, once you install Python and the requirements it's easy and fast to run it.

    Open terminal in the program's folder (from Linux point) and run
        python3 pSearch.py
        
But as an alternative and a faster method, I also build the program in a standalone executable file which you can download from every release.

 ## Notice
- This tool doesn't let you download files. Simply just a search tool. It doesn't grab direct download links, it just searches and gives you the original pages of the website. YOU CANNOT DOWNLOAD ANYTHING WITH THIS TOOL.
- You may face errors when using the standalone version for Windows. If you do face any errors please report it in the Issues section so I would know, or in the Reddit post: https://www.reddit.com/r/Piracy/comments/zz9tn7/psearch_piracy_multisearching_tool/
 
 ### Violation Notes
 This program shouldn't violate any ToS's of the websites included as it doesn't grab the download links. It still forwards to the original website, just the software's page of it.

#### Contribution 
Can be directly done by using https://sqlitebrowser.org/ and opening the database file, or use db_adder.py from the others folder. And check the Wiki page for contribution.
