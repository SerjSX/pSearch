import customtkinter
from tkinter import *
from tkinter import ttk

class progressBar(customtkinter.CTkToplevel):
    """
        Responsible to create the progress bar and update the progress while the program searches and 
        scrapes a site.
    
        customtkinter's CTkToplevel is used to add a new window at the top which will have 
        the progress bar and a title stating "Searching..."
        
        Methods:
            add_step()    : adds a step to the progress bar.
            close_window(): destroys the window (once the search and scraping is done on all websites). 
    
    """
    
    
    def __init__(self,len_websites):
        # Initializes the window
        super().__init__()
        # adds a title
        self.title("pSearch")
        # adds the focus on the window
        self.attributes("-topmost", True)
        self.geometry("80x80")

        title = customtkinter.CTkLabel(self, text="Searching...")
        title.place(x=0,y=10,relwidth=1)    
        
        # adds the progress bar, with the maximum as the length of the websites that the program
        # is searching in.
        self.search_progress_bar = ttk.Progressbar(self, orient=HORIZONTAL, maximum=len_websites)
        self.search_progress_bar.place(x=0, y=50, relwidth=1)
        
    def add_step(self):
        # add 1 step to the progress bar
        self.search_progress_bar.step(1)
        self.update()
        
    def close_window(self):
        self.destroy()