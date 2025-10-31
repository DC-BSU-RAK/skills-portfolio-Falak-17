from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random

# Store all game data in dictionary
game = { 'level': None, 'question_num': 0, 'score': 0, 'chances': 0, 'num1': 0, 'num2': 0, 'operator': '', 'ans': 0, 'root': None, 'entry': None, 'streak': 0, 'lives': 3 }

def main():
    game['root'] = Tk()
    game['root'].title(" Monster Math: Test Your Fear of Numbers!")
    game['root'].geometry("800x750")
    game['root'].resizable(False, False)
    game['root'].iconbitmap("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\favicon.ico")
    start_screen()
    game['root'].mainloop()

def clear_screen():
    for widget in game['root'].winfo_children():
        widget.destroy()

def confirm_exit():
    answer = messagebox.askyesno("Quit", "Are you sure you want to quit?\nYour progress will be lost!")
    if answer:
        game['root'].quit()

def hover(btn, color): 
    btn.config(bg=color)

def leave(btn, color): 
    btn.config(bg=color)

#   Start Window
def start_screen():
    clear_screen()
    
    start_frame = Frame(game['root'])
    start_frame.pack(fill=BOTH, expand=True)

    # Gif for background
    bg_image = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Play background.gif")  
    frames = [ImageTk.PhotoImage(frame.copy().resize((800, 750))) for frame in ImageSequence.Iterator(bg_image)]
    bg_label = Label(start_frame)
    bg_label.pack(fill="both", expand=True)
    def animate(index=0):
        bg_label.config(image=frames[index])
        game['root'].after(25, animate, (index + 1) % len(frames))
    animate(0)
   
   # Start Button
    start_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Play button.png") 
    start_img = start_img.resize((220, 90))
    start_photo = ImageTk.PhotoImage(start_img)
    start_btn = Button(start_frame, image=start_photo, bg="#382D40", activebackground="#382D40", borderwidth=0, highlightthickness=0, cursor="hand2", command=menu)
    start_btn.image = start_photo
    start_btn.place(relx=0.5, rely=0.9, anchor="center")  

    # Instructions Window
    def show_instructions():
        instruction_window = Toplevel()
        instruction_window.title("Quiz Instructions")
        instruction_window.geometry("600x670")
        instruction_window.resizable(False, False)

        instruction_frame = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Instruction background.jpg") 
        instruction_frame = instruction_frame.resize((600, 670))
        instruction_photo = ImageTk.PhotoImage(instruction_frame)
    
        bg_label = Label(instruction_window, image=instruction_photo)
        bg_label.image = instruction_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        instruction_label_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\instructions.png") 
        instruction_label_img = instruction_label_img.resize((400, 550))
        instruction_label_photo = ImageTk.PhotoImage(instruction_label_img)
        instruction_label = Label(instruction_window, image=instruction_label_photo)
        instruction_label.image = instruction_label_photo
        instruction_label.place(relx=0.5, rely=0.5, anchor="center")

    # Instructions button
    instruction_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Instructions button.png")
    instruction_img = instruction_img.resize((130, 40))
    instruction_photo = ImageTk.PhotoImage(instruction_img)
    instruction_btn = Button( start_frame, image=instruction_photo, bg="#372345", activebackground="black", borderwidth=0, highlightthickness=0, cursor="hand2",command=show_instructions)
    instruction_btn.image = instruction_photo
    instruction_btn.place(relx=0.1, rely=0.07, anchor="center")

    # Exit button
    exit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\quit button 1.png")
    exit_img = exit_img.resize((40, 40))
    exit_photo = ImageTk.PhotoImage(exit_img)
    exit_btn = Button(start_frame, image=exit_photo, bg="#372345", activebackground="black", borderwidth=0, highlightthickness=0, cursor="hand2", command=confirm_exit)
    exit_btn.image = exit_photo
    exit_btn.place(relx=0.93, rely=0.07, anchor="center")


