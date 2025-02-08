import tkinter as tk

# Create the main window
window = tk.Tk()

# Set the title of the window
window.title("LiquidNode")

# Set the size of the window (optional)
window.geometry("400x300")  # width x height

def server_make():
    print("Creating server!")
    label = tk.Label(window, text="Creating server!", font=("Arial", 14), fg="blue")
    label.pack()  # Add the label to the window
    try:
        with open("ubuntu.dockerfile", "r") as file:
            print(file.read())  # Read and print the contents of the file
    except FileNotFoundError:
        print("File not found. Did you delete server files?")

button = tk.Button(window, text="Create a server.", command=server_make)
button.pack()  # Add the button to the window

# Start the Tkinter event loop
window.mainloop()
