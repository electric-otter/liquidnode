import tkinter as tk
import subprocess
import threading
import webbrowser
import os

# Create the main window
window = tk.Tk()
window.title("LiquidNode")
window.geometry("500x400")

# Label for status updates
status_label = tk.Label(window, text="Click to create a server.", font=("Arial", 12), fg="black")
status_label.pack(pady=10)

# Function to create and start the server
def server_make():
    def run_docker():
        try:
            status_label.config(text="Creating server...", fg="blue")
            window.update_idletasks()

            # Ensure the Dockerfile is created in the current working directory
            dockerfile_path = "ubuntu.dockerfile"
            with open(dockerfile_path, "w") as file:
                file.write("""\
# This is a Dockerfile for Ubuntu
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""")

            # Verify the Dockerfile exists before proceeding
            if not os.path.exists(dockerfile_path):
                status_label.config(text="Dockerfile not found!", fg="red")
                return

            # Build Docker image
            subprocess.run(["docker", "build", "-t", "new-server", "."], check=True)
            # Run Docker container
            subprocess.run(["docker", "run", "-d", "-p", "8080:80", "--name", "liquid_server", "new-server"], check=True)

            status_label.config(text="Server started successfully on port 8080!", fg="green")
            open_browser_button.config(state="normal")  # Enable the Open Browser button
            command_entry.config(state="normal")  # Enable the command input
            run_command_button.config(state="normal")  

        except subprocess.CalledProcessError as e:
            status_label.config(text=f"Error: {e}", fg="red")
        except Exception as e:
            status_label.config(text=f"Unexpected error: {e}", fg="red")

    threading.Thread(target=run_docker, daemon=True).start()

# Function to open localhost in the browser
def open_browser():
    webbrowser.open("http://localhost:8080")

# Function to run a command inside the Docker container
def run_command():
    command = command_entry.get()
    if command:
        try:
            result = subprocess.run(["docker", "exec", "liquid_server", "bash", "-c", command], capture_output=True, text=True, check=True)
            output_label.config(text=f"Output:\n{result.stdout}", fg="black")
        except subprocess.CalledProcessError as e:
            output_label.config(text=f"Error: {e.stderr}", fg="red")

# Create the server button
create_server_button = tk.Button(window, text="Create a Server", command=server_make)
create_server_button.pack(pady=10)

# Create a button to open the server in a browser
open_browser_button = tk.Button(window, text="Open Server in Browser", command=open_browser, state="disabled")
open_browser_button.pack(pady=5)

# Input field for commands
command_label = tk.Label(window, text="Enter command for server:", font=("Arial", 10))
command_label.pack()

command_entry = tk.Entry(window, width=40, state="disabled")
command_entry.pack(pady=5)

# Button to run the entered command
run_command_button = tk.Button(window, text="Run Command", command=run_command, state="disabled")
run_command_button.pack(pady=5)

# Label to show command output
output_label = tk.Label(window, text="", font=("Arial", 10), fg="black", wraplength=400, justify="left")
output_label.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()