# Menu Window
def menu():
    clear_screen()

    main_frame = Frame(game['root'], bg="#270B44")
    main_frame.pack(fill=BOTH, expand=True)

    # Gif for background
    gif = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\menu background.gif")  
    frames = [ImageTk.PhotoImage(frame.copy().resize((800, 800))) for frame in ImageSequence.Iterator(gif)]
    label = Label(main_frame)
    label.pack(fill="both", expand=True)
    def animate(index=0):
        label.config(image=frames[index])
        game['root'].after(50, animate,(index + 1) % len(frames)) 
    animate() 


    l1 = Label(main_frame, text="Monster Math Madness!", font=("Roboto", 24, "italic"), fg="#ffd700", bg="#270B44")
    l1.place(relx=0.5, rely=0.05, anchor="center")
    box = Frame(main_frame, bg="#240B3F", bd=3, relief=RIDGE)
    box.place(relx=0.5, rely=0.3, anchor="center")
    l2_img= Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\title 1.png") 
    l2_img = l2_img.resize((240, 50))
    l2_photo = ImageTk.PhotoImage(l2_img)
    l2 = Label(box, image=l2_photo, bg="#240B3F")
    l2.image = l2_photo
    l2.pack()
    buttons = Frame(main_frame, bg="#240B3F")
    buttons.place(relx=0.5, rely=0.6, anchor="center")


    # Easy Button 
    img1 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Easy button.png")
    img1 = img1.resize((190, 80))
    easy_img = ImageTk.PhotoImage(img1)
    easy_button = Button(buttons, image=easy_img, bg="#270B44", activebackground="#270B44",borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: start(1))
    easy_button.image = easy_img
    easy_button.pack(pady=5)

    # Medium Button
    img2 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Medium button.png") 
    img2 = img2.resize((190, 80))
    medium_img = ImageTk.PhotoImage(img2)
    medium_button = Button(buttons, image=medium_img, bg="#270B44", activebackground="#270B44",borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: start(2))
    medium_button.image = medium_img
    medium_button.pack(pady=5)

    # Hard Button 
    img3 = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Hard button.png") 
    img3 = img3.resize((190, 80))
    hard_img = ImageTk.PhotoImage(img3)
    hard_button = Button(buttons, image=hard_img, bg="#270B44", activebackground="#270B44",borderwidth=0, cursor="hand2", command=lambda: start(3))
    hard_button.image = hard_img
    hard_button.pack(pady=5)

    # Footer Info
    footer = Label(main_frame, text="10 Questions • 2 Attempts • 100 Points", font=("Arial", 10), fg="#000000", bg="#3ecc17")
    footer.place(relx=0.5, rely=0.9, anchor="center")

    # Exit Game Button 
    exit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\quit button 1.png")
    exit_img = exit_img.resize((40, 40))
    exit_photo = ImageTk.PhotoImage(exit_img)
    question_button = Button(main_frame, image=exit_photo, bg="#101025", activebackground="#101025",borderwidth=0, highlightthickness=0, cursor="hand2", command=confirm_exit)
    question_button.image = exit_photo
    question_button.place(relx=0.93, rely=0.07, anchor="center")


def random_nums():
    level = game['level']
    if level == 1: 
        return random.randint(1, 9), random.randint(1, 9)
    if level == 2: 
        return random.randint(10, 99), random.randint(10, 99)
    return random.randint(1000, 9999), random.randint(1000, 9999)

def start(level):
    game.update({
        'level': level,
        'question_num': 0,
        'score': 0,
        'streak': 0,
        'chances': 0,
         'lives': 3  })

    if level == 1:
        game['bg'] = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\green background 1.jpg"
    elif level == 2:
        game['bg'] = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\orange background.jpg"
    elif level == 3:
        game['bg'] = "C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\Red background.jpg"
    next_question()


def next_question():
    if game['question_num'] >= 10 or game['lives'] <= 0:
        results()
        return

    game['question_num'] += 1
    game['chances'] = 2
    game['num1'], game['num2'] = random_nums()
    game['operator'] = random.choice(['+', '-'])
    game['ans'] = game['num1'] + game['num2'] if game['operator'] == '+' else game['num1'] - game['num2']
    show_q()


