import base64
import customtkinter 
from tkinter import * 
from tkinter import messagebox
    
class base64App(customtkinter.CTk):
    """
    Simple class to decode/encode base64 encyrpted messages.
    Specifically used for freemediaheckyeah storage links that are usually encoded.
    
    
    """
    def __init__(self):
        # This is used to close the result window if another one is opened already.
        self.result_window = None
        
        # Creating the window
        super().__init__()
        self.geometry("750x350")
        self.title("Base64 Decoder/Encoder")
        self.attributes("-topmost", True)
        
        # Adding text, input box and buttons for decode, safe decode, encode and safe encode.
        label_text = customtkinter.CTkLabel(self, text="This program is used to perform Base64 encoding/decoding")
        label_text.pack(pady=30)
 
        self.input_textbox = customtkinter.CTkTextbox(self)
        self.input_textbox.pack() 

        button_decode = customtkinter.CTkButton(self, text="Decode", command=lambda: self.decode())
        button_decode.pack(pady=10, padx=10, side=LEFT)
        
        button_sdecode = customtkinter.CTkButton(self, text="URL and Filename Safe Decode", command=lambda: self.sdecode())
        button_sdecode.pack(pady=10, padx=10, side=LEFT)

        button_encode = customtkinter.CTkButton(self, text="Encode", command=lambda: self.encode())
        button_encode.pack(pady=10, padx=10, side=LEFT)
        
        button_sencode = customtkinter.CTkButton(self, text="URL and Filename Safe Encode", command=lambda: self.sencode())
        button_sencode.pack(pady=10, padx=10, side=LEFT)
    
    # This method creates the results window after encoding/decoding to show the output
    def create_results_window(self, results):
        # As long as the results length is greatr than 0 (meaning there are results.)
        if len(results) > 0:
            # Destroy the results window if another one exists already.
            if self.result_window != None:
                self.result_window.destroy()
            
            # Create a new results window, add the title and a text box to show the results.
            self.result_window = customtkinter.CTkToplevel(self)
            self.result_window.title("Result Window")
            result_textbox = customtkinter.CTkTextbox(self.result_window)
            result_textbox.pack()

            # Insert the results in the text box under each other.
            for result in results:
                result_textbox.insert(str(result_count) + ".0", result + "\n\n")
        
            # make the text box disabled so the user can't add anything in it.
            result_textbox.configure(state="disabled")
        else:
            # shows an error if there are no results.
            messagebox.showerror("Hmm... That's weird", "Looks like you didn't put anything to " + type + ", try again")        

    # split line is used to separate each line and each word for a proper operaiton.
    def split_line(self):
        lines = self.input_textbox.get("0.0", "end").split()
        fixed_lines = [splitted for line in lines for splitted in line.split("\n")]

        return fixed_lines 
    
    # used for decoding an input 
    def decode(self):
        # Gets the correct lines 
        fixed_lines = self.split_line()
        # Initializes a list for results
        results = list()
        
        # decodes each line and appends it to the list
        for line in fixed_lines:
            decodedBytes = base64.b64decode(line)
            results.append(str(decodedBytes, "utf-8"))
            
        # creates the results window to show the results 
        self.create_results_window(results)

    # Same operation as decode, but for safe decoding.
    def sdecode(self):
        fixed_lines = self.split_line()
        results = list()
        
        for line in fixed_lines:
            decodedBytes = base64.urlsafe_b64decode(line)
            results.append(str(decodedBytes, "utf-8"))
            
        self.create_results_window(results)
    
    # same operation but for encoding
    def encode(self):
        fixed_lines = self.split_line()
        results = list()
        
        for line in fixed_lines:
            encodedBytes = base64.b64encode(line.encode("utf-8"))
            results.append(str(encodedBytes, "utf-8"))  
            
        self.create_results_window(results)

    # same operation but for safe encoding
    def sencode(self):
        fixed_lines = self.split_line()
        results = list()
        
        for line in fixed_lines:
            urlSafeEncodedBytes = base64.urlsafe_b64encode(line.encode("utf-8"))
            results.append(str(urlSafeEncodedBytes, "utf-8"))
            
        self.create_results_window(results)

app = base64App()
app.mainloop()