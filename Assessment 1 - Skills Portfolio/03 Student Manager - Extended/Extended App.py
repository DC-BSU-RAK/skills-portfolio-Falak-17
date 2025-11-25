from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

BG_MAIN = "#FDF6F0"           # Off-white linen
SIDEBAR_BG = "#3E2723"        # Deep espresso
ACCENT_PRIMARY = "#B87333"    # Copper
ACCENT_SECONDARY = "#D4A574"  # Soft gold
CARD_BG = "#FFFFFF"           # Pure white
TEXT_PRIMARY = "#3E2723"      # Deep espresso
TEXT_SECONDARY = "#8D6E63"    # Warm brown

root = Tk()
root.geometry("1250x700")
root.title("Student Manager")
root.configure(bg=BG_MAIN)

# Empty lists to copy values from file
student_code = []
student_name = []
coursework1 = []
coursework2 = []
coursework3 = []
exam_mark = []
total_coursework = []
overall_percentage = []
student_grade = []

# Store image references globally to prevent garbage collection
image_refs = {}

# Function to resize background image
def resize_bg_image(event, label, image_path, key):
    new_width = event.width
    new_height = event.height
    if new_width > 1 and new_height > 1:
        img = Image.open(image_path)
        img = img.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(img)
        label.configure(image=photo)
        image_refs[key] = photo

# Function to calculate grade based on percentage
def calculate_grade(percentage):
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

# Functioin to create statistics card
def create_stat_card(parent, title, value, bg_color, icon, image_path=None):
    # Main card container 
    parent_bg = parent.cget("bg")
    card = Frame(parent, width=220, height=125, bg=parent_bg, highlightthickness=0)
    card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    card.pack_propagate(False)

    # Add background image
    if image_path:
        bg_img = Image.open(image_path)
        bg_img.thumbnail((220, 170))
        bg_photo = ImageTk.PhotoImage(bg_img)
        image_refs[f"stat_card_{title}"] = bg_photo
        bg_label = Label(card, image=bg_photo, bg=parent_bg, borderwidth=0)
        bg_label.place(relx=0.5, rely=0.5, anchor="center")

    # ICON
    icon_label = Label(card, text=icon, fg=CARD_BG, bg=bg_color, font=("Arial", 35))
    icon_label.place(relx=0.5, rely=0.25, anchor="center")

    # TITLE
    title_label = Label(card, text=title, fg=TEXT_PRIMARY, bg=bg_color, font=("Arial", 11))
    title_label.place(relx=0.5, rely=0.51, anchor="center")

    # VALUE
    value_label = Label(card, text=value, fg=TEXT_PRIMARY, bg=bg_color, font=("Arial", 20))
    value_label.place(relx=0.5, rely=0.77, anchor="center")

