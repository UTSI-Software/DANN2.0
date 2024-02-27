#!/usr/bin/env python
import os
import time
import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
import pdfquery
import PyPDF2

def traverse_network_directory(network_dir_path):
    start_time = time.time()
    count_dirs = count_files = total_dirs = total_files = 0
    for root, dirs, files in os.walk(network_dir_path):
        print(f"Entering directory: {root}")
        print("-"*100)
        for file in files:
            count_files += 1
            print(f"File: {os.path.join(root, file)}")
        total_files += count_files
        for dir in dirs:
            count_dirs += 1
            print(f"Directory: {os.path.join(root, dir)}")
        total_dirs += count_dirs
        print(f"Total directories: {count_dirs}")
        print(f"Total files: {count_files}")
        print("#" * 100)
        count_dirs = count_files = 0
    
    end_time = time.time()
    print(f"Total directories: {total_dirs}")
    print(f"Total files: {total_files}")
    
    print(f"Total time taken: {(end_time - start_time)/60} seconds")

def print_tree(self, directory, prefix=''):
    files = []
    output = ""
    if os.path.isdir(directory):
        files = os.listdir(directory)
    files.sort()
    for i, file in enumerate(files):
        path = os.path.join(directory, file)
        is_last = i == len(files) - 1
        output += f"{prefix}{'└── ' if is_last else '├── '}{file}\n"
        if os.path.isdir(path):
            new_prefix = prefix + ('    ' if is_last else '│   ')
            output += self.print_tree(path, new_prefix)
    return output

def run_functions_on_directory(directory):
    pass
    
    #output = print_tree(directory)
    #return output


#########################
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1000x500")
        self.createWidgets()
    
    def createWidgets(self):
        # Quit button
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=0, sticky="ew")

        # Directory selection button
        self.select_button = tk.Button(self, text="Select Directory", command=self.select_directory)
        self.select_button.grid(row=1, column=0, pady=10, sticky="ew")

        # Label to display selected directory
        self.directory_label = tk.Label(self, text="No Directory Selected")
        self.directory_label.grid(row=2, column=0, pady=5)

        # Text widget to display output
        self.output_text = Text(self, height=20, width=50)
        self.output_text.grid(row=3, column=0, pady=10)

        # TextBox Creation 
        path_text = Text(self, height = 5, width = 20)
        path_text.pack()
        path = path_text.get(1.0, "end-1c")


    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_label.config(text=f"Selected Directory: {directory}")
            self.output_text.delete('1.0', tk.END)
            output = self.run_functions_on_directory(directory)
            self.output_text.insert(tk.END, output)


def main():
    root = tk.Tk()
    root.title('DANN 2.0 Path Selector')
    app = Application(master=root)
    app.grid(sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app.mainloop()

if __name__ == "__main__":
    main()