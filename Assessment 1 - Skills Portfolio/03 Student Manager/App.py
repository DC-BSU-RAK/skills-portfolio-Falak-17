from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

root = Tk()
root.geometry("1200x700")
root.title("Student Manager")
root.configure(bg="#635436")

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

# Function to create stat card
def create_stat_card(parent, title, value, color, icon):
    card = Frame(parent, bg=color, highlightbackground="#85b5b1", highlightthickness=1, height=120)
    card.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
    card.pack_propagate(False)
    
    content = Frame(card, bg=color)
    content.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    icon_label=Label(content, text=icon, font=("Arial", 18), bg=color, fg="white")
    icon_label.pack(anchor=W)
    value_label=Label(content, text=value, font=("Arial", 16, "bold"), bg=color, fg="white")
    value_label.pack(anchor=W, pady=(3, 0))
    title_label=Label(content, text=title, font=("Arial", 9), bg=color, fg="white")
    title_label.pack(anchor=W, pady=(2, 0))

# Function to update statistics cards
def update_statistics():
    for widget in stat_cards_container.winfo_children():
        widget.destroy()
    
    if len(student_code) > 0:
        total_students = len(student_code)
        avg_percentage = round(sum(overall_percentage) / len(overall_percentage), 1)
        grade_a_count = student_grade.count('A')
        avg_exam = round(sum(exam_mark) / len(exam_mark), 1)
        
        create_stat_card(stat_cards_container, "Total Students", str(total_students), "#FFB74D", "👥")
        create_stat_card(stat_cards_container, "Average Score", f"{avg_percentage}%", "#7B1FA2", "📊")
        create_stat_card(stat_cards_container, "Grade A Students", str(grade_a_count), "#66BB6A", "⭐")
        create_stat_card(stat_cards_container, "Avg Exam Score", f"{avg_exam}/100", "#42A5F5", "📝")

# Function to update overall performance display
def update_performance_display():
    for widget in perf_scrollable.winfo_children():
        widget.destroy()
    
    if len(student_code) == 0:
        Label(perf_scrollable, text="No student data available",font=("Arial", 12), bg="white", fg="#999").pack(pady=30)
    else:
        grade_colors = {'A': "#13B618", 'B': "#2383D1", 'C': "#FFF700", 'D': "#FFA200", 'F': "#FF1302"}
        
        for i in range(len(student_code)):
            shadow_frame = Frame(perf_scrollable, bg="#8B7355", highlightthickness=0)
            shadow_frame.pack(fill=X, padx=22, pady=7)
            
            # Main card with 3D raised effect
            student_card = Frame(shadow_frame, bg="#c1a06e", highlightbackground="#D4AF7A",highlightthickness=2, relief=RAISED, bd=3)
            student_card.pack(fill=X, padx=0, pady=0)
            
            color_indicator = Frame(student_card, bg=grade_colors.get(student_grade[i], '#999'), width=7)
            color_indicator.pack(side=LEFT, fill=Y)
            
            info_frame = Frame(student_card, bg="#c1a06e")
            info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
            name_row = Frame(info_frame, bg="#c1a06e")
            name_row.pack(fill=X)
            
            name=Label(name_row, text=student_name[i], font=("Georgia", 14, "bold"),bg="#c1a06e", fg="#2C1810")
            name.pack(side=LEFT)
            student_id=Label(name_row, text=f" ---- {student_code[i]}", font=("Georgia", 12),bg="#c1a06e", fg="#5E4A3C")
            student_id.pack(side=LEFT)
            
            metrics_row = Frame(info_frame, bg="#c1a06e")
            metrics_row.pack(fill=X, pady=(5, 0))
            student_coursework=Label(metrics_row, text=f"Coursework: {total_coursework[i]}/60",font=("Georgia", 10), bg="#c1a06e", fg="#5E4A3C")
            student_coursework.pack(side=LEFT, padx=(0, 1))
            student_obtained_marks=Label(metrics_row, text=f"Exam: {exam_mark[i]}/100",font=("Georgia", 10), bg="#c1a06e", fg="#5E4A3C")
            student_obtained_marks.pack(side=LEFT, padx=(0, 15))
            student_result=Label(metrics_row, text=f"Overall: {overall_percentage[i]}%",font=("Georgia", 10, "bold"), bg="#c1a06e", fg="#2C1810")
            student_result.pack(side=LEFT)
            
            # 3D grade badge with shadow
            grade_container = Frame(student_card, bg="#c1a06e")
            grade_container.pack(side=RIGHT, padx=15, pady=5)
            grade_badge = Label(grade_container, text=student_grade[i],font=("Georgia", 14, "bold"),bg=grade_colors.get(student_grade[i], '#999'),fg="white", width=3, height=1,relief=RAISED, bd=3)
            grade_badge.pack()

