from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random
import time
import pygame 

game = { 'level': None, 'question_num': 0, 'score': 0, 'chances': 0, 'num1': 0, 'num2': 0, 'operator': '', 'ans': 0, 'root': None, 'entry': None, 'streak': 0, 'lives': 3, 'countdown': 30, 'timer_running': False, 'time_taken': [], 'question_start_time': 0, 'answered_questions': 0}


# Main Window
def main():
    game['root'] = Tk()
    game['root'].title(" Monster Math: Test Your Fear of Numbers!")
    game['root'].geometry("800x750")
    game['root'].resizable(False, False)
    game['root'].iconbitmap("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\favicon.ico")
    setup_audio()
    play_music('home_music')
    start_screen()
    game['root'].mainloop()


# Clear all widgets from the screen
def clear_screen():
    for widget in game['root'].winfo_children():
        widget.destroy()


# Confirm Exit
def confirm_exit():
    answer = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if answer:
        game['root'].quit()


# Button hover effects
def hover(btn, color): 
    btn.config(bg=color)


# Button leave effects
def leave(btn, color): 
    btn.config(bg=color)


# Audio Setup
def setup_audio():
    pygame.mixer.init()
    game['sounds'] = {}

    sound_files = {
        'home_music': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\Main menu.wav',
        'easy_music': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\easy.wav',
        'medium_music': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\medium wave',
        'hard_music': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\hard.wav',
        'victory_music': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\win.wav',
        'defeat_music': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\fail.wav',
        'correct': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\correct answer.wav',
        'wrong': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\wrong answer.wav',
        'button_click': r'C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\01 Maths Quiz\Audios\button click.wav' }

    for sound_name, sound_path in sound_files.items():
        try:
            if 'music' in sound_name:
                game['sounds'][sound_name] = sound_path 
            else:
                game['sounds'][sound_name] = pygame.mixer.Sound(sound_path)
        except FileNotFoundError:
            print(f"⚠️ Warning: Sound not found: {sound_path}")


# Button click sound wrapper
def button_click_sound(command):
    def wrapper(*args, **kwargs):
        play_sound_effect('button_click')
        return command(*args, **kwargs)
    return wrapper


# Play Background Music
def play_music(music_name):
    stop_music()
    if music_name in game.get('sounds', {}):
        try:
            pygame.mixer.music.load(game['sounds'][music_name])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        except Exception as e:
            print(f"❌ Could not play music '{music_name}': {e}")
    

# Stop Music
def stop_music():
    pygame.mixer.music.stop()


# Play Sound Effect
def play_sound_effect(sound_name):
    sound = game.get('sounds', {}).get(sound_name)
    if isinstance(sound, pygame.mixer.Sound):
        sound.play()


