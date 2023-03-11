#!/usr/bin/env python
# Aim: interage ncbi-genome-download with GUI
# Written by: Nanzhen   nanzhen.qiao@gmail.com
# Version 1.0.0 10 Mar 2023

import tkinter as tk
import subprocess, os
from tkinter import filedialog

class GenomeDownloadGUI:
    def __init__(self, master):
        self.master = master # specify which window the GUI elements will be placed in - master
        master.title("NCBI Genome Download GUI")
        master.geometry("370x400") # set the size of the window (pixels)

        # enter genus 
        self.genus_label = tk.Label(master, text="Enter genus name (e.g., Fructilactobacillus):") # The first label to remind the input 
        self.genus_label.grid(row=0, column=0, sticky="W", padx=40, pady=2) # pack the label widget into the parent widget

        self.genus_entry = tk.Entry(master, width=30)
        self.genus_entry.grid(row=1, column=0, padx=40, pady=2)

        # select format 
        self.format_frame = tk.Frame(master)
        self.format_frame.grid(row=2, column=0, pady=5)

        self.format_label = tk.Label(self.format_frame, text="Select format:")
        self.format_label.pack(side="left", padx=2)

        self.format_var = tk.StringVar(self.format_frame)
        self.format_var.set("fasta") # Default format
        self.format_menu = tk.OptionMenu(self.format_frame, self.format_var, "fasta", "GenBank", "All")
        self.format_menu.pack(side="right", padx=55)

        # save to
        self.save_frame = tk.Frame(master) # `frame` can group two button widgets together
        self.save_frame.grid(row=4, column=0, pady=5)   

        self.save_button = tk.Button(self.save_frame, text="Save to:", command = self.savepath)
        self.save_button.pack(side="left", padx=2)

        self.save_entry = tk.Entry(self.save_frame, text="Save to:")
        self.save_entry.pack(side="right", padx=2)        

        # check ACC numbers by the dry run
        self.check_button = tk.Button(master, text="Check collected ACC numbers", command=self.dryrun)
        self.check_button.grid(row=6, column=0, padx=40, pady=10, sticky="EW")

        # download
        self.download_button = tk.Button(master, text="Download", font=("Arial Bold", 13), command=self.download)
        self.download_button.grid(row=7, column=0, padx=40, pady=10, sticky="EW")

        # process output
        self.process_txt = tk.Text(master, width=40, height=7, bg="#FFCC66", fg="black") # hex color code
        self.process_txt.grid(row=8, column=0, padx=40, pady=10)
        self.process_txt.insert(tk.END, "log:\n")

        # personal information
        self.info_label = tk.Label(master, text="nanzhen.qiao@gmail.com \n Version 1.0.0 10 Mar 2023") 
        self.info_label.grid(row=14, column=0, padx=40, pady=15)

    def savepath(self):
        file_path = filedialog.askdirectory()
        self.save_entry.insert(0,file_path)

    def dryrun(self): 
        genus = self.genus_entry.get() # Retrieve the user input
        format = self.format_var.get()    
        output_folder = self.save_entry.get()
        output_check_file = os.path.join(output_folder, "check_acc.txt")
        cmd = ["ncbi-genome-download", "--genera", genus, "--formats", format, "--parallel", "2", "--dry-run", "--output-folder", output_folder, "bacteria"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            self.process_txt.insert(tk.End, f"An error occurred: {stderr.decode()}\n")
            # print(f"An error occurred: {stderr.decode()}")
        else:
            with open(output_check_file, "w") as f:
                f.write(stdout.decode())
            self.process_txt.insert(tk.END, f"Command executed successfully. Output written to {output_check_file}\n")

    def download(self):
        genus = self.genus_entry.get() # Retrieve the user input
        format = self.format_var.get()
        output_folder = self.save_entry.get()
        self.process_txt.insert(tk.END, f"\nGenome of {genus} is downloading.......(the window might be frozen)\n")
        cmd = ["ncbi-genome-download", "-g", genus, "--formats", format, "-o", output_folder, "--parallel", "2", "bacteria"]
        process = subprocess.Popen(cmd)
        return_code = process.wait() # Wait for the process to finish and get its return code
        if return_code == 0:
            self.process_txt.insert(tk.END, f"Genome of {genus} downloaded successfully to {output_folder}.\n")
        else:
            self.process_txt.insert(tk.END, "An error occurred while downloading the genome.")
            
root = tk.Tk()
gui = GenomeDownloadGUI(root)
root.mainloop()