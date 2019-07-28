import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import constants

class Menubar:

    def __init__(self, parent):
        font_specs = ("ubuntu", 10)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File",
                                accelerator="Ctrl+N",
                                command=parent.new_file)
        file_dropdown.add_command(label="Open File",
                                accelerator="Ctrl+O",
                                command=parent.open_file)
        file_dropdown.add_command(label="Save",
                                accelerator="Ctrl+S",
                                command=parent.save)
        file_dropdown.add_command(label="Save As",
                                accelerator="Ctrl+Shift+S",
                                command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit",
                                command=parent.master.destroy)
        
        edit_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        edit_dropdown.add_command(label="Cut", 
                                accelerator="Ctrl+X", 
                                command=parent.cut) 
                        
        edit_dropdown.add_command(label="Copy", 
                                accelerator="Ctrl+C", 
                                command=parent.copy)

        edit_dropdown.add_command(label="Paste", 
                                accelerator="Ctrl+V", 
                                command=parent.paste)


        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes",
                                command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About",
                                command=self.show_about_message)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="Edit", menu=edit_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)

    def show_about_message(self):
        box_title = "About SnakeEditor"
        box_message = "A simple Python-made text editor."
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 1.0 - Created by Enrico Maietti"
        messagebox.showinfo(box_title, box_message)

class SnakeEditor:

    def __init__(self, master):
        master.title("Untitled - SnakeEditor")
        master.geometry("1200x700")

        font_specs = ("ubuntu", 18)

        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        
        self.bind_shortcuts()

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - SnakeEditor")
        else:
            self.master.title("Untitled - SnakeEditor")

    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("C++ Scripts", "*.cpp"),
                       ("C Scripts", "*.c"),
                       ("Python Scripts", "*.py"),
                       ("Markdown Documents", "*.md"),
                       ("JavaScript Files", "*.js"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css")])
        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            self.set_window_title(self.filename)
    
    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                        ("Text Files", "*.txt"),
                        ("C++ Scripts", "*.cpp"),
                        ("C Scripts", "*.c"),
                        ("Python Scripts", "*.py"),
                        ("Markdown Documents", "*.md"),
                        ("JavaScript Files", "*.js"),
                        ("HTML Documents", "*.html"),
                        ("CSS Documents", "*.css")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
        except Exception as e:
            print(e)

    def copy(self):
        self.textarea.clipboard_clear()
        self.textarea.clipboard_append(self.textarea.selection_get())

    def cut(self):
        self.copy()
        self.textarea.delete("sel.first", "sel.last")
    
    def paste(self):
        self.textarea.insert(tk.constants.INSERT, self.textarea.clipboard_get())
        

    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
      


if __name__ == "__main__":
    master = tk.Tk()
    pt = SnakeEditor(master)
    master.mainloop()