# Start Window
def start_screen():
    clear_screen()

    
    # Start window's Frame 
    start_frame = Frame(game['root'])
    start_frame.pack(fill=BOTH, expand=True)

    # Gif for background
    bg_image = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Gifs\\Play background.gif")  
    frames = [ImageTk.PhotoImage(frame.copy().resize((800, 750))) for frame in ImageSequence.Iterator(bg_image)]
    bg_label = Label(start_frame)
    bg_label.pack(fill="both", expand=True)
    def animate(index=0):
        bg_label.config(image=frames[index])
        game['root'].after(25, animate, (index + 1) % len(frames))
    animate(0)
   
   # Start Button
    start_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Play button.png") 
    start_img = start_img.resize((220, 90))
    start_photo = ImageTk.PhotoImage(start_img)
    start_button = Button(start_frame, image=start_photo, bg="#382D40", activebackground="#382D40", borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(menu))
    start_button.image = start_photo
    start_button.place(relx=0.5, rely=0.9, anchor="center")

    # Bounce Animation for Start Button (TAKEN FROM GPT) 
    def bounce(widget, y=0, direction=1):
      widget.place_configure(rely=0.85 + y/100)
      game['root'].after(350, lambda: bounce(widget, y + direction*2, -direction if abs(y) > 5 else direction))
    bounce(start_button)

    # Instructions Window
    def show_instructions():
        instruction_window = Toplevel()
        instruction_window.title("Quiz Instructions")
        instruction_window.geometry("600x670")
        instruction_window.resizable(False, False)

        instruction_frame = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Instruction background.jpg") 
        instruction_frame = instruction_frame.resize((600, 670))
        instruction_photo = ImageTk.PhotoImage(instruction_frame)
    
        bg_label = Label(instruction_window, image=instruction_photo)
        bg_label.image = instruction_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        instruction_label_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Instructions.png") 
        instruction_label_img = instruction_label_img.resize((400, 550))
        instruction_label_photo = ImageTk.PhotoImage(instruction_label_img)
        instruction_label = Label(instruction_window, image=instruction_label_photo)
        instruction_label.image = instruction_label_photo
        instruction_label.place(relx=0.5, rely=0.5, anchor="center")

    # Instructions button
    instruction_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Instructions button.png")
    instruction_img = instruction_img.resize((130, 40))
    instruction_photo = ImageTk.PhotoImage(instruction_img)
    instruction_button = Button( start_frame, image=instruction_photo, bg="#372345", activebackground="black", borderwidth=0, highlightthickness=0, cursor="hand2",command=button_click_sound(show_instructions))
    instruction_button.image = instruction_photo
    instruction_button.place(relx=0.1, rely=0.07, anchor="center")

    # Exit button
    exit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\quit button 1.png")
    exit_img = exit_img.resize((40, 40))
    exit_photo = ImageTk.PhotoImage(exit_img)
    exit_button = Button(start_frame, image=exit_photo, bg="#372345", activebackground="black", borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(confirm_exit))
    exit_button.image = exit_photo
    exit_button.place(relx=0.93, rely=0.07, anchor="center")


# Menu Window
def menu():
    stop_music()
    play_music('home_music')
    clear_screen()

    main_frame = Frame(game['root'], bg="#270B44")
    main_frame.pack(fill=BOTH, expand=True)

    # Gif for background
    gif = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Gifs\\menu background.gif")  
    frames = [ImageTk.PhotoImage(frame.copy().resize((800, 800))) for frame in ImageSequence.Iterator(gif)]
    label = Label(main_frame)
    label.pack(fill="both", expand=True)
    def animate(index=0):
        label.config(image=frames[index])
        game['root'].after(50, animate,(index + 1) % len(frames)) 
    animate() 

    # Titles for the Menu Screen
    l1 = Label(main_frame, text="Monster Math Madness!", font=("Roboto", 24, "italic"), fg="#ffd700", bg="#270B44")
    l1.place(relx=0.5, rely=0.05, anchor="center")
    box = Frame(main_frame, bg="#240B3F", bd=3, relief=RIDGE)
    box.place(relx=0.5, rely=0.3, anchor="center")
    l2_img= Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\title 1.png") 
    l2_img = l2_img.resize((240, 50))
    l2_photo = ImageTk.PhotoImage(l2_img)
    l2 = Label(box, image=l2_photo, bg="#240B3F")
    l2.image = l2_photo
    l2.pack()
    buttons = Frame(main_frame, bg="#240B3F")
    buttons.place(relx=0.5, rely=0.6, anchor="center")


    # Easy Button 
    img1 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Easy button.png")
    img1 = img1.resize((190, 80))
    easy_img = ImageTk.PhotoImage(img1)
    easy_button = Button(buttons, image=easy_img, bg="#270B44", activebackground="#270B44",borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(lambda: start(1)))
    easy_button.image = easy_img
    easy_button.pack(pady=5)
    # Medium Button
    img2 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Medium button.png") 
    img2 = img2.resize((190, 80))
    medium_img = ImageTk.PhotoImage(img2)
    medium_button = Button(buttons, image=medium_img, bg="#270B44", activebackground="#270B44",borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(lambda: start(2)))
    medium_button.image = medium_img
    medium_button.pack(pady=5)
    # Hard Button 
    img3 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Hard button.png") 
    img3 = img3.resize((190, 80))
    hard_img = ImageTk.PhotoImage(img3)
    hard_button = Button(buttons, image=hard_img, bg="#270B44", activebackground="#270B44",borderwidth=0, cursor="hand2", command=button_click_sound(lambda: start(3)))
    hard_button.image = hard_img
    hard_button.pack(pady=5)

    # Footer Information
    footer = Label(main_frame, text="10 Questions • 3 Attempts • 100 Points", font=("Arial", 10), fg="#000000", bg="#3ecc17")
    footer.place(relx=0.5, rely=0.9, anchor="center")
    # Exit Game Button 
    exit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\quit button 1.png")
    exit_img = exit_img.resize((40, 40))
    exit_photo = ImageTk.PhotoImage(exit_img)
    question_button = Button(main_frame, image=exit_photo, bg="#101025", activebackground="#101025",borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(confirm_exit))
    question_button.image = exit_photo
    question_button.place(relx=0.93, rely=0.07, anchor="center")


