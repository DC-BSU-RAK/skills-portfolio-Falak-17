from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random
import time
import pygame 


# Dictionary to hold all game data
game = { 'level': None, 'question_num': 0, 'score': 0, 'chances': 0, 'num1': 0, 'num2': 0, 'operator': '', 'ans': 0, 'root': None, 'entry': None, 'streak': 0, 'lives': 3, 'countdown': 30, 'timer_running': False, 'time_taken': [], 'question_start_time': 0, 'answered_questions': 0, 'wrong_count': 0, 'calculator_unlocked': False}


# Main Function
def main():
    # Create the main window for the game
    game['root'] = Tk()
    game['root'].title(" Monster Math: Test Your Fear of Numbers!")
    game['root'].geometry("800x750")
    game['root'].resizable(False, False)

    # Custom app icon
    game['root'].iconbitmap("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\favicon.ico") 
    
    # Initialize and start background music
    setup_audio()
    play_music('home_music')

    # Load the start screen first
    start_screen()
    game['root'].mainloop()


# Removes all widgets from the screen
def clear_screen():
    for widget in game['root'].winfo_children():
        widget.destroy()


# Confirm Exit
# Displays messagebox before quitting
def confirm_exit():
    answer = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if answer:
        game['root'].quit()


# Button hover effects - changes button background color
def hover(btn, color): 
    btn.config(bg=color)


# Button leave effects - restores original color
def leave(btn, color): 
    btn.config(bg=color)


# Audio Setup
def setup_audio():
    pygame.mixer.init()
    game['sounds'] = {}

    # Dictionary containing all sound file paths
    sound_files = {
        'home_music': r'C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\Main menu.wav',
        'easy_music': r'C:\\Users\\User\\Documents\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\easy.wav',
        'medium_music': r'C:\\Users\User\\Documents\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\medium.wav',
        'hard_music': r'C:\\Users\\User\\Documents\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\hard.wav',
        'victory_music': r'C:\\Users\\User\\Documents\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\win.wav',
        'defeat_music': r'C:\\Users\\User\\Documents\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\fail.wav',
        'correct': r'C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\correct answer.wav',
        'wrong': r'C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\wrong answer.wav',
        'button_click': r'C:\\Users\\User\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Audios\\button click.wav' }

    for sound_name, sound_path in sound_files.items():
        try:
            if 'music' in sound_name:
                game['sounds'][sound_name] = sound_path 
            else:
                game['sounds'][sound_name] = pygame.mixer.Sound(sound_path)
        except FileNotFoundError:
            print(f"⚠️ Warning: Sound not found: {sound_path}")


# Wrapper to add a sound effect whenever a button is clicked ( TAKEN FROM GPT )
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


# Start Screen
def start_screen():
    clear_screen()

    # A frame for the start screen
    start_frame = Frame(game['root'])
    start_frame.pack(fill=BOTH, expand=True)

    # Gif for background
    bg_image = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Gifs\\Play background.gif")
    frames = [ImageTk.PhotoImage(frame.copy().resize((800, 750))) for frame in ImageSequence.Iterator(bg_image)]
    bg_label = Label(start_frame)
    bg_label.pack(fill="both", expand=True)

    # Function to loop through GIF frames
    def animate(index=0):
        bg_label.config(image=frames[index])
        game['root'].after(25, animate, (index + 1) % len(frames))
    animate(0)

    # Play Button
    play_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Play button.png")
    play_img = play_img.resize((220, 90))
    play_photo = ImageTk.PhotoImage(play_img)
    play_button = Button(start_frame, image=play_photo, bg="#382D40", activebackground="#382D40",borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(menu))
    play_button.image = play_photo
    play_button.place(relx=0.5, rely=0.9, anchor="center")

    # Bounce Animation for Start Button (TAKEN FROM GPT)
    def bounce(widget, y=0, direction=1):
        widget.place_configure(rely=0.85 + y/100)
        game['root'].after(350, lambda: bounce(widget, y + direction*2, -direction if abs(y) > 5 else direction))
    bounce(play_button)

    # Inner function to show instructions in a popup window
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

        instruction_label_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Instructions page.png")
        instruction_label_img = instruction_label_img.resize((400, 550))
        instruction_label_photo = ImageTk.PhotoImage(instruction_label_img)
        instruction_label = Label(instruction_window, image=instruction_label_photo)
        instruction_label.image = instruction_label_photo
        instruction_label.place(relx=0.5, rely=0.5, anchor="center")

    # Instructions button
    instruction_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Instructions button.png")
    instruction_img = instruction_img.resize((130, 40))
    instruction_photo = ImageTk.PhotoImage(instruction_img)
    instruction_button = Button(start_frame, image=instruction_photo, bg="#372345", activebackground="black",borderwidth=0, highlightthickness=0, cursor="hand2",command=button_click_sound(show_instructions))
    instruction_button.image = instruction_photo
    instruction_button.place(relx=0.1, rely=0.07, anchor="center")

    # Exit button
    exit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\quit button 1.png")
    exit_img = exit_img.resize((40, 40))
    exit_photo = ImageTk.PhotoImage(exit_img)
    exit_button = Button(start_frame, image=exit_photo, bg="#372345", activebackground="black",borderwidth=0, highlightthickness=0, cursor="hand2",command=button_click_sound(confirm_exit))
    exit_button.image = exit_photo
    exit_button.place(relx=0.93, rely=0.07, anchor="center")

    # Name Label
    made_by_label = Label(start_frame,text="Credit - Falak Ahsan",font=("Comic Sans MS", 10, "bold"),fg="#FFAE00",bg="#382E3F")
    made_by_label.place(relx=0.89, rely=0.98, anchor="center")


