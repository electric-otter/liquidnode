import tkinter as tk
import subprocess

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
        with open("ubuntu.dockerfile", "w") as file:
            file.write("# This is a Dockerfile for Ubuntu\n")
            file.write("FROM ubuntu:latest\n")
            file.write("RUN apt-get update\n")
            file.write("RUN apt-get install -y nginx\n")
            file.write("EXPOSE 80\n")
            file.write("CMD [\"nginx\", \"-g\", \"daemon off;\"]\n")
        print("Dockerfile created successfully.")
        subprocess.run(["docker", "build", "-t", "new-server", "."])
        subprocess.run(["docker", "run", "-d", "-p", "8080:80", "new-server"])
        print("Server started successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

button = tk.Button(window, text="Create a server.", command=server_make)
button.pack()  # Add the button to the window

# Start the Tkinter event loop
window.mainloop()
