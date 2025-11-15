from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import random

root = Tk()
root.title("Alexa Joke Telling Assistant")
root.geometry("800x650")

# A frame for the start screen
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)

# Gif for background
bg_image = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\background 4.gif")
frames = [ImageTk.PhotoImage(frame.copy().resize((800, 650))) for frame in ImageSequence.Iterator(bg_image)]
bg_label = Label(main_frame)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Animate GIF
def animate(index=0):
    bg_label.config(image=frames[index])
    root.after(400, animate, (index + 1) % len(frames))
animate(0)

# Empty lists to store setups and punchlines
setups = []
punchlines = []

# Reading jokes from file
with open("randomJokes.txt") as file_handler:
    lines = file_handler.readlines()

for l in lines:
    if "?" in l:
        data = l.strip().split("?", 1)
        setups.append(data[0] + "?")
        punchlines.append(data[1])

current_index = [0]

# Enhanced Title with shadow effect
title_frame = Frame(main_frame, bg="", bd=1, relief=RIDGE)
title_frame.place(relx=0.5, rely=0.26, anchor="center")
title_label = Label(title_frame, font=("Comic Sans MS", 18, "bold"),fg="#ff4500", bg="#ffffff",padx=15, pady=6)
title_label.pack()

# Enhanced joke display area with rounded look
joke_display_frame = Frame(main_frame, bg="#817d7d", bd=5, relief=GROOVE)
joke_display_frame.place(relx=0.5, rely=0.33, anchor="n", width=450, height=100)
setup_label = Label(joke_display_frame, text="",wraplength=450,font=("Arial", 16, "bold"),fg="#ffffff", bg="#817d7d", pady=20)
setup_label.pack(expand=True)
punchline_label = Label(joke_display_frame, text="",wraplength=450,font=("Arial", 13, "italic"),fg="#880c4e", bg="#817d7d")
punchline_label.pack(expand=True)

# Functions
def tell_joke():
    if setups:
        current_index[0] = random.randint(0, len(setups) - 1)
        setup_label.config(text=setups[current_index[0]], font=("Arial", 18, "bold"))
        punchline_label.config(text="")

def show_punchline():
    if punchlines:
        punchline_label.config(text=punchlines[current_index[0]])

def quit_app():
    root.destroy()

# Button frames and buttons with enhanced styling
button_width = 220
button_height = 70

# Tell Joke Button
tell_btn_frame = Frame(main_frame, bg="#6200FF", bd=3, relief=RAISED)
tell_btn_frame.place(relx=0.25, rely=0.75, anchor="center")
tell_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\button 1.png").resize((button_width, button_height)))
tell_btn = Button(tell_btn_frame, image=tell_btn_img, command=tell_joke,borderwidth=0, cursor="hand2",bg="#6200FF", activebackground="#6200FF")
tell_btn.image = tell_btn_img 
tell_btn.pack()

# Show Punchline Button
punchline_btn_frame = Frame(main_frame, bg="#23751C", bd=3, relief=RAISED)
punchline_btn_frame.place(relx=0.75, rely=0.75, anchor="center")
punchline_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\button 2.png").resize((button_width, button_height)))
punchline_btn = Button(punchline_btn_frame, image=punchline_btn_img, command=show_punchline,borderwidth=3, cursor="hand2",bg="#23751C", activebackground="#23751C")
punchline_btn.image = punchline_btn_img
punchline_btn.pack()

# Next Joke Button
next_btn_frame = Frame(main_frame, bg="#FFF454", bd=3, relief=RAISED)
next_btn_frame.place(relx=0.25, rely=0.88, anchor="center")
next_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\button 3.png").resize((button_width, button_height)))
next_btn = Button(next_btn_frame, image=next_btn_img, command=tell_joke,borderwidth=0, cursor="hand2",bg="#FFF454", activebackground="#FFF454")
next_btn.image = next_btn_img
next_btn.pack()

# Quit Button
quit_btn_frame = Frame(main_frame, bg="#FF3E3E", bd=3, relief=RAISED)
quit_btn_frame.place(relx=0.75, rely=0.88, anchor="center")
quit_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\button 4.png").resize((button_width, button_height)))
quit_btn = Button(quit_btn_frame, image=quit_btn_img, command=quit_app,borderwidth=0, cursor="hand2",bg="#FF3E3E", activebackground="#FF3E3E")
quit_btn.image = quit_btn_img
quit_btn.pack()

root.mainloop()