# Menu Window
def menu():
    # Play background music
    play_music('home_music')
    # Clear whatever was on screen before showing the menu
    clear_screen()

    # Main menu's frame
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

    # A frame to hold the difficulty buttons neatly in the center
    buttons = Frame(main_frame, bg="#240B3F")
    buttons.place(relx=0.5, rely=0.6, anchor="center")

    # Easy Level Button 
    img1 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Easy button.png")
    img1 = img1.resize((190, 80))
    easy_img = ImageTk.PhotoImage(img1)
    easy_button = Button(buttons, image=easy_img, bg="#270B44", activebackground="#270B44",borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(lambda: start(1)))
    easy_button.image = easy_img
    easy_button.pack(pady=5)
    # Medium Level Button
    img2 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Medium button.png") 
    img2 = img2.resize((190, 80))
    medium_img = ImageTk.PhotoImage(img2)
    medium_button = Button(buttons, image=medium_img, bg="#270B44", activebackground="#270B44",borderwidth=0, highlightthickness=0, cursor="hand2", command=button_click_sound(lambda: start(2)))
    medium_button.image = medium_img
    medium_button.pack(pady=5)
    # Hard Level Button 
    img3 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Images\\Hard button.png") 
    img3 = img3.resize((190, 80))
    hard_img = ImageTk.PhotoImage(img3)
    hard_button = Button(buttons, image=hard_img, bg="#270B44", activebackground="#270B44",borderwidth=0, cursor="hand2", command=button_click_sound(lambda: start(3)))
    hard_button.image = hard_img
    hard_button.pack(pady=5)

    # Exit Button 
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
        # Easy level
        return random.randint(1, 9), random.randint(1, 9)
    if level == 2: 
        # Medium Level
        return random.randint(10, 99), random.randint(10, 99)
    # Hard Level
    return random.randint(1000, 9999), random.randint(1000, 9999)


# Start the quiz 
def start(level):
    stop_music()
    
    # Store current calculator status
    keep_calculator = game.get('calculator_unlocked', False)
    
    game.update({
        'level': level,
        'question_num': 0,
        'score': 0,
        'streak': 0,
        'chances': 0,
        'lives': 3,
        'countdown': 30,
        'timer_running': False,
        'time_taken': [],
        'question_start_time': 0,
        'wrong_count': 0,
        'calculator_unlocked': keep_calculator
    })

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
        play_music('hard_music')
    # Move to the first question
    next_question()