# Generate random numbers based on difficulty level
def random_nums():
    level = game['level']
    if level == 1: 
        return random.randint(1, 9), random.randint(1, 9)
    if level == 2: 
        return random.randint(10, 99), random.randint(10, 99)
    return random.randint(1000, 9999), random.randint(1000, 9999)


# Start the quiz 
def start(level):
    stop_music()
    game.update({'level': level,'question_num': 0,'score': 0,'streak': 0,'chances': 0,'lives': 3,'countdown': 30,'timer_running': False, 'time_taken': [], 'question_start_time': 0})

    # Set background and time limit based on level
    if level == 1:
        game['bg'] = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Green background.jpg"
        game['time_limit'] = 10
        play_music('easy_music')
    elif level == 2:
        game['bg'] = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Orange background.jpg"
        game['time_limit'] = 20
        play_music('medium_music')
    elif level == 3:
        game['bg'] = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Red background.jpg"
        game['time_limit'] = 30
        play_music('hard music')
    next_question()


# Load the next question 
def next_question():
    if game['question_num'] >= 10 or game['lives'] <= 0:
        results()
        return

    game['question_num'] += 1
    game['chances'] = 2
    game['countdown'] = game['time_limit']
    game['timer_running'] = True
    game['num1'], game['num2'] = random_nums()
    game['operator'] = random.choice(['+', '-'])
    game['ans'] = game['num1'] + game['num2'] if game['operator'] == '+' else game['num1'] - game['num2']
    game['question_start_time'] = time.time() 
    show_q()