# Funtion to update statistics 
def update_statistics():
    # Check if stat_cards_container exists
    if 'stat_cards_container' not in globals() or stat_cards_container is None or not stat_cards_container.winfo_exists():
        return
    
    stat_cards_container.configure(bg=BG_MAIN) 

    for widget in stat_cards_container.winfo_children():
        widget.destroy()

    if len(student_code) > 0:
        total_students = len(student_code)
        avg_percentage = round(sum(overall_percentage) / len(overall_percentage), 1)
        grade_a_count = student_grade.count('A')
        avg_exam = round(sum(exam_mark) / len(exam_mark), 1)

        # Image paths
        image_paths = {
            'students': r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\card 1.png",
            'average': r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\card 2.png",
            'grade_a': r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\card 3.png",
            'exam': r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\card 4.png"}

        # Card colors - using earth-toned theme
        card_colors = ["#BF7640", "#8B764D", "#96522B", "#FEA9C7"]
        
        # Card 1
        create_stat_card(stat_cards_container, "Total Students", str(total_students), card_colors[0], "👥", image_path=image_paths['students'])
        # Card 2
        create_stat_card(stat_cards_container, "Average Score", f"{avg_percentage}%", card_colors[1], "📊", image_path=image_paths['average'])
        # Card 3
        create_stat_card(stat_cards_container, "Grade A Students", str(grade_a_count), card_colors[2], "⭐", image_path=image_paths['grade_a'])
        # Card 4
        create_stat_card(stat_cards_container, "Avg Exam Score", f"{avg_exam}/100", card_colors[3], "📝", image_path=image_paths['exam'])

# Function to update overall performance display
def update_performance_display():
    if 'perf_scrollable' not in globals() or perf_scrollable is None or not perf_scrollable.winfo_exists():
        return
    
    for widget in perf_scrollable.winfo_children():
        widget.destroy()
    
    if len(student_code) == 0:
        Label(perf_scrollable, text="No student data available", font=("Arial", 12), bg=CARD_BG, fg=TEXT_SECONDARY).pack(pady=30)
    else:
        grade_colors = {'A': "#BF7640", 'B': "#8B764D", 'C': "#96522B", 'D': "#603200", 'F': "#3D1F00"}
        
        for i in range(len(student_code)):
            shadow_frame = Frame(perf_scrollable, bg="#D4A574", highlightthickness=0)
            shadow_frame.pack(fill=X, padx=22, pady=7)
            
            # Main card 
            student_card = Frame(shadow_frame, bg=CARD_BG, highlightbackground="#BF7640", highlightthickness=2, relief=RAISED, bd=3)
            student_card.pack(fill=X, padx=0, pady=0)
            
            color_indicator = Frame(student_card, bg=grade_colors.get(student_grade[i], '#999'), width=10)
            color_indicator.pack(side=LEFT, fill=Y)
            
            info_frame = Frame(student_card, bg=CARD_BG)
            info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
            name_row = Frame(info_frame, bg=CARD_BG)
            name_row.pack(fill=X)
            
            name = Label(name_row, text=student_name[i], font=("Georgia", 14, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
            name.pack(side=LEFT)
            student_id = Label(name_row, text=f" ---- {student_code[i]}", font=("Georgia", 12), bg=CARD_BG, fg=TEXT_SECONDARY)
            student_id.pack(side=LEFT)
            
            metrics_row = Frame(info_frame, bg=CARD_BG)
            metrics_row.pack(fill=X, pady=(5, 0))
            student_coursework = Label(metrics_row, text=f"Coursework: {total_coursework[i]}/60", font=("Georgia", 10), bg=CARD_BG, fg=TEXT_SECONDARY)
            student_coursework.pack(side=LEFT, padx=(0, 1))
            student_obtained_marks = Label(metrics_row, text=f"Exam: {exam_mark[i]}/100", font=("Georgia", 10), bg=CARD_BG, fg=TEXT_SECONDARY)
            student_obtained_marks.pack(side=LEFT, padx=(0, 15))
            student_result = Label(metrics_row, text=f"Overall: {overall_percentage[i]}%", font=("Georgia", 10, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
            student_result.pack(side=LEFT)
            
            grade_container = Frame(student_card, bg=CARD_BG)
            grade_container.pack(side=RIGHT, padx=15, pady=5)
            grade_badge = Label(grade_container, text=student_grade[i], font=("Georgia", 14, "bold"), bg=grade_colors.get(student_grade[i], '#999'), fg="white", width=3, height=1, relief=RAISED, bd=3)
            grade_badge.pack()

# Function to load data from file
def load_data():
    with open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager - Extended\studentMarks.txt") as file_handler:
        lines = file_handler.readlines()
        
    # Clear existing data
    student_code.clear()
    student_name.clear()
    coursework1.clear()
    coursework2.clear()
    coursework3.clear()
    exam_mark.clear()
    total_coursework.clear()
    overall_percentage.clear()
    student_grade.clear()
                
    # Skip first line (number of students) and read student data
    for l in lines[1:]:
        data = l.split(',')
                
        student_code.append(data[0].strip())
        student_name.append(data[1].strip())
        cw1 = int(data[2].strip())
        cw2 = int(data[3].strip())
        cw3 = int(data[4].strip())
        exam = int(data[5].strip().replace("\n", ""))
            
        coursework1.append(cw1)
        coursework2.append(cw2)
        coursework3.append(cw3)
        exam_mark.append(exam)
                    
        # Calculate total coursework
        total_cw = cw1 + cw2 + cw3
        total_coursework.append(total_cw)
                    
        # Calculate overall percentage
        total_marks = total_cw + exam
        percentage = (total_marks / 160) * 100
        overall_percentage.append(round(percentage, 2))
                    
        # Calculate grade
        grade = calculate_grade(percentage)
        student_grade.append(grade)
            
    # Refresh dashboard after loading
    update_statistics()
    update_performance_display()

# Show dashboard 
def show_dashboard():
    global stat_cards_container, perf_scrollable 
    
    # Clear content area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Main dashboard container
    dashboard_content = Frame(content_area, bg=BG_MAIN)
    dashboard_content.pack(fill=BOTH, expand=True)
    
    header = Frame(dashboard_content, bg=ACCENT_PRIMARY, height=90)
    header.pack(fill=X)
    header.pack_propagate(False)
    
    # Dashboard title
    heading = Label(header, text="Dashboard", font=("Arial", 38, "bold"), bg=ACCENT_PRIMARY, fg="white")
    heading.pack(side=LEFT, padx=(20, 20))
    
    # Date and Time display
    datetime_frame = Frame(header, bg=ACCENT_PRIMARY)
    datetime_frame.pack(side=RIGHT, padx=(20, 15))
    current_date = datetime.now().strftime("%A, %d %B %Y")
    date_label = Label(datetime_frame, text=current_date, font=("Arial", 12), bg=ACCENT_PRIMARY, fg="#FFFFFF")
    date_label.pack(side=LEFT, padx=(0, 15))
    time_label = Label(datetime_frame, text="", font=("Arial", 12), bg=ACCENT_PRIMARY, fg="#FFFFFF")
    time_label.pack(side=LEFT)
    
    # Update time every second
    def update_time():
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_label.config(text=current_time)
        time_label.after(1000, update_time)
    update_time()

    stats_frame = Frame(dashboard_content, bg=BG_MAIN)
    stats_frame.pack(fill=X, padx=20, pady=(15, 10))
    stat_cards_container = Frame(stats_frame, bg=BG_MAIN)
    stat_cards_container.pack(fill=X, padx=10, pady=(10, 5))
    bottom_container = Frame(dashboard_content, bg=BG_MAIN)
    bottom_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Configure grid for responsive layout
    bottom_container.grid_columnconfigure(0, weight=1, minsize=450)
    bottom_container.grid_columnconfigure(1, weight=1, minsize=450)
    bottom_container.grid_rowconfigure(0, weight=1)
    
    # Performance frame with earth-toned colors
    performance_frame = Frame(bottom_container, bg=CARD_BG, highlightbackground=ACCENT_SECONDARY, highlightthickness=4, relief=RAISED, bd=2)
    performance_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
    
    # Performance header
    perf_header = Frame(performance_frame, bg=CARD_BG)
    perf_header.pack(fill=X, padx=20, pady=(15, 10))
    perf_title = Label(perf_header, text="Overall Student Performance", font=("Georgia", 16, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
    perf_title.pack(side=LEFT)
    
    # Scrollable performance area with Canvas
    perf_canvas = Canvas(performance_frame, bg=CARD_BG, highlightthickness=0)
    perf_scrollbar = Scrollbar(performance_frame, orient="vertical", command=perf_canvas.yview)
    perf_scrollable = Frame(perf_canvas, bg=CARD_BG)
    
    # Configure scrolling
    perf_scrollable.bind("<Configure>", lambda e: perf_canvas.configure(scrollregion=perf_canvas.bbox("all")))
    perf_canvas.create_window((0, 0), window=perf_scrollable, anchor="nw")
    perf_canvas.configure(yscrollcommand=perf_scrollbar.set)
    
    # Pack canvas and scrollbar
    perf_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(20, 0), pady=(0, 15))
    perf_scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 5), pady=(0, 15))
    
    # Bind mousewheel for scrolling - Taken from gpt
    def on_mousewheel(event):
        perf_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    perf_canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Image box with earth-toned colors
    image_box = Frame(bottom_container, bg=CARD_BG, highlightbackground=ACCENT_PRIMARY, highlightthickness=4, relief=RAISED, bd=2)
    image_box.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
    
    # Inner image container
    image_frame = Frame(image_box, bg=CARD_BG)
    image_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
    image_path = r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\image.jpg"
    display_image = Image.open(image_path)
    img_width, img_height = display_image.size
    aspect_ratio = img_width / img_height
        
    # Resize maintaining aspect ratio
    target_height = 375
    target_width = int(target_height * aspect_ratio)
    display_image = display_image.resize((target_width, target_height))
    display_photo = ImageTk.PhotoImage(display_image)
    img_label = Label(image_frame, image=display_photo, bg=CARD_BG)
    img_label.image = display_photo 
    img_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    update_statistics()
    update_performance_display()

# View all student's record
def view_all_records():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No student records found!")
        return
    
    # Clear content area
    for widget in content_area.winfo_children():
        widget.destroy()

    # Create main records frame
    records_main = Frame(content_area, bg=BG_MAIN)
    records_main.pack(fill=BOTH, expand=True)

    # Create canvas with scrollbar
    canvas = Canvas(records_main, bg=BG_MAIN, highlightthickness=0)
    scrollbar = Scrollbar(records_main, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=BG_MAIN)

    # Configure scrolling
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Update canvas width when resized
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    # Back button
    back_btn = Button(scrollable_frame, text="← Back", font=("Georgia", 11, "bold"), bg=SIDEBAR_BG, fg="white", command=show_dashboard, padx=20, pady=8, relief=RAISED, bd=3, cursor="hand2")
    back_btn.pack(anchor=W, pady=10, padx=20)

    # Header
    header_shadow = Frame(scrollable_frame, bg="#D4A574")
    header_shadow.pack(fill=X, padx=32, pady=(10, 5))
    header_frame = Frame(header_shadow, bg=CARD_BG, relief=RAISED, bd=3, highlightbackground="#BF7640", highlightthickness=2)
    header_frame.pack(fill=X)
    header_label = Label(header_frame, text="All Student Records", font=("Georgia", 18, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, padx=20, pady=10)
    header_label.pack()
    
    # Grade colors
    grade_colors = {'A': "#BF7640", 'B': "#8B764D", 'C': "#96522B", 'D': "#603200", 'F': "#3D1F00"}
    
    # Display each student record
    for i in range(len(student_code)):
        # Outer shadow frame 
        shadow_frame = Frame(scrollable_frame, bg="#D4A574", highlightthickness=0)
        shadow_frame.pack(fill=X, padx=32, pady=7)
        
        # Main card
        student_card = Frame(shadow_frame, bg=CARD_BG, highlightbackground="#BF7640", highlightthickness=2, relief=RAISED, bd=3)
        student_card.pack(fill=X)
        
        # Color indicator
        color_indicator = Frame(student_card, bg=grade_colors.get(student_grade[i], '#999'), width=7)
        color_indicator.pack(side=LEFT, fill=Y)
        
        # Info frame
        info_frame = Frame(student_card, bg=CARD_BG)
        info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=15, pady=12)
        
        # Name row
        name_row = Frame(info_frame, bg=CARD_BG)
        name_row.pack(fill=X)
        name_label = Label(name_row, text=student_name[i], font=("Georgia", 12, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
        name_label.pack(side=LEFT)
        code_label = Label(name_row, text=f" ---- {student_code[i]}", font=("Georgia", 10), bg=CARD_BG, fg=TEXT_SECONDARY)
        code_label.pack(side=LEFT)

        # Metrics row
        metrics_row = Frame(info_frame, bg=CARD_BG)
        metrics_row.pack(fill=X, pady=(5, 0))
        
        cw_label = Label(metrics_row, text=f"Coursework: {total_coursework[i]}/60", font=("Georgia", 9), bg=CARD_BG, fg=TEXT_SECONDARY)
        cw_label.pack(side=LEFT, padx=(0, 15))
        exam_label = Label(metrics_row, text=f"Exam: {exam_mark[i]}/100", font=("Georgia", 9), bg=CARD_BG, fg=TEXT_SECONDARY)
        exam_label.pack(side=LEFT, padx=(0, 15))
        overall_label = Label(metrics_row, text=f"Overall: {overall_percentage[i]}%", font=("Georgia", 9, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
        overall_label.pack(side=LEFT)
        
        # Grade badge
        grade_container = Frame(student_card, bg=CARD_BG)
        grade_container.pack(side=RIGHT, padx=15, pady=5)
        grade_badge = Label(grade_container, text=student_grade[i], font=("Georgia", 14, "bold"), bg=grade_colors.get(student_grade[i], '#999'), fg="white", width=3, height=1, relief=RAISED, bd=3)
        grade_badge.pack()

    # Summary section
    avg_percentage = sum(overall_percentage) / len(overall_percentage)

    # Shadow for summary
    summary_shadow = Frame(scrollable_frame, bg="#D4A574")
    summary_shadow.pack(fill=X, padx=32, pady=20)
    summary_frame = Frame(summary_shadow, bg="#BF7640", highlightbackground=CARD_BG, highlightthickness=2, relief=RAISED, bd=3)
    summary_frame.pack(fill=X)
    summary_title = Label(summary_frame, text="Summary", font=("Georgia", 14, "bold"), bg="#BF7640", fg="white")
    summary_title.pack(anchor=W, padx=20, pady=(15, 5))
    total_students_label = Label(summary_frame, text=f"Total Students: {len(student_code)}", font=("Georgia", 11), bg="#BF7640", fg="white")
    total_students_label.pack(anchor=W, padx=20, pady=3)
    avg_label = Label(summary_frame, text=f"Average Percentage: {round(avg_percentage, 2)}%", font=("Georgia", 11), bg="#BF7640", fg="white")
    avg_label.pack(anchor=W, padx=20, pady=(3, 15))
    
    # Pack canvas and scrollbar
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Bind mousewheel for scrolling -Taken from gpt
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

# View individual record
def view_individual_record():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No data loaded!")
        return
    
    # Create search window
    search_window = Toplevel(root)
    search_window.title("Search Student")
    search_window.geometry("500x350")
    search_window.configure(bg=BG_MAIN)
    
    # Search label
    l12 = Label(search_window, text="🔍 Search Student", font=("Arial", 18, "bold"), bg=BG_MAIN, fg=TEXT_PRIMARY)
    l12.pack(pady=25)
    l13 = Label(search_window, text="Enter Student Code or Name:", font=("Arial", 12), bg=BG_MAIN, fg=TEXT_PRIMARY)
    l13.pack(pady=(0, 10))
    
    # Search entry
    search_entry = Entry(search_window, font=("Arial", 13), width=30, bd=2, relief="solid", highlightthickness=2, highlightbackground=ACCENT_PRIMARY, highlightcolor=ACCENT_SECONDARY)
    search_entry.pack(pady=10, ipady=8)
    search_entry.focus()
    
    # Dropdown frame
    dropdown_frame = Frame(search_window, bg=BG_MAIN)
    dropdown_frame.pack(fill=X, padx=60, pady=(5, 0))
    
    # Listbox for suggestions
    dropdown_list = Listbox(dropdown_frame, font=("Arial", 10), height=0, bd=2, relief="solid", bg=CARD_BG, selectbackground=ACCENT_PRIMARY, selectforeground="white")
    dropdown_scrollbar = Scrollbar(dropdown_frame, command=dropdown_list.yview)
    dropdown_list.configure(yscrollcommand=dropdown_scrollbar.set)
    
    # Show suggestions as user types
    def show_suggestions(event=None):
        typed = search_entry.get().strip().lower()
        dropdown_list.delete(0, END)
        
        if typed:
            # Find matching students
            matches = []
            for i in range(len(student_code)):
                if typed in student_code[i].lower() or typed in student_name[i].lower():
                    matches.append(f"{student_name[i]} - {student_code[i]}")
            
            # Show matches
            if matches:
                dropdown_list.config(height=min(5, len(matches)))
                for match in matches:
                    dropdown_list.insert(END, match)
                dropdown_list.pack(side=LEFT, fill=BOTH, expand=True)
                dropdown_scrollbar.pack(side=RIGHT, fill=Y)
            else:
                dropdown_list.pack_forget()
                dropdown_scrollbar.pack_forget()
        else:
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
    
    # Click on suggestion
    def click_suggestion(event):
        if dropdown_list.size() > 0:
            selected = dropdown_list.curselection()
            if selected:
                text = dropdown_list.get(selected[0])
                code = text.split(" - ")[-1]
                search_entry.delete(0, END)
                search_entry.insert(0, code)
                dropdown_list.pack_forget()
                dropdown_scrollbar.pack_forget()
    
    # Press Enter key
    def press_enter(event):
        if dropdown_list.size() > 0:
            first = dropdown_list.get(0)
            code = first.split(" - ")[-1]
            search_entry.delete(0, END)
            search_entry.insert(0, code)
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
        search_student()
    
    # Bind events
    search_entry.bind("<KeyRelease>", show_suggestions)
    search_entry.bind("<Return>", press_enter)
    dropdown_list.bind("<ButtonRelease-1>", click_suggestion)
    
    def search_student():
        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a student code or name")
            return
        
        # Find student
        found = False
        index = -1
        for i in range(len(student_code)):
            if (search_term.lower() == student_code[i].lower() or 
                search_term.lower() in student_name[i].lower()):
                found = True
                index = i
                break
        
        if found:
            search_window.destroy()
            
            # Clear content area
            for widget in content_area.winfo_children():
                widget.destroy()
            
            # Main detail frame
            detail_frame = Frame(content_area, bg=BG_MAIN)
            detail_frame.pack(fill=BOTH, expand=True)
            
            # Header
            header = Frame(detail_frame, bg=ACCENT_PRIMARY, height=90)
            header.pack(fill=X)
            header.pack_propagate(False)
            l14 = Label(header, text="Student Details", font=("Arial", 38, "bold"), bg=ACCENT_PRIMARY, fg="white")
            l14.pack(side=LEFT, padx=(20, 20))
            
            # DateTime display
            datetime_frame = Frame(header, bg=ACCENT_PRIMARY)
            datetime_frame.pack(side=RIGHT, padx=(20, 15))
            current_date = datetime.now().strftime("%A, %d %B %Y")
            date = Label(datetime_frame, text=current_date, font=("Arial", 12), bg=ACCENT_PRIMARY, fg="#FFFFFF")
            date.pack(side=LEFT, padx=(0, 15))
            time = Label(datetime_frame, text="", font=("Arial", 12), bg=ACCENT_PRIMARY, fg="#FFFFFF")
            time.pack(side=LEFT)
            def update_time():
                current_time = datetime.now().strftime("%I:%M:%S %p")
                time.config(text=current_time)
                time.after(1000, update_time)
            update_time()
            
            # Content container with scrollbar
            content_container = Frame(detail_frame, bg=BG_MAIN)
            content_container.pack(fill=BOTH, expand=True, padx=40, pady=30)
            
            # Create canvas and scrollbar
            canvas = Canvas(content_container, bg="#BF7640", highlightthickness=0)
            scrollbar = Scrollbar(content_container, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg="#BF7640")
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            
            # Make canvas window expand with canvas width
            def configure_canvas_window(event):
                canvas.itemconfig(canvas_window, width=event.width)
            canvas.bind("<Configure>", configure_canvas_window)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
            
            # Back button
            individualRrecord_btn = Button(scrollable_frame, text="← Back", font=("Arial", 12, "bold"), bg=SIDEBAR_BG, fg="white", command=show_dashboard, padx=20, pady=10, bd=0, cursor="hand2", relief="raised", borderwidth=3)
            individualRrecord_btn.pack(anchor=W, pady=(10, 20), padx=10)
            
            # Main card
            card = Frame(scrollable_frame, bg=CARD_BG, highlightbackground=ACCENT_PRIMARY, highlightthickness=2, relief="raised", borderwidth=5)
            card.pack(fill=BOTH, expand=True, padx=60, pady=20)
            
            # Grade colors
            grade_colors = {'A': "#BF7640", 'B': "#8B764D", 'C': "#96522B", 'D': "#603200", 'F': "#3D1F00"}
            content = Frame(card, bg=CARD_BG)
            content.pack(fill=BOTH, expand=True, padx=60, pady=40)
            
            # Icon frame
            icon_frame = Frame(content, bg="#BF7640", relief="raised", borderwidth=3, highlightbackground=ACCENT_PRIMARY, highlightthickness=2)
            icon_frame.pack(pady=(10, 20))
            icon = Label(icon_frame, text="👤", font=("Arial", 55), bg="#BF7640", padx=35, pady=25)
            icon.pack()
            l15 = Label(content, text=student_name[index], font=("Georgia", 26, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
            l15.pack(pady=(10, 5))
            
            # Code frame
            code_frame = Frame(content, bg="#BF7640", relief="raised", borderwidth=2)
            code_frame.pack(pady=10)
            l16 = Label(code_frame, text=f"Code: {student_code[index]}", font=("Arial", 14, "bold"), bg="#BF7640", fg="white", padx=25, pady=10)
            l16.pack()
            
            # Divider
            Frame(content, bg=ACCENT_PRIMARY, height=3, relief="sunken", borderwidth=1).pack(fill=X, pady=25)
            
            # Stats container 
            stats_main_container = Frame(content, bg=CARD_BG)
            stats_main_container.pack(fill=X, pady=20)
            
            # Top row 
            coursework_section = Frame(stats_main_container, bg="#FFC396", relief="raised", borderwidth=2, highlightbackground=ACCENT_PRIMARY, highlightthickness=1)
            coursework_section.pack(fill=X, pady=(0, 15))
            
            # Section header
            cw_header = Frame(coursework_section, bg=ACCENT_SECONDARY)
            cw_header.pack(fill=X)
            l17 = Label(cw_header, text="📚 Coursework Performance", font=("Arial", 14, "bold"), bg=ACCENT_SECONDARY, fg="white", pady=12)
            l17.pack()
            
            # Coursework content
            cw_content = Frame(coursework_section, bg="#FFC396")
            cw_content.pack(fill=X, padx=20, pady=20)
            
            # Circular chart
            chart_frame = Frame(cw_content, bg="#FFC396")
            chart_frame.pack(side=LEFT, padx=(0, 30))
            
            # Canvas for circular chart
            chart_canvas = Canvas(chart_frame, width=160, height=160, bg="#FFC396", highlightthickness=0)
            chart_canvas.pack()
            
            # Draw circular progress chart
            cw1 = int(coursework1[index])
            cw2 = int(coursework2[index])
            cw3 = int(coursework3[index])
            total_cw = cw1 + cw2 + cw3
            
            # Define colors for each coursework segment
            cw_colors = ['#BF7640', '#8B764D', '#96522B']
            cw_values = [cw1, cw2, cw3]
            cw_labels = ['CW1', 'CW2', 'CW3']
            
            # Draw outer ring shadow
            chart_canvas.create_oval(18, 18, 142, 142, fill="", outline="#CCCCCC", width=3)
            
            # Draw segments
            start_angle = 90
            for i, (val, col) in enumerate(zip(cw_values, cw_colors)):
                extent = (val / 60) * 360 if val > 0 else 0
                if extent > 0:
                    chart_canvas.create_arc(20, 20, 140, 140, start=start_angle, extent=extent, fill=col, outline="white", width=3)
                    start_angle += extent
            
            # Center circle
            chart_canvas.create_oval(45, 45, 115, 115, fill="white", outline=ACCENT_PRIMARY, width=3)
            chart_canvas.create_text(80, 70, text=f"{total_cw}", font=("Arial", 28, "bold"), fill=TEXT_PRIMARY)
            chart_canvas.create_text(80, 95, text="out of 60", font=("Arial", 9), fill=TEXT_SECONDARY)
            
            # Coursework breakdown details
            details_frame = Frame(cw_content, bg="#FFC396")
            details_frame.pack(side=LEFT, fill=BOTH, expand=True)
            
            # Individual coursework cards
            for i, (label, val, col) in enumerate(zip(cw_labels, cw_values, cw_colors)):
                cw_card = Frame(details_frame, bg=col, relief="flat", borderwidth=0)
                cw_card.pack(fill=X, pady=3)
                cw_inner = Frame(cw_card, bg=CARD_BG, relief="flat")
                cw_inner.pack(fill=X, padx=2, pady=2)
                
                # Layout with columns
                l24 = Label(cw_inner, text=label, font=("Arial", 11, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, width=6, anchor="w")
                l24.pack(side=LEFT, padx=(10, 5))
                
                # Progress bar
                progress_frame = Frame(cw_inner, bg="#E0E0E0", height=20, width=150)
                progress_frame.pack(side=LEFT, padx=10)
                progress_frame.pack_propagate(False)
                progress_width = int((val / 20) * 150) if val > 0 else 0
                if progress_width > 0:
                    Frame(progress_frame, bg=col, width=progress_width, height=20).pack(side=LEFT)
                l18 = Label(cw_inner, text=f"{val}/20", font=("Arial", 11, "bold"), bg=CARD_BG, fg=col, width=6)
                l18.pack(side=LEFT, padx=5)
            
            # Bottom row - Exam and Overall stats
            stats_row = Frame(stats_main_container, bg=CARD_BG)
            stats_row.pack(fill=X)
            bottom_stats = [
                ("📝 Exam Mark", f"{exam_mark[index]}", "100", ACCENT_SECONDARY),
                ("🎯 Overall Score", f"{overall_percentage[index]}", "%", ACCENT_PRIMARY)]
            
            # Create modern stat cards
            for label, value, suffix, color in bottom_stats:
                stat_card = Frame(stats_row, bg=color, relief="raised", borderwidth=3, highlightbackground=TEXT_PRIMARY, highlightthickness=1)
                stat_card.pack(side=LEFT, fill=BOTH, expand=True, padx=8)
                
                # Header section
                stat_header = Frame(stat_card, bg=color)
                stat_header.pack(fill=X, pady=(8, 0))
                l19 = Label(stat_header, text=label, font=("Arial", 12, "bold"), bg=color, fg="white")
                l19.pack()
                
                # Value section
                stat_inner = Frame(stat_card, bg=CARD_BG)
                stat_inner.pack(fill=BOTH, expand=True, padx=3, pady=3)
                value_frame = Frame(stat_inner, bg=CARD_BG)
                value_frame.pack(expand=True, pady=15)
                l20 = Label(value_frame, text=value, font=("Arial", 32, "bold"), bg=CARD_BG, fg=color)
                l20.pack(side=LEFT)
                l21 = Label(value_frame, text=f"/{suffix}", font=("Arial", 14), bg=CARD_BG, fg=TEXT_SECONDARY)
                l21.pack(side=LEFT, padx=(2, 0))
            
            # Divider
            Frame(content, bg=ACCENT_PRIMARY, height=3, relief="sunken", borderwidth=1).pack(fill=X, pady=30)
            
            # Grade display
            grade_section = Frame(content, bg=CARD_BG)
            grade_section.pack(fill=X, pady=(10, 20))
            l22 = Label(grade_section, text="Final Grade", font=("Arial", 14, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
            l22.pack(pady=(0, 10))
            grade_outer = Frame(grade_section, bg=grade_colors.get(student_grade[index], '#999'), relief="raised", borderwidth=5, highlightbackground=TEXT_PRIMARY, highlightthickness=2)
            grade_outer.pack(padx=100)
            grade_frame = Frame(grade_outer, bg=grade_colors.get(student_grade[index], '#999'))
            grade_frame.pack(padx=5, pady=5)
            grade = Label(grade_frame, text=student_grade[index], font=("Georgia", 48, "bold"), bg=grade_colors.get(student_grade[index], '#999'), fg="white", padx=60, pady=25)
            grade.pack()
            
            # Force canvas to update its scroll region
            scrollable_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        else:
            messagebox.showinfo("Not Found", "Student not found!")
    
    # Bottom buttons
    btn_frame = Frame(search_window, bg=BG_MAIN)
    btn_frame.pack(pady=25)
    search_btn = Button(btn_frame, text="Search", font=("Arial", 12, "bold"), bg=ACCENT_PRIMARY, fg="white", command=search_student, padx=30, pady=10, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    search_btn.pack(side=LEFT, padx=10)
    cancle_btn = Button(btn_frame, text="Cancel", font=("Arial", 12), bg=SIDEBAR_BG, fg="white", command=search_window.destroy, padx=30, pady=10, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    cancle_btn.pack(side=LEFT, padx=10)

# Show Highest Score
def show_highest_score():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No data loaded!")
        return
    
    max_percentage = max(overall_percentage)
    index = overall_percentage.index(max_percentage)
    
    # Clear content area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Main detail frame
    detail_frame = Frame(content_area, bg=BG_MAIN)
    detail_frame.pack(fill=BOTH, expand=True)
    
    bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\background.jpg")
    bg_image = bg_image.resize((1400, 800))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(detail_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Back button
    HighScore_back_btn = Button(detail_frame, text="← Back", font=("Arial", 10, "bold"), bg=SIDEBAR_BG, fg="white", command=show_dashboard, padx=15, pady=6, bd=0, cursor="hand2", relief="raised", borderwidth=6)
    HighScore_back_btn.pack(anchor=W, pady=(15, 10), padx=15)
    
    # Main card container 
    card_container = Frame(detail_frame, bg="#BF7640")
    card_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=0.85)
    main_card = Frame(card_container, bg="#BF7640", relief="raised", highlightbackground=ACCENT_PRIMARY, highlightthickness=3)
    main_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
    card_content = Frame(main_card, bg=CARD_BG)
    card_content.pack(fill=BOTH, expand=True, padx=80, pady=40)
    
    # Trophy image
    trophy_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\Trophy.jpg")
    trophy_image = trophy_image.resize((220, 220))
    trophy_photo = ImageTk.PhotoImage(trophy_image)
    trophy_label = Label(card_content, image=trophy_photo, bg=CARD_BG)
    trophy_label.image = trophy_photo 
    trophy_label.pack(pady=(10, 15))
    
    # Student name
    name_label = Label(card_content, text=student_name[index], font=("Arial", 24, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
    name_label.pack(pady=(10, 5))
    
    # Student code
    code_label = Label(card_content, text=f"ID: {student_code[index]}", font=("Arial", 12), bg=CARD_BG, fg=TEXT_SECONDARY)
    code_label.pack(pady=(0, 10))
    
    # Grade colors
    grade_colors = {'A': "#BF7640", 'B': "#8B764D", 'C': "#96522B", 'D': "#603200", 'F': "#3D1F00"}
    grade_frame = Frame(card_content, bg=grade_colors.get(student_grade[index], '#999'), relief="raised", borderwidth=4, highlightbackground=TEXT_PRIMARY, highlightthickness=2)
    grade_frame.pack(pady=4)
    grade_inner = Frame(grade_frame, bg=grade_colors.get(student_grade[index], '#999'))
    grade_inner.pack(padx=2, pady=2)
    l23 = Label(grade_inner, text="Final Grade", font=("Arial", 11, "bold"), bg=grade_colors.get(student_grade[index], '#999'), fg="white")
    l23.pack(pady=(5, 0))
    l24 = Label(grade_inner, text=student_grade[index], font=("Arial", 48, "bold"), bg=grade_colors.get(student_grade[index], '#999'), fg="white", padx=40, pady=10)
    l24.pack()
    
    # Score display
    score_label = Label(card_content, text=f"Overall Score: {overall_percentage[index]}%", font=("Arial", 16, "bold"), bg=CARD_BG, fg=ACCENT_SECONDARY)
    score_label.pack(pady=(15, 0))

# Show Lowest Score
def show_lowest_score():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No data loaded!")
        return
    
    min_percentage = min(overall_percentage)
    index = overall_percentage.index(min_percentage)
    
    # Clear content area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Main detail frame
    detail_frame = Frame(content_area, bg=BG_MAIN)
    detail_frame.pack(fill=BOTH, expand=True)
    
    bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\background.jpg")
    bg_image = bg_image.resize((1400, 800))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(detail_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Back button
    LowScore_back_btn = Button(detail_frame, text="← Back", font=("Arial", 10, "bold"), bg=SIDEBAR_BG, fg="white", command=show_dashboard, padx=15, pady=6, bd=0, cursor="hand2", relief="raised", borderwidth=6)
    LowScore_back_btn.pack(anchor=W, pady=(15, 10), padx=15)
    
    # Main card container
    card_container = Frame(detail_frame, bg="#BF7640")
    card_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=0.85)
    main_card = Frame(card_container, bg="#BF7640", relief="raised", highlightbackground=ACCENT_PRIMARY, highlightthickness=3)
    main_card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)
    card_content = Frame(main_card, bg=CARD_BG)
    card_content.pack(fill=BOTH, expand=True, padx=80, pady=40)
    warning_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\warning.jpg")
    warning_image = warning_image.resize((220, 220))
    warning_photo = ImageTk.PhotoImage(warning_image)
    warning_label = Label(card_content, image=warning_photo, bg=CARD_BG)
    warning_label.image = warning_photo 
    warning_label.pack(pady=(10, 15))
    
    # Student name
    name_label = Label(card_content, text=student_name[index], font=("Arial", 24, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
    name_label.pack(pady=(10, 5))
    
    # Student code
    code_label = Label(card_content, text=f"ID: {student_code[index]}", font=("Arial", 12), bg=CARD_BG, fg=TEXT_SECONDARY)
    code_label.pack(pady=(0, 10))
    
    # Grade display frame
    grade_colors = {'A': "#BF7640", 'B': "#8B764D", 'C': "#96522B", 'D': "#603200", 'F': "#3D1F00"}
    grade_frame = Frame(card_content, bg="#3D1F00", relief="raised", borderwidth=4, highlightbackground="#603200", highlightthickness=2)
    grade_frame.pack(pady=8)
    grade_inner = Frame(grade_frame, bg="#3D1F00")
    grade_inner.pack(padx=8, pady=8)
    
    l23 = Label(grade_inner, text="Final Grade", font=("Arial", 11, "bold"), bg="#3D1F00", fg="white")
    l23.pack(pady=(5, 0))
    l24 = Label(grade_inner, text=student_grade[index], font=("Arial", 48, "bold"), bg="#3D1F00", fg="white", padx=40, pady=10)
    l24.pack()
    
    # Score display
    score_label = Label(card_content, text=f"Overall Score: {overall_percentage[index]}%", font=("Arial", 16, "bold"), bg=CARD_BG, fg="#603200")
    score_label.pack(pady=(10, 5))

# Save new student's data
def save_data_to_file():
    try:
        with open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager Extended\studentMarks.txt", "w") as file_handler:
            # Write number of students
            file_handler.write(f"{len(student_code)}\n")
            
            # Write each student's data
            for i in range(len(student_code)):
                file_handler.write(f"{student_code[i]},{student_name[i]},{coursework1[i]},{coursework2[i]},{coursework3[i]},{exam_mark[i]}\n")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")
        return False

# Sort out records
def sort_student_records():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No student records found!")
        return
    
    # Clear display area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Header
    header_label = Label(content_area, text="📊 Sort Student Records", font=("Arial", 22, "bold"), bg=BG_MAIN, fg=TEXT_PRIMARY)
    header_label.pack(pady=30)
    
    # Main content frame
    content_frame = Frame(content_area, bg=BG_MAIN)
    content_frame.pack(fill=BOTH, expand=True, padx=50)
    
    # Sort options
    sort_by_var = StringVar(value="percentage")
    order_var = StringVar(value="desc")
    
    # Sort by frame
    sort_by_frame = Frame(content_frame, bg=CARD_BG, relief="raised", borderwidth=2, highlightbackground=ACCENT_PRIMARY, highlightthickness=1)
    sort_by_frame.pack(fill=X, pady=(10, 15))
    
    sort_by=Label(sort_by_frame, text="Sort By:", font=("Arial", 14, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
    sort_by.pack(pady=(20, 10))
    
    r1=Radiobutton(sort_by_frame, text="Overall Percentage", variable=sort_by_var, value="percentage", font=("Arial", 12), bg=CARD_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_SECONDARY, activebackground=CARD_BG)
    r1.pack(anchor=W, padx=40, pady=5)
    r2=Radiobutton(sort_by_frame, text="Student Name", variable=sort_by_var, value="name", font=("Arial", 12), bg=CARD_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_SECONDARY, activebackground=CARD_BG)
    r2.pack(anchor=W, padx=40, pady=5)
    r3=Radiobutton(sort_by_frame, text="Exam Mark", variable=sort_by_var, value="exam", font=("Arial", 12), bg=CARD_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_SECONDARY, activebackground=CARD_BG)
    r3.pack(anchor=W, padx=40, pady=(5, 20))
    
    # Order frame
    order_frame = Frame(content_frame, bg=CARD_BG, relief="raised", borderwidth=2, highlightbackground=ACCENT_PRIMARY, highlightthickness=1)
    order_frame.pack(fill=X, pady=(0, 15))
    order_by=Label(order_frame, text="Order:", font=("Arial", 14, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
    order_by.pack(pady=(20, 10))
    
    r4=Radiobutton(order_frame, text="Descending (High to Low)", variable=order_var, value="desc", font=("Arial", 12), bg=CARD_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_SECONDARY, activebackground=CARD_BG)
    r4.pack(anchor=W, padx=40, pady=5)
    r5=Radiobutton(order_frame, text="Ascending (Low to High)", variable=order_var, value="asc", font=("Arial", 12), bg=CARD_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_SECONDARY, activebackground=CARD_BG)
    r5.pack(anchor=W, padx=40, pady=(5, 20))
    
    def apply_sort():
        global student_code, student_name, coursework1, coursework2, coursework3, exam_mark
        global total_coursework, overall_percentage, student_grade
        
        sort_by = sort_by_var.get()
        order = order_var.get()
        
        # Create indices list
        indices = list(range(len(student_code)))
        
        # Sort based on selection
        if sort_by == "percentage":
            indices.sort(key=lambda i: overall_percentage[i], reverse=(order == "desc"))
        elif sort_by == "name":
            indices.sort(key=lambda i: student_name[i].lower(), reverse=(order == "desc"))
        elif sort_by == "exam":
            indices.sort(key=lambda i: exam_mark[i], reverse=(order == "desc"))
        
        # Reorder all lists
        student_code[:] = [student_code[i] for i in indices]
        student_name[:] = [student_name[i] for i in indices]
        coursework1[:] = [coursework1[i] for i in indices]
        coursework2[:] = [coursework2[i] for i in indices]
        coursework3[:] = [coursework3[i] for i in indices]
        exam_mark[:] = [exam_mark[i] for i in indices]
        total_coursework[:] = [total_coursework[i] for i in indices]
        overall_percentage[:] = [overall_percentage[i] for i in indices]
        student_grade[:] = [student_grade[i] for i in indices]
        
        view_all_records()
        messagebox.showinfo("Success", "Records sorted successfully!")
    
    # Buttons
    btn_frame = Frame(content_frame, bg=BG_MAIN)
    btn_frame.pack(pady=30)
    sort_btn = Button(btn_frame, text="Sort Records", font=("Arial", 13, "bold"), bg=ACCENT_PRIMARY, fg="white", command=apply_sort, padx=40, pady=12, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    sort_btn.pack(side=LEFT, padx=10)
    cancel_btn = Button(btn_frame, text="Cancel", font=("Arial", 13), bg=SIDEBAR_BG, fg="white", command=view_all_records, padx=40, pady=12, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    cancel_btn.pack(side=LEFT, padx=10)

# Add new student record
def add_student_record():
    # Clear display area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Create main container with scrollbar
    main_frame = Frame(content_area, bg=BG_MAIN)
    main_frame.pack(fill=BOTH, expand=True)
    
    # Create canvas with scrollbar
    canvas = Canvas(main_frame, bg=BG_MAIN, highlightthickness=0)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=BG_MAIN)
    
    # Configure scrolling
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Update canvas width when resized
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)
    
    # Back button
    back_btn = Button(scrollable_frame, text="← Back", font=("Georgia", 11, "bold"), bg=SIDEBAR_BG, fg="white", command=show_dashboard, padx=20, pady=8, relief=RAISED, bd=3, cursor="hand2")
    back_btn.pack(anchor=W, pady=10, padx=20)
    
    # Header shadow
    header_shadow = Frame(scrollable_frame, bg="#D4A574")
    header_shadow.pack(fill=X, padx=32, pady=(10, 5))
    header_frame = Frame(header_shadow, bg=CARD_BG, relief=RAISED, bd=3, highlightbackground="#BF7640", highlightthickness=2)
    header_frame.pack(fill=X)
    header_label = Label(header_frame, text="➕ Add New Student", font=("Georgia", 18, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, padx=20, pady=10)
    header_label.pack()
    
    # Form shadow frame
    form_shadow = Frame(scrollable_frame, bg="#D4A574")
    form_shadow.pack(fill=X, padx=32, pady=(10, 20))
    
    # Form frame
    form_frame = Frame(form_shadow, bg=CARD_BG, relief="raised", borderwidth=3, highlightbackground="#BF7640", highlightthickness=2)
    form_frame.pack(fill=X)
    
    # Entry fields container
    fields_container = Frame(form_frame, bg=CARD_BG)
    fields_container.pack(fill=X, padx=40, pady=30)
    
    # Entry fields
    fields = []
    labels_text = ["Student Code:", "Student Name:", "Coursework 1 (0-20):", "Coursework 2 (0-20):", "Coursework 3 (0-20):", "Exam Mark (0-100):"]
    
    for label_text in labels_text:
        field_frame = Frame(fields_container, bg=CARD_BG)
        field_frame.pack(fill=X, pady=10)
        
        Label(field_frame, text=label_text, font=("Arial", 12, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W).pack(fill=X, pady=(0, 5))
        
        entry = Entry(field_frame, font=("Arial", 13), bd=2, relief="solid", highlightthickness=2, highlightbackground=ACCENT_SECONDARY, highlightcolor=ACCENT_PRIMARY)
        entry.pack(fill=X, ipady=10)
        fields.append(entry)
    
    fields[0].focus()
    
    def save_student():
        # Get values
        code = fields[0].get().strip()
        name = fields[1].get().strip()
        cw1_str = fields[2].get().strip()
        cw2_str = fields[3].get().strip()
        cw3_str = fields[4].get().strip()
        exam_str = fields[5].get().strip()
        
        # Validation
        if not all([code, name, cw1_str, cw2_str, cw3_str, exam_str]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Check if student code already exists
        if code in student_code:
            messagebox.showerror("Error", "Student code already exists!")
            return
        
        try:
            cw1 = int(cw1_str)
            cw2 = int(cw2_str)
            cw3 = int(cw3_str)
            exam = int(exam_str)
            
            # Validate ranges
            if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                return
            
            # Add to lists
            student_code.append(code)
            student_name.append(name)
            coursework1.append(cw1)
            coursework2.append(cw2)
            coursework3.append(cw3)
            exam_mark.append(exam)
            
            total_cw = cw1 + cw2 + cw3
            total_coursework.append(total_cw)
            
            total_marks = total_cw + exam
            percentage = (total_marks / 160) * 100
            overall_percentage.append(round(percentage, 2))
            
            grade = calculate_grade(percentage)
            student_grade.append(grade)
            
            # Save to file
            if save_data_to_file():
                messagebox.showinfo("Success", f"Student {name} added successfully!")
                update_statistics()
                update_performance_display()
                view_all_records()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks!")
    
    # Buttons
    btn_frame = Frame(form_frame, bg=CARD_BG)
    btn_frame.pack(pady=(0, 30))
    save_btn = Button(btn_frame, text="Add Student", font=("Arial", 13, "bold"), bg=ACCENT_PRIMARY, fg="white", command=save_student, padx=40, pady=12, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    save_btn.pack(side=LEFT, padx=10)
    cancel_btn = Button(btn_frame, text="Cancel", font=("Arial", 13), bg=SIDEBAR_BG, fg="white", command=view_all_records, padx=40, pady=12, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    cancel_btn.pack(side=LEFT, padx=10)
    
    # Pack canvas and scrollbar
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Bind mousewheel for scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

# Delete student record
def delete_student_record():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No student records found!")
        return
    
    # Clear display area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Create main container
    main_frame = Frame(content_area, bg=BG_MAIN)
    main_frame.pack(fill=BOTH, expand=True)
    
    # Modern Header Section
    header_container = Frame(main_frame, bg=ACCENT_PRIMARY, height=120)
    header_container.pack(fill=X)
    header_container.pack_propagate(False)
    header_content = Frame(header_container, bg=ACCENT_PRIMARY)
    header_content.pack(fill=BOTH, expand=True, padx=40, pady=20)
    
    # Back button in header
    back_btn = Button(header_content, text="← Back", font=("Arial", 11, "bold"), bg=SIDEBAR_BG, fg=BG_MAIN, command=view_all_records,padx=25, pady=10, bd=0, cursor="hand2", relief=FLAT)
    back_btn.pack(side=LEFT)
    
    # Header title
    title_frame = Frame(header_content, bg=ACCENT_PRIMARY)
    title_frame.pack(side=LEFT, padx=30)
    delete_label=Label(title_frame, text="Delete Student", font=("Arial", 26, "bold"),bg=ACCENT_PRIMARY, fg="white")
    delete_label.pack(anchor=W)
    
    # Create canvas with scrollbar
    canvas = Canvas(main_frame, bg=BG_MAIN, highlightthickness=0)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=BG_MAIN)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)
    
    # Content container with max width
    content_container = Frame(scrollable_frame, bg=BG_MAIN)
    content_container.pack(fill=X, padx=80, pady=40)
    
    # Modern Search Card
    search_card = Frame(content_container, bg=CARD_BG, relief=FLAT, height=100)
    search_card.pack(fill=X)
    
    # Add subtle shadow effect
    shadow = Frame(search_card, bg="#E0D5CC", height=1)
    shadow.pack(fill=X, side=BOTTOM)
    search_inner = Frame(search_card, bg=CARD_BG)
    search_inner.pack(fill=X, padx=50, pady=40)
    
    # Search header
    search_std=Label(search_inner, text="🔍 Find Student", font=("Georgia", 20, "bold"),bg=CARD_BG, fg=TEXT_PRIMARY)
    search_std.pack(anchor=W, pady=(0, 10))
    
    # Modern search input container
    search_container = Frame(search_inner, bg=CARD_BG)
    search_container.pack(fill=X)
    
    # Search input with icon
    input_wrapper = Frame(search_container, bg="white", relief=FLAT,highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
    input_wrapper.pack(side=LEFT, fill=X, expand=True, padx=(0, 15))
    
    # Search icon
    search_label=Label(input_wrapper, text="🔍", font=("Arial", 16), bg="white")
    search_label.pack(side=LEFT, padx=(15, 5))
    search_entry = Entry(input_wrapper, font=("Arial", 13), bd=0, bg="white",fg=TEXT_PRIMARY, relief=FLAT)
    search_entry.pack(side=LEFT, fill=BOTH, expand=True, ipady=12, padx=(5, 15))
    search_entry.focus()
    
    # Modern search button
    search_btn = Button(search_container, text="Search", font=("Arial", 12, "bold"),bg=ACCENT_PRIMARY, fg="white", padx=40, pady=15, bd=0,cursor="hand2", relief=FLAT)
    search_btn.pack(side=LEFT)
    
    # Hover effects for search button
    def on_enter(e):
        search_btn.configure(bg="#A86530")
    def on_leave(e):
        search_btn.configure(bg=ACCENT_PRIMARY)
    search_btn.bind("<Enter>", on_enter)
    search_btn.bind("<Leave>", on_leave)
    
    # Modern dropdown for suggestions
    dropdown_frame = Frame(search_inner, bg=CARD_BG)
    dropdown_frame.pack(fill=X, pady=(15, 0))
    dropdown_list = Listbox(dropdown_frame, font=("Arial", 11), height=0, bd=0, bg="white", selectbackground=ACCENT_SECONDARY,selectforeground=TEXT_PRIMARY, relief=FLAT,highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
    dropdown_scrollbar = Scrollbar(dropdown_frame, command=dropdown_list.yview)
    dropdown_list.configure(yscrollcommand=dropdown_scrollbar.set)
    
    # Result display area
    result_frame = Frame(content_container, bg=BG_MAIN)
    result_frame.pack(fill=X)
    
    def show_suggestions(event=None):
        typed = search_entry.get().strip().lower()
        dropdown_list.delete(0, END)
        
        if typed:
            matches = []
            for i in range(len(student_code)):
                if typed in student_code[i].lower() or typed in student_name[i].lower():
                    matches.append(f"{student_name[i]} - {student_code[i]}")
            
            if matches:
                dropdown_list.config(height=min(6, len(matches)))
                for match in matches:
                    dropdown_list.insert(END, match)
                dropdown_list.pack(side=LEFT, fill=BOTH, expand=True, pady=10)
                dropdown_scrollbar.pack(side=RIGHT, fill=Y, pady=10)
            else:
                dropdown_list.pack_forget()
                dropdown_scrollbar.pack_forget()
        else:
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
    
    def click_suggestion(event):
        if dropdown_list.size() > 0:
            selected = dropdown_list.curselection()
            if selected:
                text = dropdown_list.get(selected[0])
                code = text.split(" - ")[-1]
                search_entry.delete(0, END)
                search_entry.insert(0, code)
                dropdown_list.pack_forget()
                dropdown_scrollbar.pack_forget()
                search_student()
    
    def press_enter(event):
        if dropdown_list.size() > 0 and dropdown_list.winfo_viewable():
            first = dropdown_list.get(0)
            code = first.split(" - ")[-1]
            search_entry.delete(0, END)
            search_entry.insert(0, code)
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
        search_student()
    
    search_entry.bind("<KeyRelease>", show_suggestions)
    search_entry.bind("<Return>", press_enter)
    dropdown_list.bind("<ButtonRelease-1>", click_suggestion)
    
    def search_student():
        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()
            
        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a student code or name")
            return
        
        # Find student
        found = False
        index = -1
        for i in range(len(student_code)):
            if (search_term.lower() == student_code[i].lower() or 
                search_term.lower() in student_name[i].lower()):
                found = True
                index = i
                break
        
        if found:
            # Modern student detail card
            grade_colors = {'A': "#BF7640", 'B': "#8B764D", 'C': "#96522B",'D': "#603200", 'F': "#3D1F00"}
            
            # Main card container
            detail_card = Frame(result_frame, bg=CARD_BG, relief=FLAT)
            detail_card.pack(fill=X, pady=20)
            
            # Danger indicator bar at top
            danger_bar = Frame(detail_card, bg="#E53935", height=6)
            danger_bar.pack(fill=X)
            
            # Card content
            card_padding = Frame(detail_card, bg=CARD_BG)
            card_padding.pack(fill=X, padx=50, pady=40)
            
            # Warning banner
            warning_banner = Frame(card_padding, bg="#FFEBEE", relief=FLAT,highlightbackground="#E53935", highlightthickness=2)
            warning_banner.pack(fill=X, pady=(0, 30))
            warning_content = Frame(warning_banner, bg="#FFEBEE")
            warning_content.pack(fill=X, padx=25, pady=20)
            warning_icon=Label(warning_content, text="⚠", font=("Arial", 32),bg="#FFEBEE", fg="#E53935")
            warning_icon.pack(side=LEFT, padx=(0, 15))
            warning_text_frame = Frame(warning_content, bg="#FFEBEE")
            warning_text_frame.pack(side=LEFT, fill=X, expand=True)
            warning_msg1=Label(warning_text_frame, text="Warning: Permanent Action",font=("Arial", 14, "bold"), bg="#FFEBEE", fg="#C62828",anchor=W)
            warning_msg1.pack(fill=X)
            warning_msg2=Label(warning_text_frame, text="This student record will be permanently deleted and cannot be recovered.", font=("Arial", 10), bg="#FFEBEE", fg="#D32F2F", anchor=W)
            warning_msg2.pack(fill=X, pady=(3, 0))
            
            # Student profile section
            profile_section = Frame(card_padding, bg="#FFF8F0", relief=FLAT)
            profile_section.pack(fill=X, pady=(0, 25))
            profile_inner = Frame(profile_section, bg="#FFF8F0")
            profile_inner.pack(fill=X, padx=30, pady=30)
            
            # Profile header
            profile_header = Frame(profile_inner, bg="#FFF8F0")
            profile_header.pack(fill=X, pady=(0, 20))
            
            # Student avatar
            avatar_frame = Frame(profile_header, bg=ACCENT_PRIMARY, width=80, height=80)
            avatar_frame.pack(side=LEFT, padx=(0, 20))
            avatar_frame.pack_propagate(False)
            avatar_icon=Label(avatar_frame, text="👤", font=("Arial", 40),bg=ACCENT_PRIMARY, fg="white")
            avatar_icon.pack(expand=True)
            
            # Student info
            info_header = Frame(profile_header, bg="#FFF8F0")
            info_header.pack(side=LEFT, fill=BOTH, expand=True)
            std_name=Label(info_header, text=student_name[index], font=("Georgia", 22, "bold"),bg="#FFF8F0", fg=TEXT_PRIMARY, anchor=W)
            std_name.pack(fill=X)
            std_id=Label(info_header, text=f"Student ID: {student_code[index]}",font=("Arial", 12), bg="#FFF8F0", fg=TEXT_SECONDARY, anchor=W)
            std_id.pack(fill=X, pady=(5, 0))
            
            # Grade badge
            grade_badge = Frame(profile_header, bg=grade_colors.get(student_grade[index], '#999'),relief=FLAT, width=70, height=70)
            grade_badge.pack(side=RIGHT)
            grade_badge.pack_propagate(False)
            std_grade=Label(grade_badge, text=student_grade[index], font=("Georgia", 28, "bold"),bg=grade_colors.get(student_grade[index], '#999'),fg="white")
            std_grade.pack(expand=True)
            
            # Divider
            Frame(profile_inner, bg=ACCENT_SECONDARY, height=1).pack(fill=X, pady=20)
            
            # Stats grid
            stats_grid = Frame(profile_inner, bg="#FFF8F0")
            stats_grid.pack(fill=X)
            
            stats_data = [
                ("Coursework Total", f"{total_coursework[index]}/60", "📚"),
                ("Exam Score", f"{exam_mark[index]}/100", "📝"),
                ("Overall Percentage", f"{overall_percentage[index]}%", "🎯")]
            
            for i, (label, value, icon) in enumerate(stats_data):
                stat_col = Frame(stats_grid, bg="white", relief=FLAT)
                stat_col.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
                stat_inner = Frame(stat_col, bg="white")
                stat_inner.pack(fill=X, padx=20, pady=15)
                inner_label1=Label(stat_inner, text=icon, font=("Arial", 20),bg="white")
                inner_label1.pack(pady=(0, 5))
                inner_label2=Label(stat_inner, text=label, font=("Arial", 9),bg="white", fg=TEXT_SECONDARY)
                inner_label2.pack()
                inner_label3=Label(stat_inner, text=value, font=("Arial", 16, "bold"),bg="white", fg=TEXT_PRIMARY)
                inner_label3.pack(pady=(5, 0))
            
            # Confirmation section
            confirm_section = Frame(card_padding, bg=CARD_BG)
            confirm_section.pack(fill=X, pady=(20, 0))
            
            confirmation=Label(confirm_section, text="Are you sure you want to delete this student?",font=("Arial", 13, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
            confirmation.pack(pady=(0, 25))
            
            def delete_confirmed():
                # Remove from all lists
                student_code.pop(index)
                student_name.pop(index)
                coursework1.pop(index)
                coursework2.pop(index)
                coursework3.pop(index)
                exam_mark.pop(index)
                total_coursework.pop(index)
                overall_percentage.pop(index)
                student_grade.pop(index)
                
                # Save to file
                if save_data_to_file():
                    messagebox.showinfo("Success", "Student record deleted successfully!")
                    update_statistics()
                    update_performance_display()
                    view_all_records()
            
            def cancel_delete():
                for widget in result_frame.winfo_children():
                    widget.destroy()
                search_entry.delete(0, END)
                search_entry.focus()
            
            # Modern action buttons
            btn_container = Frame(confirm_section, bg=CARD_BG)
            btn_container.pack()
            
            # Delete button with hover
            delete_btn = Button(btn_container, text="Delete Student",font=("Arial", 13, "bold"), bg="#E53935", fg="white",command=delete_confirmed, padx=45, pady=15, bd=0,cursor="hand2", relief=FLAT)
            delete_btn.pack(side=LEFT, padx=8)
            
            def delete_hover_enter(e):
                delete_btn.configure(bg="#C62828")
            def delete_hover_leave(e):
                delete_btn.configure(bg="#E53935")
            delete_btn.bind("<Enter>", delete_hover_enter)
            delete_btn.bind("<Leave>", delete_hover_leave)
            
            # Cancel button with hover
            cancel_btn = Button(btn_container, text="Cancel",font=("Arial", 13, "bold"), bg=SIDEBAR_BG, fg="white",command=cancel_delete, padx=45, pady=15, bd=0, cursor="hand2", relief=FLAT)
            cancel_btn.pack(side=LEFT, padx=8)
            
            def cancel_hover_enter(e):
                cancel_btn.configure(bg="#2E1A15")
            def cancel_hover_leave(e):
                cancel_btn.configure(bg=SIDEBAR_BG)
            cancel_btn.bind("<Enter>", cancel_hover_enter)
            cancel_btn.bind("<Leave>", cancel_hover_leave)
            
        else:
            # Modern not found message
            not_found_card = Frame(result_frame, bg=CARD_BG, relief=FLAT)
            not_found_card.pack(fill=X, pady=20)
            not_found_inner = Frame(not_found_card, bg=CARD_BG)
            not_found_inner.pack(fill=X, padx=50, pady=60)
            error1=Label(not_found_inner, text="🔍", font=("Arial", 48),bg=CARD_BG, fg=TEXT_SECONDARY)
            error1.pack(pady=(0, 15))
            error2=Label(not_found_inner, text="Student Not Found",font=("Georgia", 18, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
            error2.pack()
            error3=Label(not_found_inner, text="Please check the student code or name and try again.",font=("Arial", 11), bg=CARD_BG, fg=TEXT_SECONDARY)
            error3.pack(pady=(10, 0))
    
    search_btn.config(command=search_student)
    
    # Pack canvas and scrollbar
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Bind mousewheel for scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

# Update student record
def update_student_record():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No student records found!")
        return
    
    # Clear display area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Create main container
    main_frame = Frame(content_area, bg=BG_MAIN)
    main_frame.pack(fill=BOTH, expand=True)
    
    # Modern Header Section
    header_container = Frame(main_frame, bg=ACCENT_PRIMARY, height=120)
    header_container.pack(fill=X)
    header_container.pack_propagate(False)
    header_content = Frame(header_container, bg=ACCENT_PRIMARY)
    header_content.pack(fill=BOTH, expand=True, padx=40, pady=20)
    
    # Back button in header
    back_btn = Button(header_content, text="← Back", font=("Arial", 11, "bold"), bg=SIDEBAR_BG, fg=BG_MAIN, command=view_all_records, padx=25, pady=10, bd=0, cursor="hand2", relief=FLAT)
    back_btn.pack(side=LEFT)
    
    # Header title
    title_frame = Frame(header_content, bg=ACCENT_PRIMARY)
    title_frame.pack(side=LEFT, padx=30)
    update_label = Label(title_frame, text="Update Student", font=("Arial", 26, "bold"), bg=ACCENT_PRIMARY, fg="white")
    update_label.pack(anchor=W)
    
    # Create canvas with scrollbar
    canvas = Canvas(main_frame, bg=BG_MAIN, highlightthickness=0)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=BG_MAIN)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)
    
    # Content container with max width
    content_container = Frame(scrollable_frame, bg=BG_MAIN)
    content_container.pack(fill=X, padx=80, pady=40)
    
    # Modern Search Card
    search_card = Frame(content_container, bg=CARD_BG, relief=FLAT, height=100)
    search_card.pack(fill=X)
    
    # Add subtle shadow effect
    shadow = Frame(search_card, bg="#E0D5CC", height=1)
    shadow.pack(fill=X, side=BOTTOM)
    search_inner = Frame(search_card, bg=CARD_BG)
    search_inner.pack(fill=X, padx=50, pady=40)
    
    # Search header
    search_std = Label(search_inner, text="🔍 Find Student", font=("Georgia", 20, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
    search_std.pack(anchor=W, pady=(0, 10))
    
    # Modern search input container
    search_container = Frame(search_inner, bg=CARD_BG)
    search_container.pack(fill=X)
    
    # Search input with icon
    input_wrapper = Frame(search_container, bg="white", relief=FLAT, highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
    input_wrapper.pack(side=LEFT, fill=X, expand=True, padx=(0, 15))
    
    # Search icon
    search_label = Label(input_wrapper, text="🔍", font=("Arial", 16), bg="white")
    search_label.pack(side=LEFT, padx=(15, 5))
    search_entry = Entry(input_wrapper, font=("Arial", 13), bd=0, bg="white", fg=TEXT_PRIMARY, relief=FLAT)
    search_entry.pack(side=LEFT, fill=BOTH, expand=True, ipady=12, padx=(5, 15))
    search_entry.focus()
    
    # Modern search button
    search_btn = Button(search_container, text="Search", font=("Arial", 12, "bold"), bg=ACCENT_PRIMARY, fg="white", padx=40, pady=15, bd=0, cursor="hand2", relief=FLAT)
    search_btn.pack(side=LEFT)
    
    # Hover effects for search button
    def on_enter(e):
        search_btn.configure(bg="#A86530")
    def on_leave(e):
        search_btn.configure(bg=ACCENT_PRIMARY)
    search_btn.bind("<Enter>", on_enter)
    search_btn.bind("<Leave>", on_leave)
    
    # Modern dropdown for suggestions
    dropdown_frame = Frame(search_inner, bg=CARD_BG)
    dropdown_frame.pack(fill=X, pady=(15, 0))
    dropdown_list = Listbox(dropdown_frame, font=("Arial", 11), height=0, bd=0, bg="white", selectbackground=ACCENT_SECONDARY, selectforeground=TEXT_PRIMARY, relief=FLAT, highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
    dropdown_scrollbar = Scrollbar(dropdown_frame, command=dropdown_list.yview)
    dropdown_list.configure(yscrollcommand=dropdown_scrollbar.set)
    
    # Result display area
    result_frame = Frame(content_container, bg=BG_MAIN)
    result_frame.pack(fill=X)
    
    def show_suggestions(event=None):
        typed = search_entry.get().strip().lower()
        dropdown_list.delete(0, END)
        
        if typed:
            matches = []
            for i in range(len(student_code)):
                if typed in student_code[i].lower() or typed in student_name[i].lower():
                    matches.append(f"{student_name[i]} - {student_code[i]}")
            
            if matches:
                dropdown_list.config(height=min(6, len(matches)))
                for match in matches:
                    dropdown_list.insert(END, match)
                dropdown_list.pack(side=LEFT, fill=BOTH, expand=True, pady=10)
                dropdown_scrollbar.pack(side=RIGHT, fill=Y, pady=10)
            else:
                dropdown_list.pack_forget()
                dropdown_scrollbar.pack_forget()
        else:
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
    
    def click_suggestion(event):
        if dropdown_list.size() > 0:
            selected = dropdown_list.curselection()
            if selected:
                text = dropdown_list.get(selected[0])
                code = text.split(" - ")[-1]
                search_entry.delete(0, END)
                search_entry.insert(0, code)
                dropdown_list.pack_forget()
                dropdown_scrollbar.pack_forget()
                search_student()
    
    def press_enter(event):
        if dropdown_list.size() > 0 and dropdown_list.winfo_viewable():
            first = dropdown_list.get(0)
            code = first.split(" - ")[-1]
            search_entry.delete(0, END)
            search_entry.insert(0, code)
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
        search_student()
    
    search_entry.bind("<KeyRelease>", show_suggestions)
    search_entry.bind("<Return>", press_enter)
    dropdown_list.bind("<ButtonRelease-1>", click_suggestion)
    
    def search_student():
        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()
            
        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a student code or name")
            return
        
        # Find student
        found = False
        index = -1
        for i in range(len(student_code)):
            if (search_term.lower() == student_code[i].lower() or 
                search_term.lower() in student_name[i].lower()):
                found = True
                index = i
                break
        
        if found:
            show_update_form(index)
        else:
            # Modern not found message
            not_found_card = Frame(result_frame, bg=CARD_BG, relief=FLAT)
            not_found_card.pack(fill=X, pady=20)
            not_found_inner = Frame(not_found_card, bg=CARD_BG)
            not_found_inner.pack(fill=X, padx=50, pady=60)
            error1 = Label(not_found_inner, text="🔍", font=("Arial", 48), bg=CARD_BG, fg=TEXT_SECONDARY)
            error1.pack(pady=(0, 15))
            error2 = Label(not_found_inner, text="Student Not Found", font=("Georgia", 18, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
            error2.pack()
            error3 = Label(not_found_inner, text="Please check the student code or name and try again.", font=("Arial", 11), bg=CARD_BG, fg=TEXT_SECONDARY)
            error3.pack(pady=(10, 0))
    
    def show_update_form(index):
        # Clear result frame
        for widget in result_frame.winfo_children():
            widget.destroy()
        
        # Main update card
        update_card = Frame(result_frame, bg=CARD_BG, relief=FLAT)
        update_card.pack(fill=X, pady=20)
        
        # Info indicator bar at top
        info_bar = Frame(update_card, bg=ACCENT_PRIMARY, height=6)
        info_bar.pack(fill=X)
        
        # Card content
        card_padding = Frame(update_card, bg=CARD_BG)
        card_padding.pack(fill=X, padx=50, pady=40)
        
        # Info banner
        info_banner = Frame(card_padding, bg="#E8F5E9", relief=FLAT, highlightbackground=ACCENT_PRIMARY, highlightthickness=2)
        info_banner.pack(fill=X, pady=(0, 30))
        info_content = Frame(info_banner, bg="#E8F5E9")
        info_content.pack(fill=X, padx=25, pady=20)
        info_icon = Label(info_content, text="✏️", font=("Arial", 32), bg="#E8F5E9", fg=ACCENT_PRIMARY)
        info_icon.pack(side=LEFT, padx=(0, 15))
        info_text_frame = Frame(info_content, bg="#E8F5E9")
        info_text_frame.pack(side=LEFT, fill=X, expand=True)
        info_msg1 = Label(info_text_frame, text="Update Student Information", font=("Arial", 14, "bold"), bg="#E8F5E9", fg="#2E7D32", anchor=W)
        info_msg1.pack(fill=X)
        info_msg2 = Label(info_text_frame, text="Modify the details below and save your changes.", font=("Arial", 10), bg="#E8F5E9", fg="#388E3C", anchor=W)
        info_msg2.pack(fill=X, pady=(3, 0))
        
        # Student profile section
        profile_section = Frame(card_padding, bg="#FFF8F0", relief=FLAT)
        profile_section.pack(fill=X, pady=(0, 25))
        profile_inner = Frame(profile_section, bg="#FFF8F0")
        profile_inner.pack(fill=X, padx=30, pady=30)
        
        # Profile header
        profile_header = Frame(profile_inner, bg="#FFF8F0")
        profile_header.pack(fill=X, pady=(0, 20))
        
        # Student avatar
        avatar_frame = Frame(profile_header, bg=ACCENT_PRIMARY, width=80, height=80)
        avatar_frame.pack(side=LEFT, padx=(0, 20))
        avatar_frame.pack_propagate(False)
        avatar_icon = Label(avatar_frame, text="👤", font=("Arial", 40), bg=ACCENT_PRIMARY, fg="white")
        avatar_icon.pack(expand=True)
        
        # Student info
        info_header = Frame(profile_header, bg="#FFF8F0")
        info_header.pack(side=LEFT, fill=BOTH, expand=True)
        current_name = Label(info_header, text=student_name[index], font=("Georgia", 22, "bold"), bg="#FFF8F0", fg=TEXT_PRIMARY, anchor=W)
        current_name.pack(fill=X)
        current_id = Label(info_header, text=f"Student ID: {student_code[index]}", font=("Arial", 12), bg="#FFF8F0", fg=TEXT_SECONDARY, anchor=W)
        current_id.pack(fill=X, pady=(5, 0))
        
        # Divider
        Frame(profile_inner, bg=ACCENT_SECONDARY, height=1).pack(fill=X, pady=20)
        
        # Form section
        form_section = Frame(card_padding, bg=CARD_BG)
        form_section.pack(fill=X)
        form_title = Label(form_section, text="📝 Update Details", font=("Georgia", 18, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W)
        form_title.pack(fill=X, pady=(0, 25))
        
        # Create entry fields
        entries = {}
        
        # Student Name
        name_container = Frame(form_section, bg=CARD_BG)
        name_container.pack(fill=X, pady=(0, 20))
        name_label = Label(name_container, text="Student Name", font=("Arial", 11, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W)
        name_label.pack(fill=X, pady=(0, 8))
        name_wrapper = Frame(name_container, bg="white", relief=FLAT, highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
        name_wrapper.pack(fill=X)
        name_icon = Label(name_wrapper, text="👤", font=("Arial", 14), bg="white")
        name_icon.pack(side=LEFT, padx=(15, 5))
        entries['name'] = Entry(name_wrapper, font=("Arial", 13), bd=0, bg="white", fg=TEXT_PRIMARY, relief=FLAT)
        entries['name'].insert(0, student_name[index])
        entries['name'].pack(side=LEFT, fill=BOTH, expand=True, ipady=12, padx=(5, 15))
        
        # Student Code
        code_container = Frame(form_section, bg=CARD_BG)
        code_container.pack(fill=X, pady=(0, 20))
        code_label = Label(code_container, text="Student Code", font=("Arial", 11, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W)
        code_label.pack(fill=X, pady=(0, 8))
        code_wrapper = Frame(code_container, bg="white", relief=FLAT, highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
        code_wrapper.pack(fill=X)
        code_icon = Label(code_wrapper, text="🔖", font=("Arial", 14), bg="white")
        code_icon.pack(side=LEFT, padx=(15, 5))
        entries['code'] = Entry(code_wrapper, font=("Arial", 13), bd=0, bg="white", fg=TEXT_PRIMARY, relief=FLAT)
        entries['code'].insert(0, student_code[index])
        entries['code'].pack(side=LEFT, fill=BOTH, expand=True, ipady=12, padx=(5, 15))
        
        # Coursework scores section
        coursework_title = Label(form_section, text="📚 Coursework Scores", font=("Georgia", 16, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W)
        coursework_title.pack(fill=X, pady=(30, 20))
        
        # Coursework grid
        coursework_grid = Frame(form_section, bg=CARD_BG)
        coursework_grid.pack(fill=X, pady=(0, 20))
        
        coursework_data = [
            ('coursework1', 'Coursework 1', coursework1[index], '📝'),
            ('coursework2', 'Coursework 2', coursework2[index], '📄'),
            ('coursework3', 'Coursework 3', coursework3[index], '📃')
        ]
        
        for key, label_text, value, icon in coursework_data:
            cw_col = Frame(coursework_grid, bg=CARD_BG)
            cw_col.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
            cw_label = Label(cw_col, text=label_text, font=("Arial", 11, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W)
            cw_label.pack(fill=X, pady=(0, 8))
            cw_wrapper = Frame(cw_col, bg="white", relief=FLAT, highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
            cw_wrapper.pack(fill=X)
            cw_icon = Label(cw_wrapper, text=icon, font=("Arial", 14), bg="white")
            cw_icon.pack(side=LEFT, padx=(15, 5))
            entries[key] = Entry(cw_wrapper, font=("Arial", 13), bd=0, bg="white", fg=TEXT_PRIMARY, relief=FLAT)
            entries[key].insert(0, str(value))
            entries[key].pack(side=LEFT, fill=BOTH, expand=True, ipady=12, padx=(5, 15))
        
        # Exam score
        exam_container = Frame(form_section, bg=CARD_BG)
        exam_container.pack(fill=X, pady=(20, 0))
        exam_label = Label(exam_container, text="Exam Mark (out of 100)", font=("Arial", 11, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W)
        exam_label.pack(fill=X, pady=(0, 8))
        exam_wrapper = Frame(exam_container, bg="white", relief=FLAT, highlightbackground=ACCENT_SECONDARY, highlightthickness=2)
        exam_wrapper.pack(fill=X)
        exam_icon = Label(exam_wrapper, text="📝", font=("Arial", 14), bg="white")
        exam_icon.pack(side=LEFT, padx=(15, 5))
        entries['exam'] = Entry(exam_wrapper, font=("Arial", 13), bd=0, bg="white", fg=TEXT_PRIMARY, relief=FLAT)
        entries['exam'].insert(0, str(exam_mark[index]))
        entries['exam'].pack(side=LEFT, fill=BOTH, expand=True, ipady=12, padx=(5, 15))
        
        # Action buttons section
        action_section = Frame(card_padding, bg=CARD_BG)
        action_section.pack(fill=X, pady=(40, 0))
        
        def save_updates():
            try:
                # Validate inputs
                new_name = entries['name'].get().strip()
                new_code = entries['code'].get().strip()
                new_cw1 = int(entries['coursework1'].get().strip())
                new_cw2 = int(entries['coursework2'].get().strip())
                new_cw3 = int(entries['coursework3'].get().strip())
                new_exam = int(entries['exam'].get().strip())
                
                if not new_name or not new_code:
                    messagebox.showerror("Error", "Name and code cannot be empty!")
                    return
                
                # Check if code already exists (except for current student)
                for i in range(len(student_code)):
                    if i != index and student_code[i].lower() == new_code.lower():
                        messagebox.showerror("Error", "Student code already exists!")
                        return
                
                # Validate coursework scores (0-20)
                if not (0 <= new_cw1 <= 20 and 0 <= new_cw2 <= 20 and 0 <= new_cw3 <= 20):
                    messagebox.showerror("Error", "Coursework scores must be between 0 and 20!")
                    return
                
                # Validate exam mark (0-100)
                if not (0 <= new_exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                    return
                
                # Update data
                student_name[index] = new_name
                student_code[index] = new_code
                coursework1[index] = new_cw1
                coursework2[index] = new_cw2
                coursework3[index] = new_cw3
                exam_mark[index] = new_exam
                
                # Recalculate totals and grade
                total_coursework[index] = new_cw1 + new_cw2 + new_cw3
                overall_percentage[index] = round((total_coursework[index] + new_exam) / 1.6)
                
                # Determine grade
                if overall_percentage[index] >= 70:
                    student_grade[index] = 'A'
                elif overall_percentage[index] >= 60:
                    student_grade[index] = 'B'
                elif overall_percentage[index] >= 50:
                    student_grade[index] = 'C'
                elif overall_percentage[index] >= 40:
                    student_grade[index] = 'D'
                else:
                    student_grade[index] = 'F'
                
                # Save to file
                if save_data_to_file():
                    messagebox.showinfo("Success", "Student record updated successfully!")
                    update_statistics()
                    update_performance_display()
                    view_all_records()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for scores!")
        
        def cancel_update():
            for widget in result_frame.winfo_children():
                widget.destroy()
            search_entry.delete(0, END)
            search_entry.focus()
        
        # Modern action buttons
        btn_container = Frame(action_section, bg=CARD_BG)
        btn_container.pack()
        
        # Save button with hover
        save_btn = Button(btn_container, text="Save Changes", font=("Arial", 13, "bold"), bg=ACCENT_PRIMARY, fg="white", command=save_updates, padx=45, pady=15, bd=0, cursor="hand2", relief=FLAT)
        save_btn.pack(side=LEFT, padx=8)
        
        def save_hover_enter(e):
            save_btn.configure(bg="#A86530")
        def save_hover_leave(e):
            save_btn.configure(bg=ACCENT_PRIMARY)
        save_btn.bind("<Enter>", save_hover_enter)
        save_btn.bind("<Leave>", save_hover_leave)
        
        # Cancel button with hover
        cancel_btn = Button(btn_container, text="Cancel", font=("Arial", 13, "bold"), bg=SIDEBAR_BG, fg="white", command=cancel_update, padx=45, pady=15, bd=0, cursor="hand2", relief=FLAT)
        cancel_btn.pack(side=LEFT, padx=8)
        
        def cancel_hover_enter(e):
            cancel_btn.configure(bg="#2E1A15")
        def cancel_hover_leave(e):
            cancel_btn.configure(bg=SIDEBAR_BG)
        cancel_btn.bind("<Enter>", cancel_hover_enter)
        cancel_btn.bind("<Leave>", cancel_hover_leave)
    
    search_btn.config(command=search_student)
    
    # Pack canvas and scrollbar
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Bind mousewheel for scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

# Function to show updated record
def show_update_form(index):
    # Clear display area
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Header
    header_label = Label(content_area, text=f"Update: {student_name[index]}", font=("Arial", 22, "bold"), bg=BG_MAIN, fg=TEXT_PRIMARY)
    header_label.pack(pady=30)
    
    # Create scrollable frame
    canvas = Canvas(content_area, bg=BG_MAIN, highlightthickness=0)
    scrollbar = Scrollbar(content_area, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=BG_MAIN)
    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Form frame
    form_frame = Frame(scrollable_frame, bg=CARD_BG, relief="raised", borderwidth=2, highlightbackground=ACCENT_PRIMARY, highlightthickness=2)
    form_frame.pack(fill=BOTH, expand=True, padx=100, pady=(0, 30))
    
    # Entry fields
    fields = []
    labels_text = ["Student Code:", "Student Name:", "Coursework 1 (0-20):", "Coursework 2 (0-20):", "Coursework 3 (0-20):", "Exam Mark (0-100):"]
    current_values = [student_code[index], student_name[index], str(coursework1[index]), str(coursework2[index]), str(coursework3[index]), str(exam_mark[index])]
    
    for label_text, value in zip(labels_text, current_values):
        field_frame = Frame(form_frame, bg=CARD_BG)
        field_frame.pack(fill=X, padx=40, pady=12)
        
        lbl=Label(field_frame, text=label_text, font=("Arial", 12, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY, anchor=W)
        lbl.pack(fill=X, pady=(0, 5))
        
        entry = Entry(field_frame, font=("Arial", 13), bd=2, relief="solid", highlightthickness=2, highlightbackground=ACCENT_SECONDARY, highlightcolor=ACCENT_PRIMARY)
        entry.pack(fill=X, ipady=10)
        entry.insert(0, value)
        fields.append(entry)
    
    # Disable student code field
    fields[0].config(state='readonly', bg='#E0E0E0')
    
    def update_student():
        # Get values
        name = fields[1].get().strip()
        cw1_str = fields[2].get().strip()
        cw2_str = fields[3].get().strip()
        cw3_str = fields[4].get().strip()
        exam_str = fields[5].get().strip()
        
        # Validation
        if not all([name, cw1_str, cw2_str, cw3_str, exam_str]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            cw1 = int(cw1_str)
            cw2 = int(cw2_str)
            cw3 = int(cw3_str)
            exam = int(exam_str)
            
            # Validate ranges
            if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                return
            
            # Update lists
            student_name[index] = name
            coursework1[index] = cw1
            coursework2[index] = cw2
            coursework3[index] = cw3
            exam_mark[index] = exam
            
            total_cw = cw1 + cw2 + cw3
            total_coursework[index] = total_cw
            
            total_marks = total_cw + exam
            percentage = (total_marks / 160) * 100
            overall_percentage[index] = round(percentage, 2)
            
            grade = calculate_grade(percentage)
            student_grade[index] = grade
            
            # Save to file
            if save_data_to_file():
                messagebox.showinfo("Success", f"Student {name} updated successfully!")
                update_statistics()
                update_performance_display()
                view_all_records()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for marks!")
    
    # Buttons
    btn_frame = Frame(form_frame, bg=CARD_BG)
    btn_frame.pack(pady=30)
    update_btn = Button(btn_frame, text="Update Student", font=("Arial", 13, "bold"), bg=ACCENT_PRIMARY, fg="white", command=update_student, padx=40, pady=12, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    update_btn.pack(side=LEFT, padx=10)
    cancel_btn = Button(btn_frame, text="Cancel", font=("Arial", 13), bg=SIDEBAR_BG, fg="white", command=view_all_records, padx=40, pady=12, bd=0, cursor="hand2", relief="raised", borderwidth=3)
    cancel_btn.pack(side=LEFT, padx=10)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

# Main container
main_container = Frame(root, bg=BG_MAIN)
main_container.pack(fill=BOTH, expand=True)

# Sidebar 
sidebar_frame = Frame(main_container, bg=SIDEBAR_BG, width=230, highlightbackground="#8B764D", highlightthickness=1)
sidebar_frame.pack(side=LEFT, fill=Y)
sidebar_frame.pack_propagate(False)
sidebar_header = Frame(sidebar_frame, bg=ACCENT_PRIMARY, height=140)
sidebar_header.pack(fill=X)
sidebar_header.pack_propagate(False)
profile_section = Frame(sidebar_header, bg=ACCENT_PRIMARY)
profile_section.pack(expand=True, pady=20)
l44 = Label(profile_section, text="👤", font=("Arial", 40), bg=ACCENT_PRIMARY, fg="white")
l44.pack()
l45 = Label(profile_section, text="Admin User", font=("Arial", 13, "bold"), bg=ACCENT_PRIMARY, fg="#FFFFFF")
l45.pack(pady=(5, 2))
sidebar_menu = Frame(sidebar_frame, bg=SIDEBAR_BG)
sidebar_menu.pack(fill=BOTH, expand=True, pady=20)

# Menu items with proper button creation
def create_menu_button(parent, icon, text, command):
    btn = Button(parent, text=f"{icon}  {text}", font=("Arial", 11), bg=SIDEBAR_BG, fg="#FFFFFF", bd=0, anchor=W, padx=20, pady=12, activebackground=ACCENT_SECONDARY, cursor="hand2", command=command)
    btn.pack(fill=X, padx=10, pady=3)
    
    def on_enter(e):
        btn.configure(bg="#8B764D")
    def on_leave(e):
        btn.configure(bg=SIDEBAR_BG)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

create_menu_button(sidebar_menu, "🏫", "Dashboard", show_dashboard)
create_menu_button(sidebar_menu, "📋", "View All Records", view_all_records)
create_menu_button(sidebar_menu, "🔎", "View Individual Record", view_individual_record)
create_menu_button(sidebar_menu, "🏆", "Highest Score", show_highest_score)
create_menu_button(sidebar_menu, "⚠️", "Lowest Score", show_lowest_score)
create_menu_button(sidebar_menu, "🔄", "Sort Records", sort_student_records)
create_menu_button(sidebar_menu, "➕", "Add Student", add_student_record)
create_menu_button(sidebar_menu, "❌", "Delete Student", delete_student_record) 
create_menu_button(sidebar_menu, "✏️", "Update Student", update_student_record)

# Sidebar footer
sidebar = Frame(sidebar_frame, bg="#8B764D", height=1)
sidebar.pack(fill=X, side=BOTTOM, pady=(10, 0))
sidebar_footer = Frame(sidebar_frame, bg=SIDEBAR_BG)
sidebar_footer.pack(side=BOTTOM, fill=X, pady=15)
footer = Label(sidebar_footer, text="admin@gmail.com", font=("Arial", 9), bg=SIDEBAR_BG, fg="#B0B0B0")
footer.pack(pady=5)
content_area = Frame(main_container, bg=BG_MAIN)
content_area.pack(side=RIGHT, fill=BOTH, expand=True)

# Load data and show dashboard
root.after(100, load_data)
root.after(150, show_dashboard)
root.mainloop()