# Load the next question 
def next_question():
    # If player answered all 10 questions or lost all lives, end the game
    if game['question_num'] >= 10 or game['lives'] <= 0:
        results()
        return

    # Prepare the next question state
    game['question_num'] += 1
    game['chances'] = 2
    game['countdown'] = game['time_limit']
    game['timer_running'] = True

    # Randomize operands and operator (+ or -)
    game['num1'], game['num2'] = random_nums()
    game['operator'] = random.choice(['+', '-'])
    game['ans'] = game['num1'] + game['num2'] if game['operator'] == '+' else game['num1'] - game['num2']
    
    # Record the question start time to track player speed
    game['question_start_time'] = time.time() 

    # Shows the question on screen
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
    time_widget.place(relx=0.29 ,rely=0.02)
    
    # Store time_widget in game dict so calculator can access it
    game['time_widget'] = time_widget
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

    if game['calculator_unlocked']:
        calculator = Frame(f, bg="#16213e", relief=SOLID, bd=2) 
        calculator.place(relx=0.065, rely=0.09, anchor="center") 
        calc_button = Button(calculator, text="💡", font=("Arial", 24),bg="#16213e", fg="#00ff88", activebackground="#0f3460",command=button_click_sound(show_calculator),cursor="hand2", relief=FLAT, bd=0)
        calc_button.pack(padx=2, pady=2) 

    # Glow effect on first unlock
    if game.get('calculator_just_unlocked', False):
        def glow(color_index=0):
            colors = ["#00ff88", "#00ffff", "#00cc66", "#00ffaa", "#00ff88"]
            if color_index < 40:  # Glow 40 times (about 6 seconds)
                calc_button.config(fg=colors[color_index % len(colors)])
                game['root'].after(150, lambda: glow(color_index + 1))
            else:
                calc_button.config(fg="#00ff88")
                game['calculator_just_unlocked'] = False  
        glow()

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


# Function to confirm returning to the main menu
def confirm_return():
    game['timer_running'] = False # Function to confirm returning to the main menu
    answer = messagebox.askyesno("Return to Menu", "Are you sure you want to return?\nYour progress will be lost!")
    if answer:
        menu()    
    else:
        game['timer_running'] = True # Resume timer if user cancels


# Function to check and display message if the entry field is empty or invalid
def check():
    try:
        ans = int(game['entry'].get()) # Trying to convert input to integer
        game['timer_running'] = False # Stop timer while checking
        check_ans(ans) # Pass input to answer checking function
    except ValueError:
        messagebox.showerror("Invalid", "Please enter a valid number!")
        game['entry'].delete(0, END) # Clear the entry field
 

# Check Answers
def check_ans(user):
    # Calculate time taken for current question
    elapsed = time.time() - game['question_start_time'] 
    
    # If the answer is correct
    if user == game['ans']:
        play_sound_effect('correct')  # Play success sound
        game['answered_questions'] += 1  # Increment answered question count
        game['time_taken'].append(round(elapsed, 2))  # Record time taken
        
        if game['chances'] == 2:
            game['score'] += 10  # Full points on first try
            game['streak'] += 1  # Increase streak
            
            if game['streak'] == 3 and not game['calculator_unlocked']:
                game['calculator_unlocked'] = True
                game['calculator_just_unlocked'] = True
                messagebox.showinfo("🎉 Calculator Unlocked!","Amazing! 3 correct answers in a row!\n🔓 You've unlocked the Calculator!\nUse it anytime for the rest of the quiz.")
        else:
            game['score'] += 5  # Half points on second try
            game['streak'] = 0  # Reset streak if needed
        
        next_question()  # Load next question

    # If the answer is incorrect
    else:
        play_sound_effect('wrong')  # Play wrong sound
        game['chances'] -= 1  # Reduce attempt count
        game['streak'] = 0  # Reset streak
        game['wrong_count'] += 1  # Track wrong answers

        # If user still has one more chance
        if game['chances'] > 0:
            game['timer_running'] = False
            messagebox.showwarning("Incorrect", "❌ Wrong! Try again.")
            game['timer_running'] = True  # Resume timer
            show_q()  # Reloads the question screen
        # If both chances are used up
        else:
            game['time_taken'].append(round(elapsed, 2))  # Record time taken
            game['lives'] -= 1  # Lose one life
            # Game over if no lives left
            if game['lives'] <= 0:
                play_music('defeat_music')
                messagebox.showerror("Game Over", f"💀 No lives left!\nFinal Score: {game['score']}/100")
                results()  # Show results screen
                return
            else:
                # Show correct answer and continue by a message box
                messagebox.showwarning("Incorrect", f"❌ Correct answer: {game['ans']}\nLives left: {game['lives']}")
                next_question()


