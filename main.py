import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import shutil
from io import BytesIO
import webbrowser
import os

def download_audio():
    try:
        number = entry.get()
        url = f"https://api.hyra.io/audio/{number}"
        response = requests.get(url)
        
        if response.status_code == 200:
            messagebox.showinfo("Success", "Audio downloaded successfully!")
            info_label.config(text=f"File Info:\nNumber: {number}\nSize: {len(response.content)} bytes")
            preview_button.config(state=tk.NORMAL)
            download_button.config(state=tk.NORMAL)
            
            file_path = os.path.abspath("downloaded_audio.mp3")
            with open(file_path, "wb") as file:
                file.write(response.content)
            return file_path
        else:
            messagebox.showerror("Error", "Failed to download audio. Please check the sound id and try again.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

def preview_audio():
    try:
        file_path = download_audio()
        if file_path:
            webbrowser.open("file://" + file_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during preview: {str(e)}")

def choose_download_location():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        download_audio()
        shutil.move("downloaded_audio.mp3", file_path)

window = tk.Tk()
window.title("Audio Download")

label = tk.Label(window, text="Enter the sound id:")
label.pack(pady=10)

entry = tk.Entry(window)
entry.pack(pady=10)

download_button = tk.Button(window, text="Download Audio", command=download_audio)
download_button.pack(pady=20)

info_label = tk.Label(window, text="File Info:")
info_label.pack(pady=10)

preview_button = tk.Button(window, text="Preview Audio", command=preview_audio, state=tk.DISABLED)
preview_button.pack(pady=10)

download_button = tk.Button(window, text="Download File", command=choose_download_location, state=tk.DISABLED)
download_button.pack(pady=10)

window.mainloop()
