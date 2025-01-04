from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image
import sys
import webbrowser
import random
import pyperclip
import math
# Imports backend operations that are required to do import, load and search websites
from others.backend import websites
# Customtkinter used for GUI
import customtkinter

# Grabs the directory name
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    path = sys._MEIPASS
else:
    path = os.path.dirname(os.path.abspath(__file__))

print("Welcome to pSearch. This command line is used to see errors, you can minimize it!")

# Preparing the image widgets for search, github and copy logos.
search_img = customtkinter.CTkImage(light_image=Image.open(path + "/media/search_button.png"),
                            size=(25,25))
github_img = customtkinter.CTkImage(light_image=Image.open(path + "/media/Github/GitHub-Mark-Light-32px.png"), 
                            dark_image=Image.open(path + "/media/Github/GitHub-Mark-32px.png"),
                            size=(25,25))
copy_img = customtkinter.CTkImage(light_image=Image.open(path + "/media/copy.png"),
                                    size=(25,25))
dark_mode_img = customtkinter.CTkImage(light_image=Image.open(path + "/media/dark_mode.png"),
                                    size=(25,25))
light_mode_img = customtkinter.CTkImage(light_image=Image.open(path + "/media/light_mode.png"),
                                    size=(25,25))
                                    
# Search texts randomly shown in input box.
search_text = ["What do you want to search today?",
                "What do you want to search?",
                "Use an adblocker please!",
                "Enter what you want to search here!",
                "Here is where you put what you want to search.",
                "Enter search value here...",
                "Make sure you fill this before clicking the search button!",
                "Searching ALL sites might take some time, so try to avoid it.",
                "<-- You can search \"all\" sites ;)"]

# Used to show images for each type afterwards
type_images = {
    'android': path + '/media/android_image.png',
    'comics_manga': path + '/media/comics_manga_image.png',
    'courses': path + '/media/course_image.png',
    'ebooks': path + '/media/ebook_image.png',
    'games': path + '/media/game_image.png',
    'movieseries': path + "/media/movieseries_image.png",
    'software': path + '/media/software_image.png',
    'music': path + '/media/music_image.png',
    'all': path + '/media/all_image.png',
    'assets': path + '/media/asset_image.png',
}

