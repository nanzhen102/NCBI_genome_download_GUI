# AIM: interage ncbi-genome-download with GUI
# Name: HappyGenomes

import tkinter as tk

try:        
    window = tk.Tk() # create the main window

    frame = tk.Frame()

    label = tk.Label(
        master=frame,
        text = "You can do it!!!!",
        foreground = "white",
        background="orange",
        width=15,
        height=2) # create a label widget
    
    button = tk.Button(
        text="First step: choose one.",
        fg="orange")
    
    entry = tk.Entry(
        fg="black",
        bg="yellow",
        width=20
    )
    
    frame.pack()
    label.pack() # add widgets to the window
    button.pack()
    entry.pack()

    ACC_num = entry.get()
    print(ACC_num)

    window.title("HappyGenomes")
    window.mainloop() # start the GUI event loop

except Exception as e:
    print("An error occurred:", e)