import tkinter as tk

root = tk.Tk()

# create a label widget and place it in row 0, column 0
label1 = tk.Label(root, text="Username:")
label1.grid(row=0, column=0, sticky="E") # East - right side of the cell

# create an entry widget and place it in row 0, column 1
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=10) # specify the amount of padding (in pixels) to be added to the widget along the X and Y axes,

# create another label widget and place it in row 1, column 0
label2 = tk.Label(root, text="Password:")
label2.grid(row=1, column=0, sticky="E")

# create a password entry widget and place it in row 1, column 1
entry2 = tk.Entry(root, show="*")
entry2.grid(row=1, column=1, padx=10, pady=10)

# create a checkbutton widget and place it in row 2, column 1
checkbutton1 = tk.Checkbutton(root, text="Remember me")
checkbutton1.grid(row=2, column=1, sticky="W")

# create a frame widget and place it in row 3, column 1
frame1 = tk.Frame(root) # `frame` can group two button widgets together
frame1.grid(row=3, column=1, pady=10)

# create two button widgets and place them inside the frame
button1 = tk.Button(frame1, text="Cancel")
button1.pack(side="left", padx=5)
button2 = tk.Button(frame1, text="Login", bg="green", fg="white")
button2.pack(side="right", padx=5)

root.mainloop()