class App(customtkinter.CTk):
    def __init__(self):
        """
            This class is the primary class for the GUI and connecting to the other Python files.
            
            Primary Attributes:
                final_links = stores all of the links
                types_list = stores a list of the types of websites
                websites = stores all of the available websites from the JSON file
                
            Methods:
                __init__ = initializes the needed variables and creates the main GUI page.
                change_theme(current_theme) = changes the theme of the GUI (dark/lght)
                apply_to_variable(chosen_input) = adds the value when clicking one of the shortcut 
                                                buttons to the site search entry input box.
                cb(link, type=None) = opens the link in browser.
                create_results_window(button_num,start_position,end_position) =
                                      creates the results window 
                search_signal(button_num, nwindow, chosen_input, 
                              search_value, start_position, end_position) = 
                                      sends the search signal to search
        """
        
        super().__init__()
        
        # storing all links 
        self.final_links = {}
        
        # stores the types of the websites (no repeated) and the websites themselves in separate variables
        self.types_list = websites_var.get_types()
        self.websites = websites_var.get_all()
        
        self.title("pSearch")
        self.geometry("850x600")
        
        # these variables are initialized now to check later in search_signal method if they are open or no
        self.search_results_window = None
        self.search_results_frame = None

        # .ico works only on windows, not linux - Thanks to  viggo-wellme  for mentioning it
        # https://github.com/SerjSX/pSearch/pull/3
        if os.name == "nt":
            self.iconbitmap(path + "/media/icon.ico")

        # This frame includes other buttons with small functions
        top_functions_frame = customtkinter.CTkFrame(self)
        top_functions_frame.pack(side=TOP, fill=BOTH)

        # theme changer button
        self.toggle_theme_btn = customtkinter.CTkButton(top_functions_frame, text="", cursor="hand2",image = light_mode_img if customtkinter.get_appearance_mode() == 'Dark' else dark_mode_img, command=lambda: self.change_theme(customtkinter.get_appearance_mode()), width=40, corner_radius=0)
        self.toggle_theme_btn.pack(side=LEFT, padx=5)
        
        
        # Github visit button
        github_button = customtkinter.CTkButton(top_functions_frame, text="Star on Github! ", border_spacing=3, cursor="hand2", height=30, width=0, corner_radius=0, image=github_img, command=lambda: self.cb("https://github.com/SerjSX/pSearch/"))
        github_button.pack(side=RIGHT, padx=5)

        # Title message - pSearch
        wlcmsg = customtkinter.CTkLabel(self, text="pSearch - Piracy Multi-Search Tool", font=customtkinter.CTkFont(size=24, weight="bold"))
        wlcmsg.pack(side=TOP, pady=100)

        # Creates a list for storing the available sites from the database to show on the dropdown list
        self.websites_list_dropdown = ['all'] + [web['name'] + " - Type: " + web['type'] for web in self.websites]

        # Create a StringVar to insert the chosen value in it (either by clicking one of the buttons or from dropdown menu)
        option_chosen = StringVar()

        # Sets the first item in the list as the default chosen input.
        option_chosen.set("all")

        # Creates a frame to put the search bar, dropdown menu, and search button in it.
        process_chosen_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        process_chosen_frame.pack(padx=10, pady=10) 

        # Creates entry for user input space with width 300      
        search_entry_input = customtkinter.CTkEntry(process_chosen_frame, height=30, width=350,placeholder_text=random.choice(search_text))

        # Creates entry for user input space with width 300      
        self.site_entry_input = customtkinter.CTkComboBox(process_chosen_frame, variable=option_chosen, values=self.websites_list_dropdown, height=30, width=200, command=lambda e: self.apply_to_variable(self.site_entry_input.get()))
        self.site_entry_input.set("Enter site name here")
        # allows the user to search the sites list.
        self.bind('<Return>',self.update_site_entry_input)


        # Creates the search button widget, with the on-click command heading towards search_signal method
        # with passing the option chosen and the search entry.
        search_submit_btn = customtkinter.CTkButton(process_chosen_frame, 
                                                text="", 
                                                image=search_img, 
                                                command=lambda: self.search_signal(0, False, self.site_entry_input.get(), search_entry_input.get(), 0, 0), 
                                                width=10,
                                                height=30,  
                                                cursor="hand2")

        self.site_entry_input.pack(side=LEFT, padx=5)
        search_entry_input.pack(side=LEFT)

        search_submit_btn.pack(side=RIGHT, padx=10)

        # Bind the keyboard function Enter to the entry so user can directly click Enter to search.
        search_entry_input.bind("<Return>", lambda e: self.search_signal(0, False, self.site_entry_input.get(), search_entry_input.get(), 0, 0))


        # This frame is used to show the type shortcuts
        typesFrame = customtkinter.CTkScrollableFrame(self, height=500, width=500, fg_color="transparent", border_width=1)
        typesFrame.pack(pady=20)
        titleButton = customtkinter.CTkLabel(typesFrame, text="Shortcuts", fg_color="transparent", font=("Ariel", 20), width=70, height=32)
        titleButton.pack(pady=(25,0))
        descr = customtkinter.CTkLabel(typesFrame, text="Search by types faster", fg_color="transparent", font=customtkinter.CTkFont(family="Ariel", size=12, slant="italic"), width=70, height=32)
        descr.pack(pady=5)

        # Creates an outer frame for displaying all-in-one types search with their logo and text.
        types_outer_frame = customtkinter.CTkFrame(typesFrame, fg_color="transparent", cursor="hand2")
        types_outer_frame.pack(padx=5,pady=(0,5))
        
        
        # Adding the shortcut buttons based on the types of the websites 
        # For each type in the types taken from the websites_var method get_types()...
        # The two count variables below are used to control how many type buttons the program
        # will load in a single row (3 per row, then scrollable frame to see other rows.).
        col_count,row_count = 0,0
        for type in self.types_list:
            if type != "all":
                # Create a frame to insert image and name under it
                type_frame = customtkinter.CTkFrame(master=types_outer_frame)
                type_frame.grid(row=row_count,column=col_count, pady=10, padx=30)

                # Generates the image for the type.
                # The variable has a specific name to prevent errors, and it grabs the directory from the dictionary 
                # according to the type's name.
                type_images["{0}".format(type)] = customtkinter.CTkImage(light_image=Image.open(type_images[type]),
                                                                    size=(48,48))

                # Creates the buttons for each type to display type name
                type_btns = customtkinter.CTkButton(master=type_frame, 
                                                width=70,
                                                height=32,
                                                text=type.capitalize() + " Sites", 
                                                command=lambda type=type: self.apply_to_variable(type),
                                                image=type_images["{0}".format(type)],
                                                compound="top", 
                                                cursor="hand2",)
                type_btns.pack(side=TOP)
                
                col_count += 1
                
                if col_count == 3:
                    row_count += 1
                    col_count = 0    
             
    # Used for changing the software's theme - dark or light
    def change_theme(self,current_theme):
        if current_theme == "Light":
            self.toggle_theme_btn.configure(image=light_mode_img)
            customtkinter.set_appearance_mode("dark")
        else:
            self.toggle_theme_btn.configure(image=dark_mode_img)
            customtkinter.set_appearance_mode("light")


    # This allows the user to enter a site name, click Enter, and then check the 
    # dropdown menu to see possible choices.
    def update_site_entry_input(self,event):
        # gets the current input and makes it lowercase
        a=self.site_entry_input.get().lower()
        
        # proceeds only if the length of the input is not 0 and it isn't empty, if they are
        # then keep the same websites list.
        if (len(a) != 0) and (a != " "):
            # loops over the websites and checks if the user input is in the websites.
            newvalues=[i for i in self.websites_list_dropdown if a in i.lower()]
        else:
            newvalues=self.websites_list_dropdown

        # If the results of newvalues ins't 0, set it as the new values of the dropdown menu
        if len(newvalues) != 0:
            self.site_entry_input.configure(values=newvalues)
        else:
            # else throws an error.
            messagebox.showerror("Couldn't find that site!", "That site is not found. Try to rephrase it, or check the list to know the available websites.")



    # This is used when the user clicks from the dropdown menu to search a site or if a shortcut is 
    # clicked on. If the user clicks on one of the type buttons, then this function is responsible
    # to set the value of the site_entry_input as the clicked value.
    def apply_to_variable(self,chosen_input):
        self.site_entry_input.set(chosen_input)


    # Used when clicking on the results to visit link
    def cb(self, link, type=None):
        webbrowser.open_new(link)
    
        # Adjusts the window of the results so it wouldn't be shown on top of the browser.
        if type == "result":
            self.search_results_window.attributes("-topmost", False)
 
   
    # Responsible to create the window to show results.
    def create_results_window(self,button_num,start_position,end_position):
        # If the search results window isn't None then most probably there's another one already on-screen,so it destroys it to just have one window.
        if self.search_results_window != None:
            self.search_results_window.destroy()
            
        # Create a result window for the frame, adds title and puts it as the main focus
        self.search_results_window = customtkinter.CTkToplevel(self)
        self.search_results_window.title("pSearch - Results")
        self.search_results_window.attributes("-topmost", True)
       
        
        # creates a scrollable frame to put the results in afterwards 
        self.search_results_frame = customtkinter.CTkScrollableFrame(self.search_results_window, fg_color="transparent")
        self.search_results_frame.pack(anchor="nw", fill=BOTH, expand=True)
        
            
        # At the end, it prints the results if the length of the results is greater than 0, else no 
        # results.
        if len(self.final_links) > 0:
            # result_count is used to limit how much results the program is allowed to show.
            result_count = 0 

            # Creates a notice block to always use an adblocker extension
            notice_ublock = customtkinter.CTkButton(self.search_results_frame, text="Please use an adblocker extension, whether in your browser or through a DNS service. Click on this text to go Piracy Megathread's protection recommendation.",
                                                    command=lambda: self.cb("https://www.reddit.com/r/Piracy/wiki/megathread/#wiki_.26F5_.279C_not_so_fast_sailor.21_do_this_first", "result"))
            notice_ublock.pack(expand=TRUE, fill=BOTH)

            # Convert dictionary keys and values to list to select accordingly afterwards
            keys = list(self.final_links.keys())
            values = list(self.final_links.values())
            
            # Loops over the range (start_position,end_position) to display each result.
            # start position and end positions are used to keep track of the buttons if 
            # there are long results. At first, it's from 0 till the length of the results
            # we got. If the number of results is 28 and the limit per page is 30, then 
            # the program does not add buttons on the results page. 
            # But if there are 64 results for example, and the limit is 30, then the program
            # will add 3 buttons on the results page.
            # button 1 = 30 results, button 2 = 30 results, button 3 = 4 results.
            # And the start and end position will change accordingly as seen later with the 
            # computations used when creating the buttons for the result pages.
            for i in range(start_position,end_position):
                # Assign variables to each necessary information
                # i = index number according to start_position and end_position
                type = keys[i][0]
                site_name = keys[i][1]
                site_link = keys[i][2]
                name = keys[i][3]
                link = values[i]
                
                # Limiting only 30 results per page. (starts from 0)
                if result_count < 30:
                    # The frame to put a result's data in.
                    # Stores 2 frames for each result which store the title, the link and the copy button.
                    self.result_primary_frame = customtkinter.CTkFrame(self.search_results_frame, fg_color="transparent")
                    self.result_primary_frame.pack(expand=TRUE, fill=BOTH, pady=20)

                    # Putting a frame for the site name and the title.
                    result_frame = customtkinter.CTkFrame(self.result_primary_frame, fg_color="transparent")
                    result_frame.pack(expand=TRUE, fill=BOTH, in_=self.result_primary_frame)              
                    # a frame for the copy button and the result link
                    result_link_frame = customtkinter.CTkFrame(self.result_primary_frame, fg_color="transparent")
                    result_link_frame.pack(expand=TRUE, fill=BOTH, side=TOP)

                    copy_button = customtkinter.CTkButton(result_link_frame,  cursor="hand2", image=copy_img, text="", width=20, corner_radius=0, fg_color="#EAE0DA", hover_color="#F7F5EB", command=lambda link=link: pyperclip.copy(link))
                    copy_button.pack(side=LEFT, anchor="w")

                    # The color of the site name changes if it's the top result, or else by default orange.
                    result_site_name = customtkinter.CTkLabel(result_frame, text=" " + site_name + " ", fg_color="#A8E4A0" if type == "best" else "orange", corner_radius=0, width=40, text_color="black")

                    # If the link is too long (greater than 160 characters), the program strips it and adds "..." at the end.
                    result_link = customtkinter.CTkLabel(result_link_frame, text=link[:159].strip() + "..." if len(link) > 160 else link.strip(), cursor="hand2", font=customtkinter.CTkFont(size=12))

                    # If the name/title of the result is too long (greater than 110 characters), the program again strips the text.
                    result_name = customtkinter.CTkLabel(result_frame, text=name[:109].strip() + "..." if len(name) > 110 else name.strip(), cursor="hand2", font=customtkinter.CTkFont(size=18, weight="bold"))
                
                    result_site_name.pack(side=LEFT, anchor="w")
                    result_name.pack(side=LEFT, anchor="w", padx=10)
                    result_link.pack(side=LEFT, anchor="w", padx=5)
                
                    result_name.bind("<Button-1>", lambda e,link=link: self.cb(link, "result"))
                    result_link.bind("<Button-1>", lambda e,link=link: self.cb(link, "result"))
                    
                    # to limit only 30 results
                    result_count += 1

            # If the number of results is greater than 30, create the buttons at the bottom of the results page!
            if len(self.final_links) > 30:
                # count is used for counting each number from the input
                several_btn_count = 0
                
                # length has the length of the results
                several_btn_length = len(self.final_links)
                
                # list to append the amount for each button
                several_btn_list = list()

                # Divides the input by 30 (to get appx how many buttons it needs)
                btn_count = math.ceil(several_btn_length/30)

                # For b in the range of btn_count...
                for b in range(btn_count):
                    # for i in the range of the input plus one...
                    for i in range(several_btn_length + 1):      
            
                        # If the _count reached 30
                        if several_btn_count == 30:
                            # append it to the list
                            several_btn_list.append(str(b) + "-" + str(several_btn_count))
                            # deduct from _length the appended amount
                            several_btn_length = several_btn_length - several_btn_count
                            # reset the btn count to 0
                            several_btn_count = 0
                            # break and start over
                            break

                        # if the b is the last button count and the count matches the length, which means
                        # it's the last button's amount...
                        if b == btn_count - 1 and several_btn_count == several_btn_length:
                            # append _count to the list
                            several_btn_list.append(str(b) + "-" + str(several_btn_count))
                        # Increment several_btn_count by 1
                        several_btn_count += 1

            
                # to limit only showing 20 buttons.
                button_limit_count = 0 
                button_limit = 20 # this is the maximum number of buttons allowed to show 
                for button in several_btn_list:
                    if button_limit_count <= button_limit:
                        # Split the value
                        button_split = button.split("-")
                        # Put the id and value in separate variables
                        button_id = int(button_split[0])
                        button_value = int(button_split[1])

                        # create the button by passing starting position(button_id*button_limit) and ending position(button_id*button_limit+button_value)
                        # WHEN CLICKED computation is done to find the start position and end 
                        # position. button_value is the number of results in the page, 
                        # and button_id is the count. So:
                        # starting_position: 0 * 20
                        # ending position: 0 * 20 + 30 (if the maximum limit of results is 30)
                        # for button 1:
                        #   starting_position: 1*20
                        #   ending position: 1 * 20 + 30 (if the number of resuolts in page 1
                        #                                 is 30)
                        # ...
                        other_page_btns = customtkinter.CTkButton(self.search_results_frame, text=button_id, command=lambda button_id=button_id, button_value=button_value: self.search_signal(str(button_id), True, self.chosen_input, self.search_value, button_id*button_limit, button_id*button_limit+button_value), width=30, height=30)
                        other_page_btns.pack(side=LEFT, padx=10, pady=5)

                        # Only allowing 20 buttons to be displayed, increase till condition meets.
                        button_limit_count += 1

                    else:
                        # break for loop once condition meets
                        break

            # Adjusts the geometry of the window
            # Also changes the title of the window to state the count of results and which window the
            # user it in.
            self.search_results_window.geometry("1250x650")
            self.search_results_window.title("pSearch - " + str(result_count) + " results - Window " + str(button_num))
            
        # If it isn't greater than 0, it says No Results
        else:
            noresult = messagebox.showwarning("No results!", "Click Ok to search again.")
            self.search_results_window.destroy()                    

    
    # sends the signal to do a search 
    def search_signal(self, button_num, nwindow, chosen_input, 
                        search_value, start_position, end_position):
        
        try:
            # Splits the chosen_input to extract the name of the site
            self.chosen_input = chosen_input.split('-')[0].strip()     
        except:
            # if that throws an error for whatever reason, keep the input as the same. Possibly it can 
            # be a type so it does not have a count with -.
            self.chosen_input = chosen_input
            
        self.search_value = search_value

        # If the tnered search value isn't 0 then proceed with searching 
        if len(self.search_value) != 0:
            # If new window is false, if it's true then the user clicked one of the buttons on an already existing results window and the starting/endig position are different.
            if nwindow == False:
                # Proceeds with the search method in websites_var, which is supposed to return a 
                # dictionary containing all of the search results (best > default)
                # Check backend.py for more information on what it does.
                self.final_links = websites_var.search(self.chosen_input,self.search_value,nwindow)
                
                # If it is -1, then there is an input error so it does not create a results window.
                if self.final_links != -1:
                    self.create_results_window(button_num,0,len(self.final_links))
            
            else:
                self.create_results_window(button_num,start_position, end_position)

        else:
            messagebox.showerror("No search input!", "Hmm, you're going to search... Nothing? Try again.")
        
    
websites_var = websites()
websites_var.load_json()

app = App()
app.mainloop()