# Calculator 
def show_calculator():
    # Pause timer before showing warning
    was_running = game.get('timer_running', False)
    if was_running:
        game['timer_running'] = False
    
    # Warning message before using calculator
    warning = messagebox.askyesno("⚠️ Calculator Warning","Using the calculator will consume it!\n\n""You'll need 3 consecutive correct answers to unlock it again.\n\n""Do you want to proceed?")
    
    if not warning:
        if was_running:
            game['timer_running'] = True
            restart_timer()
        return
    
    # Lock calculator and reset streak
    game['calculator_unlocked'] = False
    game['streak'] = 0

    # Create calculator window with modern styling
    calc_window = Toplevel(game['root'])
    calc_window.title("🧮 Monster Calculator")
    calc_window.geometry("400x450")
    calc_window.resizable(False, False)
    calc_window.config(bg="black")

    # Handle closing calculator window
    def on_close():
        calc_window.destroy()
        if was_running:
            game['timer_running'] = True
            restart_timer()
    
    calc_window.protocol("WM_DELETE_WINDOW", on_close)

    # Header Frame
    header = Frame(calc_window, bg="#0a0a0a", height=50)
    header.pack(fill=X, pady=(10, 0))
    
    title_label = Label(header, text="🧮 CALCULATOR",font=("Arial", 14, "bold"),fg="#00ff88", bg="#0a0a0a")
    title_label.pack()

    # Display Frame with glow effect
    display_frame = Frame(calc_window, bg="#0a0a0a")
    display_frame.pack(pady=20, padx=20)
    
    # Glowing border frame
    glow_frame = Frame(display_frame, bg="#669f85", bd=0)
    glow_frame.pack(padx=2, pady=2)
    
    # Calculator display entry
    display = Entry(glow_frame, font=("DS-Digital", 32, "bold"),justify="right", bg="#1a1a2e", fg="#00ff88",bd=10, relief=FLAT, insertbackground="#00ff88",readonlybackground="#1a1a2e")
    display.pack(ipady=15, ipadx=10)
    display.insert(0, "0")

    # Internal calculator state
    calc = {"current": "", "operator": None, "prev": 0}

    # Handle number button clicks
    def button_click(value):
        if calc["current"] == "" or display.get() == "0":
            calc["current"] = str(value)
            display.delete(0, END)
            display.insert(0, calc["current"])
        else:
            calc["current"] += str(value)
            display.delete(0, END)
            display.insert(0, calc["current"])

    # Clear calculator state and display
    def clear():
        calc["current"] = ""
        calc["operator"] = None
        calc["prev"] = 0
        display.delete(0, END)
        display.insert(0, "0")

    # Perform calculation
    def calculate():
        try:
            if calc["operator"] and calc["current"]:
                num = float(calc["current"])
                result = calc["prev"] + num if calc["operator"] == "+" else calc["prev"] - num
                display.delete(0, END)
                display.insert(0, str(int(result) if result == int(result) else result))
                calc["current"] = str(result)
                calc["operator"] = None
        except Exception:
            display.delete(0, END)
            display.insert(0, "Error")

    # Set current operator (+ or -)
    def set_operator(op):
        if calc["current"]:
            calc["prev"] = float(calc["current"])
            calc["operator"] = op
            calc["current"] = ""
            display.delete(0, END)

    # Buttons Frame
    buttons_frame = Frame(calc_window, bg="#0a0a0a")
    buttons_frame.pack(pady=10, padx=20)

    # Button styles
    number_style = {"font": ("Arial", 18, "bold"),"bg": "#372d3a","fg": "white","activebackground": "#07073A","activeforeground": "white","cursor": "hand2","width": 5,"height": 2,"bd": 0,"relief": FLAT }
    operator_style = {"font": ("Arial", 18, "bold"),"bg": "#f06f40","fg": "white","activebackground": "#8b2c07","activeforeground": "white","cursor": "hand2","width": 5,"height": 2,"bd": 0,"relief": FLAT}
    equals_style = {"font": ("Arial", 18, "bold"),"bg": "#07532f","fg": "#0a0a0a","activebackground": "#125a36","activeforeground": "#0a0a0a","cursor": "hand2","width": 5,"height": 2,"bd": 0,"relief": FLAT}

    # Calculator buttons and layout
    buttons = [
        ('7', 1, 0, number_style), ('8', 1, 1, number_style), ('9', 1, 2, number_style), ('-', 1, 3, operator_style),
        ('4', 2, 0, number_style), ('5', 2, 1, number_style), ('6', 2, 2, number_style), ('+', 2, 3, operator_style),
        ('1', 3, 0, number_style), ('2', 3, 1, number_style), ('3', 3, 2, number_style), ('.', 3, 3, number_style),
        ('0', 4, 0, number_style), ('=', 4, 3, equals_style)]

    # Create each button
    for (text, row, col, style) in buttons:
        if text == '=':
            button_command = calculate
        elif text == '+':
            button_command = lambda op='+': set_operator(op)
        elif text == '-':
            button_command = lambda op='-': set_operator(op)
        else:
            button_command = lambda value=text: button_click(value)

        btn = Button(buttons_frame, text=text, command=button_command, **style)
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        
        # Hover effects
        original_bg = style["bg"]
        hover_bg = style["activebackground"]
        btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=original_bg: b.config(bg=c))

    # Make button grid responsive
    for i in range(4):
        buttons_frame.grid_columnconfigure(i, weight=1)
    for i in range(1, 5):
        buttons_frame.grid_rowconfigure(i, weight=1)

    # Clear button
    clear_btn = Button(buttons_frame, text="CLEAR",font=("Arial", 15, "bold"),bg="#e63946", fg="white",activebackground="#ff4757",activeforeground="white",command=clear, cursor="hand2",width=15, height=2, bd=0, relief=FLAT)
    clear_btn.grid(row=4, column=1, columnspan=2, padx=4, pady=4, sticky="ew")
    
    # Hover for clear button
    clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#AA222D"))
    clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#640E16"))

    # Bottom section
    bottom_frame = Frame(calc_window, bg="#0a0a0a")
    bottom_frame.pack(fill=X, pady=(15, 10), padx=20)

    # Small monster icon
    monster_label = Label(bottom_frame, text="👾")
    monster_label.pack(pady=5)