# Function to load data from file
def load_data():
    with open("studentMarks.txt", "r") as file_handler:
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
    
    # Hide other views
    for widget in content_area.winfo_children():
        widget.destroy()
    
    # Show dashboard content
    dashboard_content = Frame(content_area, bg="#E6D5C3")
    dashboard_content.pack(fill=BOTH, expand=True)
    bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\background.jpg") 
    bg_image = bg_image.resize((1400, 800)) 
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(dashboard_content, image=bg_photo)
    bg_label.image = bg_photo 
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Header
    header = Frame(dashboard_content, bg="#5E4A3C", height=90)
    header.pack(fill=X)
    header.pack_propagate(False)
    heading=Label(header, text="Dashboard", font=("Arial", 36, "bold"), bg="#5E4A3C", fg="white")
    heading.pack(side=LEFT, padx=(15, 20))
    datetime_frame = Frame(header, bg="#5E4A3C")
    datetime_frame.pack(side=RIGHT, padx=(20, 10))
    current_date = datetime.now().strftime("%A, %d %B %Y")
    date = Label(datetime_frame, text=current_date, font=("Arial", 11), bg="#5E4A3C", fg="#FFFFFF")
    date.pack(side=LEFT, padx=(0, 15))
    time_label = Label(datetime_frame, text="Time: ", font=("Arial", 11), bg="#5E4A3C", fg="#FFFFFF")
    time_label.pack(side=LEFT)
    def update_time():
        current_time = datetime.now().strftime("%I:%M:%S %p")
        time_label.config(text=current_time)
        time_label.after(1000, update_time)  
    update_time() 

    # Statistics Cards Section
    stats_frame = Frame(dashboard_content, bg="#E6D5C3")
    stats_frame.pack(fill=X, padx=20, pady=(15, 10))
    stat_cards_container = Frame(stats_frame, bg="#E6D5C3")
    stat_cards_container.pack(fill=X, padx=10, pady=(10,5))
    bottom_container = Frame(dashboard_content, bg="#E6D5C3")
    bottom_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

    # LEFT - Performance frame
    performance_frame = Frame(bottom_container, bg="white", highlightbackground="#E6D5C3", highlightthickness=1, width=550, height=500)
    performance_frame.pack(side=LEFT, padx=(0, 15))
    performance_frame.pack_propagate(False)
    perf_bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\background 1.jpg") 
    perf_bg_image = perf_bg_image.resize((700, 700))
    perf_bg_photo = ImageTk.PhotoImage(perf_bg_image)
    perf_bg_label = Label(performance_frame, image=perf_bg_photo)
    perf_bg_label.image = perf_bg_photo 
    perf_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    perf_header = Frame(performance_frame, bg="white")
    perf_header.pack(fill=X, padx=20, pady=(15, 10))
    l1=Label(perf_header, text="Overall Student Performance", font=("Georgia", 14, "bold"), bg="white", fg="#333")
    l1.pack(side=LEFT)
    perf_canvas = Canvas(performance_frame, bg="white", highlightthickness=0)
    perf_scrollbar = Scrollbar(performance_frame, orient="vertical", command=perf_canvas.yview)
    perf_scrollable = Frame(perf_canvas, bg="white")  
    perf_scrollable.bind("<Configure>", lambda e: perf_canvas.configure(scrollregion=perf_canvas.bbox("all")))
    perf_canvas.create_window((0, 0), window=perf_scrollable, anchor="nw")
    perf_canvas.configure(yscrollcommand=perf_scrollbar.set)
    perf_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(20, 0), pady=(0, 15))
    perf_scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 5), pady=(0, 15))
    perf_canvas.bind_all("<MouseWheel>", lambda e: perf_canvas.yview_scroll(int(-1*(e.delta/120)), "units")) #Taken from gpt

    # RIGHT - Image frame 
    image_box = Frame(bottom_container, bg="white", highlightbackground="#E6D5C3", highlightthickness=1, width=400, height=500)
    image_box.pack(side=RIGHT, padx=(0, 0))
    image_box.pack_propagate(False)
    image_frame = Frame(image_box, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
    image_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)
    display_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\image.jpg") 
    display_image = display_image.resize((380, 350)) 
    display_photo = ImageTk.PhotoImage(display_image)
    img_label = Label(image_frame, image=display_photo, bg="white")
    img_label.image = display_photo 
    img_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    update_statistics()
    update_performance_display()

