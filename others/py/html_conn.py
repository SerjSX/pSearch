import urllib.parse, urllib.request
import requests
from tkinter import messagebox
import traceback
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# This page is responsible for connecting and scraping a page.

# Used as a header when requesting a website
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}
          
class page_conn:
    def __init__(self,search_value,site_name,site_link,site_slink,chosen_type,plusorspace): 
        """
            This class is used to connect and scrape a website with specific attributes.
            
            Primary Attributes:
                site_name = the site's name
                site_link = the site's link (normal domain)
                site_slink = the site's search link (used to search something)
                
            Paramethers:
                search_value = what to search in a site
                site_name = the name of the website
                site_link = the site's link
                site_slink = the site's search link
                chosen_type = the type of the website (used for preparing the search link)
                plusorspace = used to identify if the site searches with separating words
                              by a space or a + sign.
                              
            Methods:
                get_html() = attempts to get the html file, returns it with the page code (health).
                             if it fails it just returns an error page code -1.
                scrape(html,site_link,site_key1,site_key2,site_key3,hasmainlink) =
                            scrapes the results and returns the best links and the normal links.
                
        
        """
        # Adjusting the search URL based on the criterias passed to be used in the other methods.
        self.site_name = site_name
        self.site_link = site_link
        self.site_slink = site_slink
        
        # If the link starts with https://1337x.to then quote it with %20 (space), this is unique for this site
        # because of its web structure.
        if site_link.startswith("https://1337x.to"):
            # If chosen_type is Android, add the keyword "android" at the end for accurate results.
            if chosen_type == "android":
                search_value_fixed = urllib.parse.quote(search_value + " android")
                # Connect the url with the software name the user put at the beginning
                self.search_url = site_slink + search_value_fixed + "/1/"
            else:
                search_value_fixed = urllib.parse.quote(search_value)
                # Connect the url with the software name the user put at the beginning
                self.search_url = site_slink + search_value_fixed + "/1/"
        # If the site is FileCR and the chosen type is Android, then specifically search it in
        # the android section for accurate results.
        elif site_name == "FileCR" and chosen_type == "android":
            self.search_url = site_slink + urllib.parse.quote_plus(search_value) + "&subcat_filter=&category-type=23"
        # If it doesn't start with https://1337x.to/ then quote it with + (it replaces space with +), this is
        # the default method as most sites work this way.
        else:
            if plusorspace == 0:
                search_value_fixed = urllib.parse.quote_plus(search_value)
            else:
                search_value_fixed = urllib.parse.quote(search_value)           
        
            # Connect the url with the software name the user put at the beginning
            self.search_url = site_slink + search_value_fixed
    
    
    # Gets the HTML file and page code.
    def get_html(self):
        # Try to open the URL to read
        try:
            # Send a request to connect to the site with the header and retrieve html
            html = requests.get(self.search_url, headers=header).content
            
            # page_code variable is used to identify a healthy connection or no.
            # The program then chooses to scrape or no, preventing further errors if any.
            page_code = 200
            return (html,page_code)
        except:  #if an error pops up, then show the error. This should be reported on Github since the site may be broken or changed.
            messagebox.showerror("Error!", "An error occurred during searching the following site: " + self.search_url + "\nSearch process will continue")
            print(self.search_url + " resulted the following error (search will continue):\n" + traceback.format_exc())
            print("Please report it to the developer on Github")
            page_code = -1
            return (0,page_code)
            
    def scrape(self,html,site_link,site_key1,site_key2,site_key3,hasmainlink):        
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(html, 'lxml', parse_only=SoupStrainer(site_key1))
        result_links,best_results,allLinks = {},{},{}

        # Souping elements according to the chosen software. Some work the same way, so they have the same souping method.
        # If the site_key2-3 aren't 'null', then use the default method (specific class)
        if site_key2 != "null" and site_key3 != "null":
            tags = soup.find_all(site_key1, attrs={site_key2: site_key3})
        # If it is null, then this is done on purpose as the websites have special conditions, for example 1337x. Explained further afterwards.
        else:
            # soups without a specific class, the site_key1 is most probably "a".
            tags = soup.find_all(site_key1)

        # For each tag in tags...
        for tag in tags:
            # Find the "a" / links
            links = tag.a

            # If it didn't result "None"...
            if links is not None:
                # Get the href (link)
                main_link_a = links.get("href")
                # If it isn't None...
                if main_link_a is not None:
                    # The link_text stores the text of the link.
                    # The condition checks if hasmainlink value is 1, meaning this site will have link results without the domain of
                    # the website. So the program adds the domain for a correct output.
                    link_text = links.get_text(" ",strip=True)
                    if hasmainlink == 1:
                        result_links_val = self.site_link + main_link_a
                    # If not, just use the returned link as it is.
                    else:
                        result_links_val = main_link_a

                    # adds result.
                    result_links[link_text] = result_links_val

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
                    link_text = tag.get_text(" ",strip=True)
                    if main_link_b.startswith("/torrent/"):
                        # uses tag.text because the name/link is already in the looped tag.
                        result_links[link_text] = self.site_link + main_link_b
        
        
        # keeps track of count to know the best count.
        results_count = 0
        
        # If the length of result_links is greater than 0...
        if len(result_links) > 0:
            # Append the link to allLinks list.
            for link in result_links.items():
                if results_count < 1:
                    best_results[("best", self.site_name, self.site_link, link[0])] = link[1]
                    results_count = results_count + 1
                else:
                    allLinks[("default", self.site_name, self.site_link, link[0])] = link[1]
                                        
            return (best_results, allLinks)
        else:
            print("\nPlease note that the following site returned no results: " + self.site_slink)
            return -1