# Restart countdown timer after the calculator hint is used
def restart_timer():
    def tick_timer():
        if game['timer_running'] and game['countdown'] > 0:
            game['countdown'] -= 1
            if 'time_widget' in game and game['time_widget'].winfo_exists():
                game['time_widget'].config(text=f"⏱ {game['countdown']}s")
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


# Display the results screen
def results():
    # Stop timer
    game['timer_running'] = False 

    # Clear window for result display
    clear_screen() 

    # Determine grade and feedback message based on score
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
        grade, msgg = "F", "Don’t quit — keep trying!"


    # Play victory or defeat music based on performance
    if score >= 60:
        stop_music()
        play_music('victory_music')
    else:
        stop_music()
        play_music('defeat_music')


    # Result's frame
    f = Frame(game['root'], bg="#0d0221", width=800, height=750)
    f.place(x=0, y=0)

    # Background GIF based on pass/fail result
    if score >= 60:
        gif_path = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Gifs\\result background 1.gif"
        bg_img = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy().resize((800, 750))) for frame in ImageSequence.Iterator(bg_img)]
        bg_label = Label(f)
        bg_label.place(x=0, y=0, width=800, height=750)
        def animate_bg(index=0):
            bg_label.config(image=frames[index])
            bg_label.lower() 
            game['root'].after(80, animate_bg, (index + 1) % len(frames))
        animate_bg()
    else:
        gif_path1 = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Gifs\\result background.gif"
        bg_img = Image.open(gif_path1)
        frame1 = [ImageTk.PhotoImage(frame.copy().resize((800, 780))) for frame in ImageSequence.Iterator(bg_img)]
        bg_label1 = Label(f)
        bg_label1.place(x=0, y=0, width=800, height=750)
        def animate_bg(index=0):
            bg_label1.config(image=frame1[index])
            bg_label1.lower() 
            game['root'].after(80, animate_bg, (index + 1) % len(frame1))
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

    # Animate score counting up
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

    # Calculate player statistics
    questions_answered = game.get('answered_questions', 0)  
    missed_questions = 10 - questions_answered 
    wrong_answers = game.get('wrong_count', 0)
    average_time = round(sum(game['time_taken']) / len(game['time_taken']), 2) if game['time_taken'] else 0
    
    # Display player performance stats
    stats_text = Label(record_frame, text=f"Missed Questions: {missed_questions}\nWrong Answers: {wrong_answers}\nAverage Time: {average_time} sec", font=("Arial", 11, "bold"), fg="#ffffff", bg="#175E7A", justify="center")
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