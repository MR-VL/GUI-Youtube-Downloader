# Import necessary libraries
from tkinter import *
from pytube import YouTube
import threading
from tkinter import ttk
import json
from tkinter import messagebox

# Initialize a flag for checking if the preferences file is found
jsonFileFound = False

# Function to read preferences from the JSON file
def readFile():
    with open('preferences.json', 'r') as file:
        preferenceData = json.load(file)
    return preferenceData

# Function to write preferences to the JSON file
def writeFile(jsonData):
    with open('preferences.json', 'w') as file:
        json.dump(jsonData, file, indent=2)

try:
    # Try reading preferences from the file
    jsonData = readFile()
    # default resolution saved in preferences file
    resolution = jsonData['resolution']
    firstTimeValue = jsonData['firstTime']
    jsonFileFound = TRUE
except:
    # If there's an exception, show an error message
    messagebox.showerror('Python Error', 'Critical Root Error Occurred, Package preferences.json not found. Please '
                                         'download file or fully re-install program')

# Check if the preferences file was found
if (jsonFileFound == TRUE):
    # Create the main Tkinter window
    root = Tk()
    root.geometry('500x300')
    root.resizable(False, False)
    root.title("Youtube Downloader")
    Label(root, text='Youtube Video Downloader', font='arial 20 bold').pack()

    # Initialize a StringVar for the YouTube link
    link = StringVar()
    Label(root, text='Paste Link Here:', font='arial 15 bold').place(x=160, y=60)
    Entry(root, width=70, textvariable=link).place(x=32, y=90)
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.place(x=50, y=200)

    # Function to paste the link from the clipboard
    def paste():
        link.set(root.clipboard_get())

    # Function to clear the entry textbox
    def clear():
        link.set("")

    # Buttons for pasting and clearing the link
    Button(root, text='Paste From Clipboard', bg='#83FF7F', padx=2, command=paste).place(x=50, y=120, width=200)
    Button(root, text='Clear Textbox', bg='#FF7F7F', padx=2, command=clear).place(x=250, y=120, width=200)

    # Function for the downloading label
    def downloading(progress_bar):
        Label(root, text='D O W N L O A D I N G', font='arial 15').place(x=140, y=230)
        progress_bar["value"] = 40
        root.update_idletasks()

    # Function to handle the downloading process
    def Downloader(progress_bar, jsonData):
        url = YouTube(str(link.get()))
        getLength(url, jsonData)

        video = url.streams.filter(res=resolution).first()

        # Function to download the video in a new thread
        def downloadVideo():
            video.download("downloads/")

        # download the video using a new thread to prevent tkinter from being unresponsive
        t = threading.Thread(target=downloadVideo)
        t.start()

        progress_bar["value"] = 100
        Label(root, text='D O W N L O A D E D !', font='arial 15').place(x=140, y=230)
        root.update_idletasks()

    # Function to get the length of the video and update preferences
    def getLength(url, jsonData):
        length = (url.length / 3600)
        jsonData['totalHours'] += length
        jsonData['totalVideo'] += 1
        writeFile(jsonData)

    # Function to open a new window for advanced features
    def openNewWindow(jsonData):
        newWindow = Toplevel(root)
        newWindow.title("Advanced Features")
        newWindow.geometry("500x300")
        newWindow.grab_set()

        # Function to save changes in the new window
        def save():
            newWindow.grab_release()
            writeFile(jsonData)
            newWindow.destroy()

        # Bind the save function to the window close event
        newWindow.protocol("WM_DELETE_WINDOW", save)

        # Function to handle the selection of video resolution in the new window
        def sel():
            selection = str(var.get())
            if selection == "1":
                jsonData['resolution'] = "144p"
            elif selection == "2":
                jsonData['resolution'] = "240p"
            elif selection == "3":
                jsonData['resolution'] = "360p"
            elif selection == "4":
                jsonData['resolution'] = "480p"
            elif selection == "5":
                jsonData['resolution'] = "720p"
            else:
                messagebox.showerror('Python Error', 'Critical Root Error Occurred, Please Restart Program')

        # Initialize a variable for the radio buttons
        var = IntVar()
        var.set(1)

        # Create radio buttons for different resolutions
        Radiobutton(newWindow, text="144p", variable=var, value=1, command=sel).place(x=20, y=20)
        Radiobutton(newWindow, text="240p", variable=var, value=2, command=sel).place(x=20, y=50)
        Radiobutton(newWindow, text="360p", variable=var, value=3, command=sel).place(x=20, y=80)
        Radiobutton(newWindow, text="480p", variable=var, value=4, command=sel).place(x=20, y=110)
        Radiobutton(newWindow, text="720p", variable=var, value=5, command=sel).place(x=20, y=140)
        Label(newWindow, text='Changes will be saved upon closing this window and changes are persistent.',
              font='arial 9').place(x=20, y=190)
        sel()

    # Button to initiate the download process
    Button(root, text='DOWNLOAD', bg='light blue', padx=2,
           command=lambda: [downloading(progress_bar), Downloader(progress_bar, jsonData)]) \
        .place(x=50, y=150, width=400, height=50)

    # Button to open the advanced features window
    Button(root, text="Advanced Features", command=lambda: [openNewWindow(jsonData)], bg="#FD9600") \
        .place(x=10, y=270)

# Check if it's the first time running the program
if firstTimeValue == 0:
    # Function for the first-time terms of service window
    def firstTime(jsonData):
        localFirstTimeValue = firstTimeValue
        firstTimeWindow = Toplevel(root)
        screen_width = firstTimeWindow.winfo_screenwidth()
        screen_height = firstTimeWindow.winfo_screenheight()
        width = 500
        height = 300
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        # Set the geometry of the window
        firstTimeWindow.geometry(f"{width}x{height}+{x}+{y}")

        firstTimeWindow.title("Terms Of Service")
        firstTimeWindow.geometry("300x300")
        firstTimeWindow.grab_set()
        Label(firstTimeWindow, text='Terms Of Service', font='arial 15').place(x=70, y=5)

        terms_text = (
            "By using this program you hereby agree to use it in acceptance to Youtube's terms of service. "
            "I, Mr-VL, am not responsible for the actions you perform while using this program. "
            "This program was created as a functional demonstration and shall be used in accordance and "
            "following proper guidelines and not breaking any laws."
        )

        Label(firstTimeWindow, text=terms_text, font='arial 10', justify='left', wraplength=280).place(x=10, y=30)

        # Button to accept the terms
        Button(firstTimeWindow, text="Accept", command=lambda: [saveCheck(jsonData, 1)], bg="#66ed7d", width=18) \
            .place(x=5, y=170)

        # Button to decline and exit the program
        Button(firstTimeWindow, text="Decline", command=lambda: [saveCheck(jsonData, 0)], bg="#f74d4d",
               width=18) \
            .place(x=150, y=170)

        # Function to save the user's choice and close the first-time window

        def saveCheck(jsonData, val):
            jsonData['firstTime'] = val
            writeFile(jsonData)
            firstTimeWindow.destroy()

            # If declined, exit the program
            if val == 0:
                root.destroy()
                messagebox.showerror('Python Error', 'ERROR: YOU MUST AGREE TO TERMS AND CONDITIONS TO CONTINUE '
                                                     'PLEASE RE-RUN PROGRAM AND READ AND ACCEPT IN ORDER TO CONTINUE')

        firstTimeWindow.protocol("WM_DELETE_WINDOW", lambda: saveCheck(jsonData, localFirstTimeValue))


    # Call the firstTime function
    firstTime(jsonData)

# Start the Tkinter main loop
root.mainloop()