# View all student's record
def view_all_records():
    # Hide other content
    for widget in content_area.winfo_children():
        widget.destroy()

    # Create records frame with background
    records_frame = Frame(content_area, bg="#E6D5C3")
    records_frame.pack(fill=BOTH, expand=True, padx=20, pady=(20, 20))

    # Load background image
    bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\background.jpg") 
    bg_image = bg_image.resize((1400, 800)) 
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(records_frame, image=bg_photo)
    bg_label.image = bg_photo 
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    canvas = Canvas(records_frame, bg="#E6D5C3", highlightthickness=0)
    scrollbar = Scrollbar(records_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#E6D5C3")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Back button with 3D effect
    back_btn = Button(scrollable_frame, text="← Back", font=("Georgia", 11, "bold"),bg="#5E4A3C", fg="white", command=show_dashboard,padx=20, pady=8, relief=RAISED, bd=3, cursor="hand2")
    back_btn.pack(anchor=W, pady=10, padx=20)

    # Header with 3D frame
    header_shadow = Frame(scrollable_frame, bg="#8B7355")
    header_shadow.pack(anchor=W, padx=32, pady=(10, 5))
    
    header_frame = Frame(header_shadow, bg="#c1a06e", relief=RAISED, bd=3,highlightbackground="#D4AF7A", highlightthickness=2)
    header_frame.pack()
    
    l2=Label(header_frame, text="All Student Records", font=("Georgia", 18, "bold"),bg="#c1a06e", fg="#2C1810", padx=20, pady=10)
    l2.pack()
    grade_colors = {'A': "#13B618", 'B': "#2383D1", 'C': "#FFF700", 'D': "#FFA200", 'F': "#FF1302"}
    for i in range(len(student_code)):
        # Outer shadow frame for 3D effect
        shadow_frame = Frame(scrollable_frame, bg="#8B7355", highlightthickness=0)
        shadow_frame.pack(fill=X, padx=22, pady=7)
        
        # Main card with 3D raised effect
        student_card1 = Frame(shadow_frame, bg="#c1a06e", highlightbackground="#D4AF7A",highlightthickness=2, relief=RAISED, bd=3)
        student_card1.pack(fill=X, padx=0, pady=0)
        color_indicator1 = Frame(student_card1, bg=grade_colors.get(student_grade[i], '#999'), width=7)
        color_indicator1.pack(side=LEFT, fill=Y)
        info_frame1 = Frame(student_card1, bg="#c1a06e")
        info_frame1.pack(side=LEFT, fill=BOTH, expand=True, padx=15, pady=12)
        name_row = Frame(info_frame1, bg="#c1a06e")
        name_row.pack(fill=X)
        l3=Label(name_row, text=student_name[i], font=("Georgia", 12, "bold"),bg="#c1a06e", fg="#2C1810")
        l3.pack(side=LEFT)
        l4=Label(name_row, text=f" ---- {student_code[i]}", font=("Georgia", 10),bg="#c1a06e", fg="#5E4A3C")
        l4.pack(side=LEFT)

        metrics_row1 = Frame(info_frame1, bg="#c1a06e")
        metrics_row1.pack(fill=X, pady=(5, 0))
        l5=Label(metrics_row1, text=f"Coursework: {total_coursework[i]}/60",font=("Georgia", 9), bg="#c1a06e", fg="#5E4A3C")
        l5.pack(side=LEFT, padx=(0, 15))
        l6=Label(metrics_row1, text=f"Exam: {exam_mark[i]}/100",font=("Georgia", 9), bg="#c1a06e", fg="#5E4A3C")
        l6.pack(side=LEFT, padx=(0, 15))
        l7=Label(metrics_row1, text=f"Overall: {overall_percentage[i]}%",font=("Georgia", 9, "bold"), bg="#c1a06e", fg="#2C1810")
        l7.pack(side=LEFT)
        grade_container = Frame(student_card1, bg="#c1a06e")
        grade_container.pack(side=RIGHT, padx=15, pady=5)
        l8=Label(grade_container, text=student_grade[i], font=("Georgia", 14, "bold"),bg=grade_colors.get(student_grade[i], '#999'), fg="white",width=3, height=1, relief=RAISED, bd=3)
        l8.pack()

    # Summary section with 3D effect
    avg_percentage = sum(overall_percentage) / len(overall_percentage)

    # Shadow for summary
    summary_shadow = Frame(scrollable_frame, bg="#8B7355")
    summary_shadow.pack(fill=X, padx=32, pady=20)
    summary_frame = Frame(summary_shadow, bg="#D4AF7A", highlightbackground="#c1a06e",highlightthickness=2, relief=RAISED, bd=3)
    summary_frame.pack(fill=X)
    l9=Label(summary_frame, text="Summary", font=("Georgia", 14, "bold"),bg="#D4AF7A", fg="#2C1810")
    l9.pack(anchor=W, padx=20, pady=(15, 5))
    l10=Label(summary_frame, text=f"Total Students: {len(student_code)}",font=("Georgia", 11), bg="#D4AF7A", fg="#5E4A3C")
    l10.pack(anchor=W, padx=20, pady=3)
    l11=Label(summary_frame, text=f"Average Percentage: {round(avg_percentage, 2)}%",font=("Georgia", 11), bg="#D4AF7A", fg="#5E4A3C")
    l11.pack(anchor=W, padx=20, pady=(3, 15))
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

# View Individual Record with Enhanced Dropdown
def view_individual_record():
    if len(student_code) == 0:
        messagebox.showwarning("No Data", "No data loaded!")
        return
    
    search_window = Toplevel(root)
    search_window.title("Search Student")
    search_window.geometry("450x300")
    search_window.configure(bg="#E6D5C3")
    
    search_label = Label(search_window, text="🔍 Search Student", font=("Arial", 16, "bold"),bg="#E6D5C3", fg="#5E4A3C")
    search_label.pack(pady=20)
    l12 = Label(search_window, text="Enter Student Code or Name:",font=("Arial", 11), bg="#E6D5C3", fg="#5E4A3C")
    l12.pack(pady=(0, 10))
    search_entry = Entry(search_window, font=("Arial", 12), width=30, bd=2,relief="solid", highlightthickness=2,highlightbackground="#5E4A3C", highlightcolor="#3E3027")
    search_entry.pack(pady=10, ipady=8)
    search_entry.focus()
    
    # Dropdown listbox for suggestions
    dropdown_frame = Frame(search_window, bg="#E6D5C3")
    dropdown_frame.pack(fill=X, padx=60)
    dropdown_list = Listbox(dropdown_frame, font=("Arial", 10), height=0,bd=2, relief="solid", highlightthickness=1,highlightbackground="#5E4A3C", bg="white",selectbackground="#5E4A3C", selectforeground="white")
    dropdown_scrollbar = Scrollbar(dropdown_frame, orient="vertical",command=dropdown_list.yview)
    dropdown_list.configure(yscrollcommand=dropdown_scrollbar.set)
    def update_dropdown(event=None):
        search_term = search_entry.get().strip().lower()
        dropdown_list.delete(0, END)
        if search_term:
            matches = []
            for i in range(len(student_code)):
                if search_term in student_code[i].lower() or search_term in student_name[i].lower():
                    matches.append(f"{student_name[i]} - {student_code[i]}")
            
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
    
    def select_from_dropdown(event):
        if dropdown_list.size() > 0:
            selection = dropdown_list.curselection()
            if selection:
                selected = dropdown_list.get(selection[0])
            else:
                selected = dropdown_list.get(0)
            code = selected.split(" - ")[-1]
            search_entry.delete(0, END)
            search_entry.insert(0, code)
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
            search_student()
    
    def handle_keypress(event):
        if event.keysym == 'Down':
            if dropdown_list.size() > 0:
                dropdown_list.focus()
                dropdown_list.selection_clear(0, END)
                dropdown_list.selection_set(0)
                dropdown_list.activate(0)
            return "break"
        elif event.keysym == 'Escape':
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
            return "break"
    
    def handle_listbox_keypress(event):
        if event.keysym == 'Return':
            select_from_dropdown(event)
            return "break"
        elif event.keysym == 'Escape':
            dropdown_list.pack_forget()
            dropdown_scrollbar.pack_forget()
            search_entry.focus()
            return "break"
    
    search_entry.bind("<KeyRelease>", update_dropdown)
    search_entry.bind("<Down>", handle_keypress)
    search_entry.bind("<Escape>", handle_keypress)
    dropdown_list.bind("<Button-1>", select_from_dropdown)
    dropdown_list.bind("<Return>", handle_listbox_keypress)
    dropdown_list.bind("<Escape>", handle_listbox_keypress)
    
    def search_student():
        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a student code or name")
            return
        found = False
        index = -1
        for i in range(len(student_code)):
            if search_term.lower() == student_code[i].lower() or search_term.lower() in student_name[i].lower():
                found = True
                index = i
                break
        
        if found:
            search_window.destroy()
            # Clear content area
            for widget in content_area.winfo_children():
                widget.destroy()
            
            # Main detail frame with dashboard colors
            detail_frame = Frame(content_area, bg="#E6D5C3")
            detail_frame.pack(fill=BOTH, expand=True)
            bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\background.jpg")
            bg_image = bg_image.resize((1400, 800))
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(detail_frame, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            header = Frame(detail_frame, bg="#5E4A3C", height=90)
            header.pack(fill=X)
            header.pack_propagate(False)
            heading = Label(header, text="Student Details", font=("Arial", 36, "bold"),bg="#5E4A3C", fg="white")
            heading.pack(side=LEFT, padx=(15, 20))
            
            # DateTime display
            datetime_frame = Frame(header, bg="#5E4A3C")
            datetime_frame.pack(side=RIGHT, padx=(20, 10))
            current_date = datetime.now().strftime("%A, %d %B %Y")
            date = Label(datetime_frame, text=current_date, font=("Arial", 11),bg="#5E4A3C", fg="#FFFFFF")
            date.pack(side=LEFT, padx=(0, 15))
            time_label = Label(datetime_frame, text="", font=("Arial", 11),bg="#5E4A3C", fg="#FFFFFF")
            time_label.pack(side=LEFT)
            
            def update_time():
                current_time = datetime.now().strftime("%I:%M:%S %p")
                time_label.config(text=current_time)
                time_label.after(1000, update_time)
            update_time()
            
            # Content container with scrollbar
            content_container = Frame(detail_frame, bg="#E6D5C3")
            content_container.pack(fill=BOTH, expand=True, padx=40, pady=30)
            
            # Create canvas and scrollbar for scrolling
            canvas = Canvas(content_container, bg="#745F48", highlightthickness=0)
            scrollbar = Scrollbar(content_container, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg="#745F48")
            scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            # Bind mousewheel
            canvas.bind_all("<MouseWheel>",lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
            back_btn = Button(scrollable_frame, text="← Back", font=("Arial", 11, "bold"),bg="#5E4A3C", fg="white", command=show_dashboard,padx=20, pady=10, bd=0, cursor="hand2",relief="raised", borderwidth=3)
            back_btn.pack(anchor=W, pady=(0, 20))
            # Main card with 3D effect
            card = Frame(scrollable_frame, bg="white",highlightbackground="#5E4A3C", highlightthickness=2,relief="raised", borderwidth=5)
            card.pack(fill=BOTH, expand=True, padx=60, pady=20)
            
            # Grade color definitions
            grade_colors = {
                'A': '#4CAF50', 
                'B': '#2196F3', 
                'C': '#FF9800', 
                'D': '#FF5722', 
                'F': '#F44336'
            }
            
            # Top color bar with 3D effect
            color_bar = Frame(card, bg=grade_colors.get(student_grade[index], '#999'),height=10, relief="raised", borderwidth=2)
            color_bar.pack(fill=X)
            content = Frame(card, bg="white")
            content.pack(fill=BOTH, expand=True, padx=60, pady=40)
            icon_frame = Frame(content, bg="#461180", relief="raised", borderwidth=3,highlightbackground="#5E4A3C", highlightthickness=2)
            icon_frame.pack(pady=(10, 20))
            
            l13 = Label(icon_frame, text="👤", font=("Arial", 50), bg="white",padx=30, pady=20)
            l13.pack()
            l14 = Label(content, text=student_name[index], font=("Georgia", 24, "bold"),bg="white", fg="#5E4A3C")
            l14.pack(pady=(10, 5))
            code_frame = Frame(content, bg="#E6D5C3", relief="raised", borderwidth=2)
            code_frame.pack(pady=10)
            l15 = Label(code_frame, text=f"Code: {student_code[index]}",font=("Arial", 13, "bold"), bg="#E6D5C3", fg="#5E4A3C",padx=20, pady=8)
            l15.pack()
            
            # Divider with 3D effect
            frame = Frame(content, bg="#5E4A3C", height=3, relief="sunken",borderwidth=1)
            frame.pack(fill=X, pady=25)
            
            # Statistics section - HORIZONTAL LAYOUT
            stats_container = Frame(content, bg="white")
            stats_container.pack(fill=X, pady=15)
            
            stats = [
                ("Total Coursework", f"{total_coursework[index]} / 60", "#4CAF50"),
                ("Exam Mark", f"{exam_mark[index]} / 100", "#2196F3"),
                ("Overall Percentage", f"{overall_percentage[index]}%", "#FF9800"),]
            
            # Create horizontal layout for stats
            for idx, (label, value, color) in enumerate(stats):
                stat_card = Frame(stats_container, bg=color, relief="raised",borderwidth=3, highlightbackground="#5E4A3C",highlightthickness=1)
                stat_card.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=8)
                stat_inner = Frame(stat_card, bg="white")
                stat_inner.pack(fill=BOTH, expand=True, padx=3, pady=3)
                l16 = Label(stat_inner, text=label, font=("Arial", 11, "bold"),bg="white", fg="#5E4A3C")
                l16.pack(pady=(15, 5))
                l17 = Label(stat_inner, text=value, font=("Arial", 16, "bold"),bg="white", fg=color)
                l17.pack(pady=(5, 15))
            
            # Divider
            frame1 = Frame(content, bg="#5E4A3C", height=3, relief="sunken",borderwidth=1)
            frame1.pack(fill=X, pady=25)
            grade_outer = Frame(content, bg=grade_colors.get(student_grade[index], '#999'),relief="raised", borderwidth=5,highlightbackground="#5E4A3C", highlightthickness=2)
            grade_outer.pack(fill=X, pady=(10, 20), padx=200)
            grade_frame = Frame(grade_outer,bg=grade_colors.get(student_grade[index], '#999'))
            grade_frame.pack(fill=X, padx=5, pady=5)
            l18 = Label(grade_frame, text=f"Final Grade: {student_grade[index]}",font=("Georgia", 20, "bold"),bg=grade_colors.get(student_grade[index], '#999'),fg="white", pady=20)
            l18.pack()
        else:
            messagebox.showinfo("Not Found", "Student not found!")
    
    btn_frame = Frame(search_window, bg="#E6D5C3")
    btn_frame.pack(pady=20)
    search_btn = Button(btn_frame, text="Search", font=("Arial", 11, "bold"),bg="#31271F", fg="white", command=search_student,padx=30, pady=10, bd=0, cursor="hand2",relief="raised", borderwidth=3)
    search_btn.pack(side=LEFT, padx=5)
    cancel_btn = Button(btn_frame, text="Cancel", font=("Arial", 11),bg="#5E4A3C", fg="white", command=search_window.destroy,padx=30, pady=10, bd=0, cursor="hand2",relief="raised", borderwidth=3)
    cancel_btn.pack(side=LEFT, padx=5)
    search_entry.bind("<Return>", lambda e: search_student())

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
    
    # Main detail frame with dashboard colors
    detail_frame = Frame(content_area, bg="#E6D5C3")
    detail_frame.pack(fill=BOTH, expand=True)
    bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\image 1.jpg")
    bg_image = bg_image.resize((1400, 800))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(detail_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Content container WITHOUT scrollbar
    content_container = Frame(detail_frame, bg="#E6D5C3")
    content_container.pack(fill=BOTH, expand=True, padx=30, pady=15)
    
    # Back button - smaller padding
    HighScore_back_btn=Button(content_container, text="← Back", font=("Arial", 10, "bold"),bg="#5E4A3C", fg="white", command=show_dashboard,padx=15, pady=6, bd=0, cursor="hand2",relief="raised", borderwidth=3)
    HighScore_back_btn.pack(anchor=W, pady=(0, 10))
    
    # Top achievement banner - reduced size
    banner = Frame(content_container, bg="#8B4513", relief="raised",borderwidth=4, highlightbackground="#5E4A3C", highlightthickness=2)
    banner.pack(fill=X, padx=10, pady=(0, 12))
    banner_content = Frame(banner, bg="#D4AF37")
    banner_content.pack(fill=BOTH, expand=True, padx=6, pady=6)
    l19=Label(banner_content, text="═══════════════════════════════════════",font=("Courier", 10, "bold"), bg="#D4AF37", fg="#5E4A3C")
    l19.pack(pady=(8, 3))
    l20=Label(banner_content, text="⭐ TOP ACADEMIC PERFORMER ⭐",font=("Arial", 18, "bold"), bg="#D4AF37", fg="#8B4513")
    l20.pack(pady=3)
    l21=Label(banner_content, text="═══════════════════════════════════════",font=("Courier", 10, "bold"), bg="#D4AF37", fg="#5E4A3C")
    l21.pack(pady=(3, 8))
    
    # PODIUM STYLE LAYOUT - reduced padding
    podium_container = Frame(content_container, bg="#E6D5C3")
    podium_container.pack(fill=BOTH, expand=True, padx=10)
    podium = Frame(podium_container, bg="white", relief="raised", borderwidth=4, highlightbackground="#D4AF37", highlightthickness=3)
    podium.pack(fill=BOTH, expand=True)
    stripe_container = Frame(podium, bg="#AA6005", height=20)
    stripe_container.pack(fill=X)
    stripe_container.pack_propagate(False)
    colors = ["#FFD700", "#C0C0C0", "#FFD700", "#C0C0C0", "#FFD700"]
    for i, color in enumerate(colors):
        Frame(stripe_container, bg=color, width=200).pack(side=LEFT, fill=Y, expand=True)
    podium_content = Frame(podium, bg="white")
    podium_content.pack(fill=BOTH, expand=True, padx=60, pady=8)
    
    # Medal section - smaller medals
    medal_section = Frame(podium_content, bg="white")
    medal_section.pack(pady=(2, 5))
    medals_frame = Frame(medal_section, bg="white")
    medals_frame.pack()
    l22=Label(medals_frame, text="🥈", font=("Arial", 22), bg="white")
    l22.pack(side=LEFT, padx=5)
    center_medal = Frame(medals_frame, bg="#FFD700", relief="raised",borderwidth=2, highlightbackground="#FFA000", highlightthickness=2)
    center_medal.pack(side=LEFT, padx=8)
    l23=Label(center_medal, text="🥇", font=("Arial", 38), bg="#FFD700",padx=10, pady=8)
    l23.pack()
    l24=Label(medals_frame, text="🥉", font=("Arial", 22), bg="white")
    l24.pack(side=LEFT, padx=5)
    
    # Rank badge - smaller
    rank_badge = Frame(podium_content, bg="#8B4513", relief="raised", borderwidth=2)
    rank_badge.pack(pady=6)
    l25=Label(rank_badge, text="RANK #1", font=("Arial", 12, "bold"),bg="#8B4513", fg="#FFD700", padx=20, pady=4)
    l25.pack()
    
    # Student name with decorative elements - reduced spacing
    name_section = Frame(podium_content, bg="white")
    name_section.pack(pady=8)
    l26=Label(name_section, text="━━━━━━━━", font=("Arial", 10),bg="white", fg="#D4AF37")
    l26.pack()
    l27=Label(name_section, text=student_name[index],font=("Georgia", 20, "bold"), bg="white", fg="#5E4A3C")
    l27.pack(pady=5)
    l28=Label(name_section, text="━━━━━━━━", font=("Arial", 10),bg="white", fg="#D4AF37")
    l28.pack()
    ribbon = Frame(podium_content, bg="#5E4A3C", relief="raised", borderwidth=2)
    ribbon.pack(pady=6)
    l29=Label(ribbon, text=f"ID: {student_code[index]}",font=("Arial", 11, "bold"), bg="#5E4A3C", fg="white",padx=25, pady=5)
    l29.pack()
    
    # Score showcase grid - more compact
    scores_grid = Frame(podium_content, bg="white")
    scores_grid.pack(pady=10, fill=X, padx=20)
    
    # Right column 
    right_col = Frame(scores_grid, bg="white")
    right_col.pack(fill=BOTH, expand=True, padx=10)
    perc_box = Frame(right_col, bg="#E8F5E9", relief="ridge", borderwidth=3,highlightbackground="#4CAF50", highlightthickness=2)
    perc_box.pack(fill=BOTH, expand=True)
    l30=Label(perc_box, text="OVERALL", font=("Arial", 10, "bold"),bg="#E8F5E9", fg="#2E7D32")
    l30.pack(pady=(8, 2))
    l31=Label(perc_box, text=f"{overall_percentage[index]}%",font=("Arial", 32, "bold"), bg="#E8F5E9", fg="#4CAF50")
    l31.pack(pady=3)

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
    detail_frame = Frame(content_area, bg="#E6D5C3")
    detail_frame.pack(fill=BOTH, expand=True)
    bg_image = Image.open(r"C:\Users\User\Documents\CYBER Y2\Semester 3\Code Lab II\skills-portfolio-Falak-17\Assessment 1 - Skills Portfolio\03 Student Manager\Images\image 1.jpg")
    bg_image = bg_image.resize((1400, 800))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(detail_frame, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Content container
    content_container = Frame(detail_frame, bg="#E6D5C3")
    content_container.pack(fill=BOTH, expand=True, padx=30, pady=15)
    
    # Back button
    LowScore_back_btn = Button(content_container, text="← Back", font=("Arial", 10, "bold"),bg="#5E4A3C", fg="white", command=show_dashboard,padx=15, pady=6, bd=0, cursor="hand2",relief="raised", borderwidth=3)
    LowScore_back_btn.pack(anchor=W, pady=(0, 10))
    
    # Top warning banner
    banner = Frame(content_container, bg="#8B4513", relief="raised",borderwidth=4, highlightbackground="#5E4A3C", highlightthickness=2)
    banner.pack(fill=X, padx=10, pady=(0, 12))
    banner_content = Frame(banner, bg="#FFCDD2")
    banner_content.pack(fill=BOTH, expand=True, padx=6, pady=6)
    l32=Label(banner_content, text="═══════════════════════════════════════",font=("Courier", 10, "bold"), bg="#FFCDD2", fg="#D32F2F")
    l32.pack(pady=(8, 3))
    l33=Label(banner_content, text="⚠️ NEEDS ACADEMIC SUPPORT ⚠️",font=("Arial", 18, "bold"), bg="#FFCDD2", fg="#D32F2F")
    l33.pack(pady=3)
    l34=Label(banner_content, text="═══════════════════════════════════════",font=("Courier", 10, "bold"), bg="#FFCDD2", fg="#D32F2F")
    l34.pack(pady=(3, 8))
    
    # Main card container
    card_container = Frame(content_container, bg="#E6D5C3")
    card_container.pack(fill=BOTH, expand=True, padx=10)
    card = Frame(card_container, bg="white", relief="raised", borderwidth=3,highlightbackground="#E57373", highlightthickness=2)
    card.pack(fill=BOTH, expand=True)
    
    # Red warning stripe
    stripe_container = Frame(card, bg="#D32F2F", height=15)
    stripe_container.pack(fill=X)
    stripe_container.pack_propagate(False)
    colors = ["#FFCDD2", "#EF5350", "#FFCDD2", "#EF5350", "#FFCDD2"]
    for i, color in enumerate(colors):
        Frame(stripe_container, bg=color, width=200).pack(side=LEFT, fill=Y, expand=True)
    
    card_content = Frame(card, bg="white")
    card_content.pack(fill=BOTH, expand=True, padx=40, pady=5)
    icon_section = Frame(card_content, bg="white")
    icon_section.pack(pady=(1, 3))
    l35=Label(icon_section, text="⚠️", font=("Arial", 40), bg="white")
    l35.pack()
    
    # Alert badge
    alert_badge = Frame(card_content, bg="#D32F2F", relief="raised", borderwidth=2)
    alert_badge.pack(pady=4)
    l36=Label(alert_badge, text="LOWEST SCORE", font=("Arial", 11, "bold"),bg="#D32F2F", fg="white", padx=18, pady=3)
    l36.pack()
    
    # Student name section
    name_section = Frame(card_content, bg="white")
    name_section.pack(pady=5)
    l37=Label(name_section, text="━━━━━━━━", font=("Arial", 9),bg="white", fg="#E57373")
    l37.pack()
    l38=Label(name_section, text=student_name[index],font=("Georgia", 18, "bold"), bg="white", fg="#5E4A3C")
    l38.pack(pady=4)
    l39=Label(name_section, text="━━━━━━━━", font=("Arial", 9),bg="white", fg="#E57373")
    l39.pack()
    
    # ID ribbon
    ribbon = Frame(card_content, bg="#5E4A3C", relief="raised", borderwidth=2)
    ribbon.pack(pady=4)
    l40=Label(ribbon, text=f"ID: {student_code[index]}",font=("Arial", 10, "bold"), bg="#5E4A3C", fg="white",padx=20, pady=4)
    l40.pack()
    
    # Score display
    scores_grid = Frame(card_content, bg="white")
    scores_grid.pack(pady=6, fill=X, padx=15)
    score_col = Frame(scores_grid, bg="white")
    score_col.pack(fill=BOTH, expand=True, padx=8)
    perc_box = Frame(score_col, bg="#FFEBEE", relief="ridge", borderwidth=3,highlightbackground="#E57373", highlightthickness=2)
    perc_box.pack(fill=BOTH, expand=True)
    l41=Label(perc_box, text="OVERALL", font=("Arial", 9, "bold"),bg="#FFEBEE", fg="#D32F2F")
    l41.pack(pady=(6, 1))
    l42=Label(perc_box, text=f"{overall_percentage[index]}%",font=("Arial", 28, "bold"), bg="#FFEBEE", fg="#E57373")
    l42.pack(pady=2)
    
    # Grade display
    grade_display = Frame(perc_box, bg="#E57373", relief="raised", borderwidth=2)
    grade_display.pack(pady=(4, 6), padx=10)
    l43=Label(grade_display, text=f"⚠️ GRADE {student_grade[index]} ⚠️",font=("Arial", 12, "bold"), bg="#E57373", fg="white",padx=12, pady=5)
    l43.pack()
    
    # Bottom support message
    support = Frame(card_content, bg="#D32F2F", relief="raised", borderwidth=2,highlightbackground="#E57373", highlightthickness=1)
    support.pack(pady=(4, 3))
    support_inner = Frame(support, bg="#FFCDD2")
    support_inner.pack(padx=2, pady=2)
    warning=Label(support_inner, text="◆ REQUIRES INTERVENTION ◆",font=("Arial", 9, "bold"), bg="#FFCDD2", fg="#D32F2F",padx=15, pady=5)
    warning.pack()

# Main container
main_container = Frame(root, bg="#f5f5f5")
main_container.pack(fill=BOTH, expand=True)

# Sidebar 
sidebar_frame = Frame(main_container, bg="#f8f9fa", width=230, highlightbackground="#e0e0e0", highlightthickness=1)
sidebar_frame.pack(side=LEFT, fill=Y)
sidebar_frame.pack_propagate(False)
sidebar_header = Frame(sidebar_frame, bg="#5E4A3C", height=140)
sidebar_header.pack(fill=X)
sidebar_header.pack_propagate(False)
profile_section = Frame(sidebar_header, bg="#5E4A3C")
profile_section.pack(expand=True, pady=20)
l1=Label(profile_section, text="👤", font=("Arial", 40), bg="#5E4A3C", fg="white")
l1.pack()
l2=Label(profile_section, text="Admin User", font=("Arial", 13, "bold"),bg="#5E4A3C", fg="#FFFFFF")
l2.pack(pady=(5, 2))
sidebar_menu = Frame(sidebar_frame, bg="#f8f9fa")
sidebar_menu.pack(fill=BOTH, expand=True, pady=20)

# Menu items with proper button creation
def create_menu_button(parent, icon, text, command):
    btn = Button(parent, text=f"{icon}  {text}", font=("Arial", 11),bg="#5E4A3C", fg="#FFFFFF", bd=0, anchor=W, padx=20, pady=12,activebackground="#E1BEE7", cursor="hand2", command=command)
    btn.pack(fill=X, padx=10, pady=3)
    
    def on_enter(e):
        btn.configure(bg="#3A2A1E")
    def on_leave(e):
        btn.configure(bg="#5E4A3C")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

create_menu_button(sidebar_menu, "🏠", "Dashboard", show_dashboard)
create_menu_button(sidebar_menu, "📋", "View All Records", view_all_records)
create_menu_button(sidebar_menu, "🔍", "View Individual Record", view_individual_record)
create_menu_button(sidebar_menu, "🏆", "Highest Score", show_highest_score)
create_menu_button(sidebar_menu, "📉", "Lowest Score", show_lowest_score)

# Sidebar footer
sidebar=Frame(sidebar_frame, bg="#e0e0e0", height=1)
sidebar.pack(fill=X, side=BOTTOM, pady=(10, 0))
sidebar_footer = Frame(sidebar_frame, bg="#f8f9fa")
sidebar_footer.pack(side=BOTTOM, fill=X, pady=15)
footer=Label(sidebar_footer, text="admin@gmail.com", font=("Arial", 9),bg="#f8f9fa", fg="#999")
footer.pack(pady=5)
content_area = Frame(main_container, bg="#f5f5f5")
content_area.pack(side=RIGHT, fill=BOTH, expand=True)

# Load data and show dashboard
root.after(100, load_data)
root.after(150, show_dashboard)
root.mainloop()