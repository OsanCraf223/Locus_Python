# Import necessary modules from tkinter for GUI components and file dialogs
from tkinter import *
from tkinter import scrolledtext, filedialog
from tkinter import PhotoImage

# ----------------------- Function Definitions -----------------------

def new_file():
    """Clears the text box to start a new file."""
    txtbox.delete("1.0", END)

def open_file():
    """Opens a file dialog and loads selected file contents into the text box."""
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=[
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("Python Files", "*.py"),
            ("Java Files", "*.java"),
            ("HTML Files", "*.html"),
            ("CSV Files", "*.csv"),
        ]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            txtbox.delete("1.0", END)
            txtbox.insert(END, content)

def save_file():
    """Opens a save dialog and writes the text box contents to the chosen file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".lcs",
        filetypes=[("LCS Files", "*.lcs"), ("All Files", "*.*")],
        title="Save As"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(txtbox.get("1.0", END))

def show_about():
    """Displays an About dialog."""
    from tkinter import messagebox
    messagebox.showinfo(
        "About",
        "Locus_Python\nA simple text editor to save and open files.\nBy OsanCraf223"
    )

# ---------------------- Main Window Setup -----------------------

master_window = Tk()

# Set application icon (requires locusImage.png in the same directory)
try:
    icon = PhotoImage(file="locusImage.png")
    master_window.iconphoto(False, icon)
except Exception:
    pass  # If the icon is missing, ignore the error

master_window.title("Enhanced Text Viewer")
master_window.geometry("700x500")

# ------------------------ Text Box Setup ------------------------

txtbox = scrolledtext.ScrolledText(master_window, width=80, height=25, font=("Consolas", 12))
txtbox.grid(row=0, column=0, sticky=N+S+E+W)

master_window.grid_rowconfigure(0, weight=1)
master_window.grid_columnconfigure(0, weight=1)

# ------------------------ Menu Bar Setup ------------------------

menu = Menu(master_window)
master_window.config(menu=menu)

# ------------------------ File Menu ------------------------

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New', command=new_file)
filemenu.add_command(label='Open...', command=open_file)
filemenu.add_separator()
filemenu.add_command(label='Save As...', command=save_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=master_window.quit)

# ------------------------ Help Menu ------------------------

helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=show_about)

# -------------------- Main Event Loop ----------------------

master_window.mainloop()