def show_q():
    clear_screen()

    f = Frame(game['root'])
    f.pack(fill="both", expand=True)

    bg_file = game['bg']
    img = Image.open(bg_file)
    frames = [ImageTk.PhotoImage(frame.copy().resize((800, 750)))
              for frame in ImageSequence.Iterator(img)]

    bg_label = Label(f)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def animate(index=0):
        bg_label.config(image=frames[index])
        game['root'].after(40, animate, (index + 1) % len(frames))
    animate()

    # Top Bar
    top = Frame(f, bg="#16213e", height=60)
    top.pack(fill=X)
    # Question number
    l3 = Label(top, text=f"Q {game['question_num']} of 10",font=("Arial", 14, "bold"), fg="#8db3b9", bg="#16213e")
    l3.pack(side=LEFT, padx=30)
    # Score display
    l4 = Label(top, text=f"⭐ Score: {game['score']}/100",font=("Arial", 14, "bold"), fg="#ffd700", bg="#16213e")
    l4.pack(side=RIGHT, padx=30)

    lives_display = ""
    for i in range(3):
        if i < game['lives']:
            lives_display += "❤️ "
        else:
            lives_display += "🤍 "
    lives_label = Label(top, text=f"Lives: {lives_display}",font=("Arial", 14, "bold"), fg="#ff4757", bg="#16213e")
    lives_label.pack(side=RIGHT, padx=30)

    # Progress Bar
    c = Canvas(f, width=500, height=20, bg="#1a1a2e", highlightthickness=0)
    c.pack(pady=10)
    c.create_rectangle(0, 0, 500, 20, fill="#16213e", outline="")
    c.create_rectangle(0, 0, ((game['question_num'] - 1) / 10) * 500, 20, fill="#00ff88", outline="")

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

    # Entry Field
    e1 = Frame(f, bg="#000000")
    e1.pack(pady=20)
    l5 = Label(e1, text="Your Answer:",font=("Arial", 14, "bold"), fg="#ffffff", bg="#000000")
    l5.pack()
    game['entry'] = Entry(e1, font=("Arial", 28, "bold"), width=10, justify='center', bg="#16213e", fg="white",insertbackground="#ffffff", relief=SOLID, bd=2)
    game['entry'].pack(pady=10)
    game['entry'].focus()

    # Submit Button
    submit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\enter button.png")
    submit_img = submit_img.resize((140, 90))
    submit_photo = ImageTk.PhotoImage(submit_img)
    sub_button = Button(f, image=submit_photo, bg="#000000",activebackground="#000000", borderwidth=0,highlightthickness=0, cursor="hand2", command=check)
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
    quit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\quit button.png")
    quit_img = quit_img.resize((50, 50))
    quit_photo = ImageTk.PhotoImage(quit_img)
    quit_button = Button(f, image=quit_photo, bg="#121111",activebackground="#121111", borderwidth=0,highlightthickness=0, cursor="hand2", command=confirm_exit)
    quit_button.image = quit_photo
    quit_button.place(relx=0.95, rely=0.95, anchor="center")

    return_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\return button.png")
    return_img = return_img.resize((50, 50))
    return_photo = ImageTk.PhotoImage(return_img)
    return_button = Button(f, image=return_photo, bg="#121111", activebackground="#121111",borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: confirm_return())
    return_button.image = return_photo
    return_button.place(relx=0.055, rely=0.95, anchor="center")


def confirm_return():
    answer = messagebox.askyesno("Return to Menu", "Are you sure you want to return?\nYour progress will be lost!")
    if answer:
        menu()    


def check():
    try:
        ans = int(game['entry'].get())
        check_ans(ans)
    except ValueError:
        messagebox.showerror("Invalid", "Please enter a valid number!")
        game['entry'].delete(0, END)
 

