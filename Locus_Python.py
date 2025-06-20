# Import necessary modules from tkinter for GUI components and file dialogs
from tkinter import *
from tkinter import scrolledtext, filedialog
from tkinter import PhotoImage

# ----------------------- Function Definitions -----------------------

# Function to save the contents of the text box to a file
def save_file():
    # Opens a Save As dialog with a custom extension (.lcs) and filters
    file_path = filedialog.asksaveasfilename(
        defaultextension=".lcs",
        filetypes=[("LCS Files", "*.lcs"), ("All Files", "*.*")],
        title="Save As"
    )
    # If the user selects a file, write the contents of the text box to the chosen file
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            # Get all text from the text box and write it to the file
            file.write(txtbox.get("1.0", END))

# Function to open a file and display its contents in the text box
def open_file():
    # Opens an Open File dialog allowing various file types
    file_path = filedialog.askopenfilename(
        title="Open File", 
        filetypes=[
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Python Files", "*.py"),
            ("Java Files", "*.java"),
            ("HTML Files", "*.html"),
            ("CSV Files", "*.csv")
        ]
    )
    # If the user selects a file, read its content and display it in the text box
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            # Clear the current contents of the text box
            txtbox.delete("1.0", END)
            # Insert the file's content into the text box
            txtbox.insert(END, content)

# ---------------------- Main Window Setup -----------------------

# Create the main application window
master_window = Tk()

# Set application icon (requires LocusImage.png in the same directory)
icon = PhotoImage(file="LocusImage.png")
master_window.iconphoto(False, icon)

# Set the window title
master_window.title("Enhanced Text Viewer")

# Set the initial size of the window
master_window.geometry("700x500")

# ------------------------ Text Box Setup ------------------------

# Create a ScrolledText widget (a text box with a vertical scrollbar)
txtbox = scrolledtext.ScrolledText(master_window, width=80, height=25, font=("Consolas", 12))
# Place the widget in the window using grid layout, making it fill all available space
txtbox.grid(row=0, column=0, sticky=N+S+E+W)

# Allow the text box to expand when the window is resized
master_window.grid_rowconfigure(0, weight=1)
master_window.grid_columnconfigure(0, weight=1)

# ------------------------ Menu Bar Setup ------------------------

# Create the menu bar and attach it to the main window
menu = Menu(master_window)
master_window.config(menu=menu)

# ------------------------ File Menu ------------------------

# Create the File menu within the menu bar
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=filemenu)

# Add menu items to the File menu
filemenu.add_command(label='New')  # Creates a new file (currently not implemented)
filemenu.add_command(label='Open...', command=open_file)  # Opens an existing file
filemenu.add_separator()  # Adds a separator line
filemenu.add_command(label='Save As...', command=save_file)  # Saves the current content to a file
filemenu.add_command(label='Exit', command=master_window.quit)  # Closes the application

# ------------------------ Help Menu ------------------------

# Create the Help menu within the menu bar
helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=helpmenu)

# Add an About item (currently not implemented)
helpmenu.add_command(label='About')

# -------------------- Main Event Loop ----------------------

# Start the Tkinter event loop (keeps the window open and responsive)
master_window.mainloop()
