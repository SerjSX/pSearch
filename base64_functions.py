import base64
import customtkinter
from tkinter import * 
from tkinter import messagebox

def button_click_event(type, input):
    results = list()
    lines = input.split()
    fixed_lines = list()

    for line in lines:
        split = line.split("\n")
        for splitted in split:
            fixed_lines.append(splitted)
    
    for line in fixed_lines:
        if type == "decode":
            decodedBytes = base64.b64decode(line)
            results.append(str(decodedBytes, "utf-8"))

        elif type == "safe decode":
            decodedBytes = base64.urlsafe_b64decode(line)
            results.append(str(decodedBytes, "utf-8"))

        elif type == "encode":
            encodedBytes = base64.b64encode(line.encode("utf-8"))
            results.append(str(encodedBytes, "utf-8"))   

        elif type == "safe encode":
            urlSafeEncodedBytes = base64.urlsafe_b64encode(line.encode("utf-8"))
            results.append(str(urlSafeEncodedBytes, "utf-8"))
        
    if len(results) > 0:
        result_window = customtkinter.CTkToplevel(app)
        result_textbox = customtkinter.CTkTextbox(result_window)
        result_textbox.pack()
        result_count = 1

        for result in results:
            result_textbox.insert(str(result_count) + ".0", result + "\n\n")
            result_count = result_count + 1
        
        result_textbox.configure(state="disabled")
    else:
        messagebox.showerror("Hmm... That's weird", "Looks like you didn't put anything to " + type + ", try again")


def start_base64():
    global app

    app = customtkinter.CTk()
    app.geometry("750x350")
    app.title("Base64 Decoder/Encoder")

    label_text = customtkinter.CTkLabel(app, text="This program is used to perform Base64 encoding/decoding")
    label_text.pack(pady=30)

    input_textbox = customtkinter.CTkTextbox(app)
    input_textbox.pack()

    button_decode = customtkinter.CTkButton(app, text="Decode", command=lambda: button_click_event("decode", input_textbox.get("0.0", "end")))
    button_decode.pack(pady=10, padx=10, side=LEFT)
    button_sdecode = customtkinter.CTkButton(app, text="URL and Filename Safe Decode", command=lambda: button_click_event("safe decode", input_textbox.get("0.0", "end")))
    button_sdecode.pack(pady=10, padx=10, side=LEFT)

    button_encode = customtkinter.CTkButton(app, text="Encode", command=lambda: button_click_event("encode", input_textbox.get("0.0", "end")))
    button_encode.pack(pady=10, padx=10, side=LEFT)
    button_sencode = customtkinter.CTkButton(app, text="URL and Filename Safe Encode", command=lambda: button_click_event("safe encode", input_textbox.get("0.0", "end")))
    button_sencode.pack(pady=10, padx=10, side=LEFT)

    app.mainloop()

