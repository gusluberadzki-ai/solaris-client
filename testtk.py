import tkinter as tk 
from tkinter import messagebox

TAB = tk.Tk()
TAB.title("Nuclear Launch Control")
TAB.geometry("600x400")

label = tk.Label(TAB, text=" if you press the button, you will doom the world",font=("Stencil",24,"bold"),fg = "Green")
label.pack(pady=30)

def Launch():
    messagebox.showinfo("messageThink", "You have launched the nuclear weapons!")

button = tk.Button(  
    TAB,
    text="LAUNCH",
    font=("Stencil",20,"bold"),
    bg="red",
    fg="white",
    height=2,
    command=Launch
)
button.pack()

TAB.mainloop()
