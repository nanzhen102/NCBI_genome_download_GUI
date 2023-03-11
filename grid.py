import tkinter as tk

root = tk.Tk() # create a Tk object

# create a label widget and place it in row 0, column 0
label1 = tk.Label(root, text="Label 1")
label1.grid(row=0, column=0)

# create a button widget and place it in row 1, column 0
button1 = tk.Button(root, text="Button 1")
button1.grid(row=1, column=0)

# create another label widget and place it in row 0, column 1
label2 = tk.Label(root, text="Label 2")
label2.grid(row=0, column=1)

# create another button widget and place it in row 1, column 1
button2 = tk.Button(root, text="Button 2")
button2.grid(row=1, column=1)

root.mainloop() # run the GUI event loop
