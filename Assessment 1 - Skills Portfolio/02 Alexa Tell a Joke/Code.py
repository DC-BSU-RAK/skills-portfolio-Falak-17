from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random
import pygame

root = Tk()
root.title("Alexa Joke Telling Assistant")
root.geometry("1150x730")
root.resizable(FALSE, FALSE)

# Dictionary to hold all sounds
sounds = {}

# State variable to track if first joke has been told
first_joke = [False]

# Audio Setup
def setup_audio():
    pygame.mixer.init()
    print("🔊 Pygame mixer initialized")
    
    # Dictionary containing all sound file paths
    sound_files = {
        'background_music': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\02 Alexa Tell a Joke\Audios\background.wav',
        'click_sound': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\02 Alexa Tell a Joke\Audios\click.wav',
        'next_joke': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\02 Alexa Tell a Joke\Audios\next joke.wav',
        'punchline': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\02 Alexa Tell a Joke\Audios\punchline.wav'}
    
    for sound_name, sound_path in sound_files.items():
        if 'music' in sound_name:
            sounds[sound_name] = sound_path
            print(f"✅ Loaded music path: {sound_name}")
        else:
            sounds[sound_name] = pygame.mixer.Sound(sound_path)
            print(f"✅ Loaded sound: {sound_name}")


# Wrapper to add a sound effect whenever a button is clicked
def button_click_sound(command, sound_name):
    def wrapper(*args, **kwargs):
        play_sound_effect(sound_name)
        return command(*args, **kwargs)
    return wrapper


# Play Background Music
def play_background_music():
    music_path = sounds.get('background_music')
    if music_path:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        print(f"✅ Playing background music")
    else:
        print(f"❌ Background music file not found")


# Stop Music
def stop_music():
    pygame.mixer.music.stop()


# Play Sound Effect
def play_sound_effect(sound_name):
    sound = sounds.get(sound_name)
    if isinstance(sound, pygame.mixer.Sound):
        sound.set_volume(0.5)
        sound.play()
        print(f"✅ Playing sound: {sound_name}")
    else:
        print(f"❌ Sound not found: {sound_name}")


# Initialize audio
setup_audio()
play_background_music()

# Main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True)

bg_image_path = r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\02 Alexa Tell a Joke\Images\background 1.jpg"
bg_img = Image.open(bg_image_path)
bg_img = bg_img.resize((1150, 730))  
bg_image = ImageTk.PhotoImage(bg_img)
bg_label = Label(main_frame, image=bg_image)
bg_label.image = bg_image
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Empty lists to store setups and punchlines
setups = []
punchlines = []

# Reading jokes from file
with open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\02 Alexa Tell a Joke\randomJokes.txt") as file_handler:
    lines = file_handler.readlines()

for l in lines:
    if "?" in l:
        data = l.strip().split("?", 1)
        setups.append(data[0] + "?")
        punchlines.append(data[1])

current_index = [0]

# Title Frame
title_frame = Frame(main_frame, bg="white", bd=1, relief=RIDGE)
title_frame.place(relx=0.5, rely=0.26, anchor="center")

# Animated Title GIF on top of background
title_img_path = r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\02 Alexa Tell a Joke\Gifs\Title.gif"
title_gif = Image.open(title_img_path)
title_frames = [ImageTk.PhotoImage(frame.copy().resize((450, 130))) for frame in ImageSequence.Iterator(title_gif)]
title_label = Label(bg_label, bd=0, highlightthickness=0)
title_label.place(relx=0.49, rely=0.34, anchor="center")

# Animate title GIF
def animate_title(index=0):
    title_label.config(image=title_frames[index])
    root.after(40, animate_title, (index + 1) % len(title_frames))
animate_title(0)

# Joke display area with rounded look
joke_display_frame = Frame(main_frame, bg="#000000", bd=3, relief=GROOVE)
joke_display_frame.place(relx=0.5, rely=0.41, anchor="n", width=500, height=150)
joke_label = Label(joke_display_frame, text="",wraplength=450,font=("Arial", 16, "bold"),fg="#ffffff", bg="#000000", pady=15)
joke_label.pack(expand=True)
punchline_label = Label(joke_display_frame, text="",wraplength=450,font=("Arial", 16, "bold"),fg="#2847af", bg="#000000", pady=10)
punchline_label.pack(expand=True)

# Functions
def tell_joke():
    if first_joke[0]:
        messagebox.showinfo("Use Next Joke", "Please use the 'Next Joke' button to see more jokes!")
        return
    if setups:
        current_index[0] = random.randint(0, len(setups) - 1)
        joke_label.config(text=setups[current_index[0]], font=("Arial", 18, "bold"))
        punchline_label.config(text="")
        first_joke[0] = True

def show_punchline():
    if joke_label["text"] == "":
        messagebox.showwarning("Wait!", "Please press 'Alexa Tell Me a Joke' button first!")
    elif punchlines:
        punchline_label.config(text=punchlines[current_index[0]])

def next_joke():
    if not first_joke[0]:
        messagebox.showinfo("Start First", "Please click 'Alexa Tell Me a Joke' button first!")
        return
    if setups:
        current_index[0] = random.randint(0, len(setups) - 1)
        joke_label.config(text=setups[current_index[0]], font=("Arial", 18, "bold"))
        punchline_label.config(text="")

def quit_app():
    result = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if result:
        stop_music()
        root.destroy()

# Button size
button_width = 220
button_height = 70

# Tell Joke Button
tell_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\Images\\button 1.png").resize((button_width, button_height)))
tell_btn_frame = Frame(bg_label, bg="#6200FF", bd=3, relief=RAISED)
tell_btn_frame.place(relx=0.35, rely=0.72, anchor="center")
tell_btn = Button(tell_btn_frame, image=tell_btn_img, command=button_click_sound(tell_joke, 'click_sound'), borderwidth=0, cursor="hand2", bg="#6200FF", activebackground="#6200FF")
tell_btn.image = tell_btn_img
tell_btn.pack()
tell_btn.bind("<Enter>", lambda e: tell_btn.config(bg="#2B0A70")) 
tell_btn.bind("<Leave>", lambda e: tell_btn.config(bg="#6029B8"))  

# Show Punchline Button
punchline_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\Images\\button 2.png").resize((button_width, button_height)))
punchline_btn_frame = Frame(bg_label, bg="#23751C", bd=3, relief=RAISED)
punchline_btn_frame.place(relx=0.65, rely=0.72, anchor="center")
punchline_btn = Button(punchline_btn_frame, image=punchline_btn_img, command=button_click_sound(show_punchline, 'punchline'), borderwidth=0, cursor="hand2", bg="#23751C", activebackground="#23751C")
punchline_btn.image = punchline_btn_img
punchline_btn.pack()
punchline_btn.bind("<Enter>", lambda e: punchline_btn.config(bg="#0B4B05"))  
punchline_btn.bind("<Leave>", lambda e: punchline_btn.config(bg="#2AAB1E")) 

# Next Joke Button
next_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\Images\\button 3.png").resize((button_width, button_height)))
next_btn_frame = Frame(bg_label, bg="#FFF454", bd=3, relief=RAISED)
next_btn_frame.place(relx=0.35, rely=0.86, anchor="center")
next_btn = Button(next_btn_frame, image=next_btn_img, command=button_click_sound(next_joke, 'next_joke'), borderwidth=0, cursor="hand2", bg="#FFF454", activebackground="#FFF454")
next_btn.image = next_btn_img
next_btn.pack()
next_btn.bind("<Enter>", lambda e: next_btn.config(bg="#636307")) 
next_btn.bind("<Leave>", lambda e: next_btn.config(bg="#D6CA1D"))  

# Quit Button
quit_btn_img = ImageTk.PhotoImage(Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\02 Alexa Tell a Joke\\Images\\button 4.png").resize((button_width, button_height)))
quit_btn_frame = Frame(bg_label, bg="#FF3E3E", bd=3, relief=RAISED)
quit_btn_frame.place(relx=0.65, rely=0.86, anchor="center")
quit_btn = Button(quit_btn_frame, image=quit_btn_img, command=button_click_sound(quit_app, 'click_sound'), borderwidth=0, cursor="hand2", bg="#FF3E3E", activebackground="#FF3E3E")
quit_btn.image = quit_btn_img
quit_btn.pack()
quit_btn.bind("<Enter>", lambda e: quit_btn.config(bg="#530404"))
quit_btn.bind("<Leave>", lambda e: quit_btn.config(bg="#D71111"))  

root.mainloop()