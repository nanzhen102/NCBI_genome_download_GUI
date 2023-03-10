# Aim: interage ncbi-genome-download with GUI
# Name: NCBI Genome Download GUI

import tkinter as tk
import subprocess

class GenomeDownloadGUI:
    def __init__(self, master):
        self.master = master # specify which window the GUI elements will be placed in - master
        master.title("NCBI Genome Download GUI")
        master.geometry("400x310") # set the size of the window (pixels)

        # select the genus 
        self.genus_label = tk.Label(master, text="Enter genus name (e.g., Fructilactobacillus):") # The first label to remind the input 
        self.genus_label.pack() # pack the label widget into the parent widget

        self.genus_entry = tk.Entry(master, width=30)
        self.genus_entry.pack()

        # select the format 
        self.genus_label = tk.Label(master, text="") # create a blank label
        self.genus_label.pack()

        self.format_label = tk.Label(master, text="Select format to download:")
        self.format_label.pack()

        self.format_var = tk.StringVar(master)
        self.format_var.set("fasta")  # Default format
        self.format_menu = tk.OptionMenu(master, self.format_var, "fasta", "GenBank", "All")
        self.format_menu.pack()

        # check ACC numbers by the dry run
        self.genus_label = tk.Label(master, text="") # create a blank label
        self.genus_label.pack()

        self.download_button = tk.Button(master, text="Check collected \n ACC numbers", command=self.dryrun)
        self.download_button.pack()

        # download
        self.genus_label = tk.Label(master, text="") # create a blank label
        self.genus_label.pack()

        self.download_button = tk.Button(master, text="Download \n Genomes", font=("Arial Bold", 14), command=self.download)
        self.download_button.pack()

        # my information
        self.genus_label = tk.Label(master, text="") # create a blank label
        self.genus_label.pack()

        self.genus_label = tk.Label(master, text="Nanzhen \n nanzhen.qiao@gmail.com") 
        self.genus_label.pack() 

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
        p = subprocess.Popen(["ncbi-genome-download", "--genera", genus, "--formats", format, "--parallel 4"])
        return_code = p.wait() # Wait for the process to finish and get its return code
        if return_code == 0:
            print(f"Genome of {genus} downloaded successfully.")
        else:
            print("An error occurred while downloading the genome.")

root = tk.Tk()
gui = GenomeDownloadGUI(root)
root.mainloop()