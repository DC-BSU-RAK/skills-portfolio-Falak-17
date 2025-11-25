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
    with open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\studentMarks.txt") as file_handler:
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