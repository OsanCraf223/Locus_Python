from tkinter import *
from tkinter import scrolledtext, filedialog
from tkinter import PhotoImage



#save fuction
def save_file():
    #assigns the custom extention to the Save As function
    file_path = filedialog.asksaveasfilename(
        defaultextension=".lcs",
        filetypes=[("LCS Files", "*.lcs"), ("All Files", "*.*")],
        title="Save As"
    )#if the filwe is writable it will  save the file
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(txtbox.get("1.0", END))
            

def open_file():
    
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
    )#if file is readable it will open in the text editor
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            txtbox.delete("1.0", END)
            txtbox.insert(END, content)
            
            


master_window = Tk()

#logo 
icon = PhotoImage(file="LocusImage.png")
master_window.iconphoto(False, icon)

master_window.title("Enhanced Text Viewer")

#set frame geometry
master_window.geometry("700x500")

# Add ScrolledText
txtbox = scrolledtext.ScrolledText(master_window, width=80, height=25, font=("Consolas", 12))
txtbox.grid(row=0, column=0, sticky=N+S+E+W)

# Configure window resizing
master_window.grid_rowconfigure(0, weight=1)
master_window.grid_columnconfigure(0, weight=1)

# Create menu bar
menu = Menu(master_window)
master_window.config(menu=menu)

# File menu
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Open...', command=open_file)
filemenu.add_separator()
filemenu.add_command(label='Save As...', command=save_file)
filemenu.add_command(label='Exit', command=master_window.quit)

# Help menu
helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')

master_window.mainloop()