# Display the question screen
def show_q():
    clear_screen()

    # Question screen's Frame
    f = Frame(game['root'])
    f.pack(fill="both", expand=True)

    # Background Image
    bg_file = game['bg']
    img = Image.open(bg_file)
    img = img.resize((800, 750))
    bg_photo = ImageTk.PhotoImage(img)
    bg_label = Label(f, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Top Bar that displays question number, score, lives and timer
    top = Frame(f, bg="#16213e", height=60)
    top.pack(fill=X)
    question_num_display = Label(top, text=f"Q {game['question_num']} of 10",font=("Arial", 14, "bold"), fg="#8db3b9", bg="#16213e")
    question_num_display.pack(side=LEFT, padx=30)
    score_display = Label(top, text=f"⭐ Score: {game['score']}/100",font=("Arial", 14, "bold"), fg="#ffd700", bg="#16213e")
    score_display.pack(side=RIGHT, padx=30)

    # Lives display using heart emojis
    lives_display = ""
    for i in range(3):
        if i < game['lives']:
            lives_display += "❤️"
        else:
            lives_display += "🤍"
    lives_label = Label(top, text=f"Lives: {lives_display}",font=("Arial", 14, "bold"), fg="#ff4757", bg="#16213e")
    lives_label.pack(side=RIGHT, padx=30)
    
    # Timer display 
    time_widget = Label(top, text=f"⏱ {game['countdown']}s",font=('Arial', 16, 'bold'), fg='#3498db', bg='#16213e')
    time_widget.pack(side=RIGHT, padx=15)
    def tick_timer():
        if game['timer_running'] and game['countdown'] > 0:
            game['countdown'] -= 1
            time_widget.config(text=f"⏱ {game['countdown']}s")
            game['root'].after(1000, tick_timer)
        elif game['countdown'] <= 0 and game['timer_running']:
            game['timer_running'] = False
            elapsed = time.time() - game['question_start_time'] 
            game['time_taken'].append(round(elapsed, 2))  
            game['lives'] -= 1
            if game['lives'] <= 0:
                messagebox.showerror("Time's Up!", f"⏰ Time ran out!\n💀 No lives left!\nFinal Score: {game['score']}/100")
                results()
            else:
                messagebox.showwarning("Time's Up!", f"⏰ Time ran out!\nCorrect answer: {game['ans']}\n💔 You lost one life.\nLives left: {game['lives']}")
                next_question()
    tick_timer()
    
    # Progress Bar that shows how many questions have been answered
    c = Canvas(f, width=500, height=20, bg="#1a1a2e", highlightthickness=0)
    c.pack(pady=10)
    c.create_rectangle(0, 0, 500, 20, outline="#00ff88", width=2)
    c.create_rectangle(0, 0, ((game['question_num'] - 1) / 10) * 500, 20, fill="#3498db", outline="")
    
    # Question Display background
    question_display = Frame(f, bg="#000000", bd=0)
    question_display.pack(pady=(120, 20))
    op_col = "#3275cc" if game['operator'] == '+' else "#cf3d6e"
    first_num = Label(question_display, text=f"{game['num1']}  ",font=("Arial", 42, "bold"), fg="white", bg="#000000")
    first_num.pack(side=LEFT)
    sign = Label(question_display, text=game['operator'],font=("Arial", 42, "bold"), fg=op_col, bg="#000000")
    sign.pack(side=LEFT, padx=10)
    second_num = Label(question_display, text=f"  {game['num2']}  =",font=("Arial", 42, "bold"), fg="white", bg="#000000")
    second_num.pack(side=LEFT)

    # Entry Field for user to input an answer
    e1 = Frame(f, bg="#000000")
    e1.pack(pady=20)
    l5 = Label(e1, text="Your Answer:",font=("Arial", 14, "bold"), fg="#ffffff", bg="#000000")
    l5.pack()
    game['entry'] = Entry(e1, font=("Arial", 28, "bold"), width=10, justify='center', bg="#16213e", fg="white",insertbackground="#ffffff", relief=SOLID, bd=2)
    game['entry'].pack(pady=10)
    game['entry'].focus()
    game['entry'].bind('<Return>', lambda event: check())

    # Submit Button
    submit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\enter button.png")
    submit_img = submit_img.resize((140, 90))
    submit_photo = ImageTk.PhotoImage(submit_img)
    sub_button = Button(f, image=submit_photo, bg="#000000",activebackground="#000000", borderwidth=0,highlightthickness=0, cursor="hand2", command=button_click_sound(check))
    sub_button.image = submit_photo
    sub_button.pack(pady=10)

    # Warnings and streak message
    if game['chances'] == 1:
        warning = Label(f, text="⚠️ Second Attempt - 5 Points",font=("Arial", 12, "bold"), fg="#ffaa00", bg="#000000")
        warning.pack(pady=5)
    
    if game['streak'] >= 3:
        streak_record = Label(f, text=f"🔥 {game['streak']} Question Streak! 🔥",font=("Arial", 12, "bold"), fg="#ff6b00", bg="#000000")
        streak_record.pack(pady=5)

    # Quit Button
    quit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\quit button.png")
    quit_img = quit_img.resize((50, 50))
    quit_photo = ImageTk.PhotoImage(quit_img)
    quit_button = Button(f, image=quit_photo, bg="#121111",activebackground="#121111", borderwidth=0,highlightthickness=0, cursor="hand2", command=button_click_sound(confirm_exit))
    quit_button.image = quit_photo
    quit_button.place(relx=0.95, rely=0.95, anchor="center")

    # Return button to go back to Menu screen
    return_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\return button.png")
    return_img = return_img.resize((50, 50))
    return_photo = ImageTk.PhotoImage(return_img)
    return_button = Button(f, image=return_photo, bg="#121111", activebackground="#121111",borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(lambda: confirm_return()))
    return_button.image = return_photo
    return_button.place(relx=0.055, rely=0.95, anchor="center")


# Confirm Return to Menu
def confirm_return():
    game['timer_running'] = False
    answer = messagebox.askyesno("Return to Menu", "Are you sure you want to return?\nYour progress will be lost!")
    if answer:
        menu()    
    else:
        game['timer_running'] = True


# Function to check and display message if the entry field is empty or invalid
def check():
    try:
        ans = int(game['entry'].get())
        game['timer_running'] = False
        check_ans(ans)
    except ValueError:
        messagebox.showerror("Invalid", "Please enter a valid number!")
        game['entry'].delete(0, END)
 

def check_ans(user):
    elapsed = time.time() - game['question_start_time'] 
    
    if user == game['ans']:
        play_sound_effect('correct')
        game['answered_questions'] += 1  
        game['time_taken'].append(round(elapsed, 2))  
        if game['chances'] == 2:
            game['score'] += 10
            game['streak'] += 1
        else:
            game['score'] += 5
            game['streak'] = 0
        next_question()
    else:
        play_sound_effect('wrong')
        game['chances'] -= 1
        game['streak'] = 0
        if game['chances'] > 0:
            game['timer_running'] = False
            messagebox.showwarning("Incorrect", "❌ Wrong! Try again.")
            game['timer_running'] = True
            show_q()
        else:
            game['time_taken'].append(round(elapsed, 2))  
            game['lives'] -= 1
            if game['lives'] <= 0:
                play_music('defeat_music')
                messagebox.showerror("Game Over", f"💀 No lives left!\nFinal Score: {game['score']}/100")
                results()
                return
            else:
                messagebox.showwarning("Incorrect", f"❌ Correct answer: {game['ans']}\nLives left: {game['lives']}")
                next_question()


# Display the results screen
def results():
    game['timer_running'] = False
    clear_screen()

    score = game['score']
    if score >= 90:
        grade, msgg = "A+", "Phenomenal! You’ve mastered this!"
    elif score >= 80:
        grade, msgg = "A", "Amazing effort — excellence achieved!"
    elif score >= 70:
        grade, msgg = "B", "Solid performance! You’re getting stronger!"
    elif score >= 60:
        grade, msgg = "C", "You’re improving — keep the momentum!"
    else:
        grade, msgg = "F", "Don’t quit — every setback is a setup for a comeback!"


    if score >= 60:
        stop_music()
        play_music('victory_music')
    else:
        stop_music()
        play_music('defeat_music')


    # Main Frame
    f = Frame(game['root'], bg="#0d0221", width=800, height=750)
    f.place(x=0, y=0)

    # Animated GIF Background
    gif_path = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Gifs\\result background.gif"
    bg_img = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(frame.copy().resize((800, 750))) for frame in ImageSequence.Iterator(bg_img)]
    bg_label = Label(f)
    bg_label.place(x=0, y=0, width=800, height=750)

    def animate_bg(index=0):
        bg_label.config(image=frames[index])
        bg_label.lower() 
        game['root'].after(80, animate_bg, (index + 1) % len(frames))
    animate_bg()

    # Mini Frame
    mini_frame = Frame(f, width=450, height=550, bg="#08313B")
    mini_frame.place(relx=0.5, rely=0.5, anchor="center")
    mini_frame.pack_propagate(False)

    # Mini frame background image
    mini_img_path = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\box.png"
    mini_frame_img = Image.open(mini_img_path).resize((450, 550))
    mini_frame_photo = ImageTk.PhotoImage(mini_frame_img)
    bg_mini = Label(mini_frame, image=mini_frame_photo)
    bg_mini.image = mini_frame_photo
    bg_mini.place(x=0, y=0, relwidth=1, relheight=1)

    # Main Result Card 
    card_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\card frame.png")
    card_img = card_img.resize((380, 290))
    card_photo = ImageTk.PhotoImage(card_img)
    card = Label(mini_frame, image=card_photo, bg="#08313B", bd=0)
    card.image = card_photo
    card.place(relx=0.5, rely=0.47, anchor="center")

    # Score Section
    Message = Label(mini_frame, text="FINAL SCORE", font=("Arial", 14, "bold"), fg="#ffffff", bg="#08313B")
    Message.place(relx=0.5, rely=0.26, anchor="center")
    
    score_display = Frame(mini_frame, bg="#0d0221", relief=SUNKEN, bd=2, width=180, height=90)
    score_display.place(relx=0.5, rely=0.38, anchor="center")
    score_display.config(highlightthickness=3)
    score_display.pack_propagate(False)
    
    score_label = Label(score_display, text="0", font=("Impact", 38, "bold"), fg="#ffd700", bg="#0d0221")
    score_label.place(relx=0.5, rely=0.44, anchor="center")

    def animate(i=0):
        if i <= score:
            score_label.config(text=str(i))
            game['root'].after(20, lambda: animate(i + 1))
    animate()

    obtained_score = Label(score_display, text="/ 100 Points", font=("Arial", 11), fg="#FFFFFF", bg="#0d0221")
    obtained_score.place(relx=0.5, rely=0.88, anchor="center")

    # Grade Section
    grade_box = Frame(mini_frame, bg="#ffd700", relief=RAISED, bd=3, width=100, height=70)
    grade_box.place(relx=0.5, rely=0.56, anchor="center")
    grade_box.pack_propagate(False)
    
    obtained_grade = Label(grade_box, text=grade, font=("Arial", 32, "bold"), fg="#000000", bg="#ffd700")
    obtained_grade.place(relx=0.5, rely=0.51, anchor="center")

    # Remarks Section
    remarks = Label(mini_frame, text=msgg, font=("Arial", 12, "bold"), fg="#ffd700", bg="#08313B")
    remarks.place(relx=0.5, rely=0.66, anchor="center")

    record_frame = Frame(mini_frame, width=400, height=100)
    record_frame.place(relx=0.5, rely=0.84, anchor="center")
    record_frame.pack_propagate(False)

    record_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\record.png")
    record_img = record_img.resize((400, 100))
    record_photo = ImageTk.PhotoImage(record_img)
    record_label = Label(record_frame, image=record_photo, bd=0)
    record_label.image = record_photo
    record_label.place(x=0, y=0, relwidth=1, relheight=1)

    questions_answered = game.get('answered_questions', 0)  
    lives_remaining = game.get('lives', 0)
    missed_questions = 10 - questions_answered 
    average_time = round(sum(game['time_taken']) / len(game['time_taken']), 2) if game['time_taken'] else 0

    stats_text = Label(record_frame, text=f"Questions Answered: {questions_answered}/10\nMissed Questions: {missed_questions}\nLives Remaining: {lives_remaining}/3\nAverage Time per Question: {average_time} sec", font=("Arial", 9, "bold"), fg="#ffffff", bg="#175E7A", justify="center")
    stats_text.place(relx=0.5, rely=0.5, anchor="center")

    # Play Again Button
    play_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\play again button.png").resize((70, 70))
    play_photo = ImageTk.PhotoImage(play_img)
    play_button = Button(f, image=play_photo, bg="black", activebackground="black", borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(menu))
    play_button.image = play_photo
    play_button.place(relx=0.43, rely=0.93, anchor="center")

    # Quit Button
    quit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\quit button 1.png").resize((70, 70))
    quit_photo = ImageTk.PhotoImage(quit_img)
    quit_button = Button(f, image=quit_photo, bg="black", activebackground="black", borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(game['root'].quit))
    quit_button.image = quit_photo
    quit_button.place(relx=0.57, rely=0.93, anchor="center")

main()