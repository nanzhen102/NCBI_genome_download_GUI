# Aim: interage ncbi-genome-download with GUI
# Name: NCBI Genome Download GUI

import tkinter as tk
import subprocess

class GenomeDownloadGUI:
    def __init__(self, master):
        self.master = master # specify which window the GUI elements will be placed in - master
        master.title("NCBI Genome Download GUI")
        master.geometry("365x280") # set the size of the window (pixels)

        # enter genus 
        self.genus_label = tk.Label(master, text="Enter genus name (e.g., Fructilactobacillus):") # The first label to remind the input 
        self.genus_label.grid(row=0, column=0, sticky="W", padx=40, pady=2) # pack the label widget into the parent widget

        self.genus_entry = tk.Entry(master, width=30)
        self.genus_entry.grid(row=1, column=0, padx=40, pady=2)

        # select format 
        self.format_label = tk.Label(master, text="Select format:")
        self.format_label.grid(row=2, column=0, sticky="W", padx=40, pady=2)

        self.format_var = tk.StringVar(master)
        self.format_var.set("fasta")  # Default format
        self.format_menu = tk.OptionMenu(master, self.format_var, "fasta", "GenBank", "All")
        self.format_menu.grid(row=3, column=0, sticky="W", padx=40, pady=2)

        # save as
        self.save_frame = tk.Frame(master) # `frame` can group two button widgets together
        self.save_frame.grid(row=4, column=0, pady=5)   

        self.save_button = tk.Button(self.save_frame, text="Save as:")
        self.save_button.pack(side="left", padx=2)
        self.save_entry = tk.Entry(self.save_frame, text="Save as:")
        self.save_entry.pack(side="right", padx=2)        

        # check ACC numbers by the dry run
        self.check_button = tk.Button(master, text="Check collected ACC numbers", command=self.dryrun)
        self.check_button.grid(row=6, column=0, padx=40, pady=5)

        # download
        self.download_button = tk.Button(master, text="Download", font=("Arial Bold", 13), command=self.download)
        self.download_button.grid(row=7, column=0, padx=40, pady=5)

        # personal information
        self.info_label = tk.Label(master, text="nanzhen.qiao@gmail.com \n Version 1. 10 Mar 2023") 
        self.info_label.grid(row=8, column=0, padx=40, pady=10)

    def dryrun(self): 
        genus = self.genus_entry.get() # Retrieve the user input
        format = self.format_var.get()    
        output_folder = "/Users/nanzhen"
        output_check_file = "/Users/nanzhen/check.txt"
        cmd = ["ncbi-genome-download", "--genera", genus, "--formats", format, "--parallel", "4", "--dry-run", "--output-folder", output_folder, "bacteria"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"An error occurred: {stderr.decode()}")
        else:
            with open(output_check_file, "w") as f:
                f.write(stdout.decode())
            print(f"Command executed successfully. Output written to {output_check_file}")

    def download(self):
        genus = self.genus_entry.get() # Retrieve the user input
        format = self.format_var.get()
        process = subprocess.Popen(["ncbi-genome-download", "--genera", genus, "--formats", format, "--parallel 4"])
        return_code = process.wait() # Wait for the process to finish and get its return code
        if return_code == 0:
            print(f"Genome of {genus} downloaded successfully.")
        else:
            print("An error occurred while downloading the genome.")

root = tk.Tk()
gui = GenomeDownloadGUI(root)
root.mainloop()