def check_ans(user):
    if user == game['ans']:
        if game['chances'] == 2:
            game['score'] += 10
            game['streak'] += 1
            messagebox.showinfo("Correct", f"🎉 Correct!\n⭐ You earned 10 points!\nTotal Score: {game['score']}/100")
        else:
            game['score'] += 5
            game['streak'] = 0
            messagebox.showinfo("Correct", f"👍 You earned 5 points!\n⭐ Score: {game['score']}/100")

        next_question()

    else:
        game['chances'] -= 1
        game['streak'] = 0

        if game['chances'] > 0:
            messagebox.showwarning("Incorrect", "❌ Wrong! Try again.\n🔄 One more attempt (worth 5 points).")
            show_q()
        else:
            game['lives'] -= 1

            if game['lives'] <= 0:
                messagebox.showerror("Game Over", f"💀 No lives left!\nFinal Score: {game['score']}/100")
                results()
                return
            else:
                messagebox.showwarning("Incorrect", f"❌ Correct answer: {game['ans']}\n💔 You lost one life.\nLives left: {game['lives']}")
                next_question()


def results():
    clear_screen()
    score = game['score']
    if score >= 90: 
        grade, color, emo, msgg = "A+", "#00ff88", "🏆", "OUTSTANDING!"
    elif score >= 80: 
        grade, color, emo, msgg = "A", "#00d4ff", "🌟", "EXCELLENT!"
    elif score >= 70: 
        grade, color, emo, msgg = "B", "#ffaa00", "😊", "GOOD JOB!"
    elif score >= 60: 
        grade, color, emo, msgg = "C", "#ff9500", "📚", "NOT BAD!"
    else: 
        grade, color, emo, msgg = "F", "#ff4757", "💪", "KEEP PRACTICING!"

    f = Frame(game['root'], bg="#1a1a2e")
    f.pack(fill=BOTH, expand=True)
    l6 = Label(f, text=f"{emo} QUIZ COMPLETE! {emo}", font=("Arial", 28, "bold"), fg="#ffd700", bg="#1a1a2e")
    l6.pack(pady=30)
    card = Frame(f, bg="#2d3561", relief=RAISED, bd=5)
    card.pack(pady=20, padx=80, fill=BOTH, expand=True)

    score_text = Label(card, text="YOUR SCORE", font=("Arial", 16), fg="#a0a0a0", bg="#2d3561")
    score_text.pack(pady=(30, 10))
    score_label = Label(card, text="0", font=("Arial", 72, "bold"), fg="#00d4ff", bg="#2d3561")
    score_label.pack()
    def animate(i=0):
        if i <= score:
            score_label.config(text=str(i))
            game['root'].after(20, lambda: animate(i + 1))
    animate()

    marks = Label(card, text="out of 100", font=("Arial", 14), fg="#a0a0a0", bg="#2d3561")
    marks.pack(pady=(0, 20))
    grade_label = Label(card, text=f"GRADE: {grade}", font=("Arial", 32, "bold"), fg=color, bg="#2d3561")
    grade_label.pack(pady=20)
    remarks = Label(card, text=msgg, font=("Arial", 13, "bold"), fg="white", bg="#2d3561")
    remarks.pack(pady=(10, 30))

    buttons = Frame(f, bg="#1a1a2e")
    buttons.pack(pady=30)
    
    # Play Again Button
    play_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\play_again_button.png")  
    play_img = play_img.resize((180, 70))
    play_photo = ImageTk.PhotoImage(play_img)
    play = Button(buttons, image=play_photo, bg="#1a1a2e", activebackground="#1a1a2e", borderwidth=0, highlightthickness=0, cursor="hand2", command=menu)
    play.image = play_photo
    play.pack(side=LEFT, padx=10)

    # Quit Button 
    quit_img = Image.open("C:\\Users\\User\\Documents\\CYBER Y2\\Semester 3\\Code Lab II\\skills-portfolio-Falak-17\\Assessment 1 - Skills Portfolio\\01 Maths Quiz\\quit button 1.png") 
    quit_img = quit_img.resize((40, 40))
    quit_photo = ImageTk.PhotoImage(quit_img)
    quit_button = Button(buttons, image=quit_photo, bg="#1a1a2e", activebackground="#1a1a2e", borderwidth=0, highlightthickness=0, cursor="hand2", command=game['root'].quit)
    quit_button.image = quit_photo
    quit_button.pack(side=LEFT, padx=10)

main()