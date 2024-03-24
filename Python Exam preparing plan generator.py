import datetime
import calendar
import tkinter as tk
from tkinter import ttk, messagebox

# Dictionary containing universities and their SAT score ranges
universities_scores = {
    "Harvard University": (1480, 1580),
    "Massachusetts Institute of Technology": (1500, 1570),
    "Stanford University": (1440, 1570),
    "University of California--Berkeley": (1330, 1530),
    "University of Chicago": (1510, 1570),
    "University of Pennsylvania": (1470, 1570),
    "California Institute of Technology": (1530, 1580),
    "Columbia University": (1460, 1570),
    "Yale University": (1460, 1570),
    "Princeton University": (1460, 1570),
    "University of Michigan--Ann Arbor": (1340, 1530),
    "University of California--Los Angeles": (1290, 1510),
    "University of Virginia": (1330, 1500),
    "University of North Carolina--Chapel Hill": (1270, 1480),
    "Duke University": (1450, 1570),
    "University of California--San Diego": (1300, 1510),
    "Northwestern University": (1450, 1550),
    "Cornell University": (1420, 1550),
    "Johns Hopkins University": (1450, 1550),
    "New York University": (1340, 1510)
}

def generate_study_plan(hours_per_day, target_score, proficiency_levels, exam_date):
    # Define study schedule
    study_schedule = {
        'Math': 5,
        'Reading': 4,
        'Writing & Language': 4
    }
    
    # Calculate total study hours needed
    total_hours_needed = target_score * 2
    
    # Calculate total days needed
    total_days_needed = total_hours_needed / hours_per_day
    
    # Calculate start date
    start_date = datetime.date.today()
    
    # Generate study plan
    current_date = start_date
    study_plan = []
    while total_days_needed > 0:
        for subject, hours in study_schedule.items():
            proficiency_factor = proficiency_levels[subject] / 5  # Assuming proficiency level ranges from 1 to 5
            study_hours = int(hours * proficiency_factor)
            study_plan.append((current_date, subject, study_hours))
            total_days_needed -= 1
            if total_days_needed <= 0:
                break
        current_date += datetime.timedelta(days=1)
    
    # Add exam date to the study plan
    study_plan.append((exam_date, "SAT Exam", 0))
    
    return study_plan

def print_calendar(year, month, study_plan):
    cal_str = ""
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        for day in week:
            if day == 0:
                cal_str += "   "
            else:
                study_day = datetime.date(year, month, day)
                if study_day in [item[0] for item in study_plan]:
                    cal_str += f"{day:2}* "
                else:
                    cal_str += f"{day:2}  "
        cal_str += "\n"
    return cal_str

def suggest_universities(target_score):
    suggestions = []
    for university, scores in universities_scores.items():
        if scores[0] <= target_score <= scores[1]:
            suggestions.append(university)
    return suggestions

def submit():
    try:
        # Retrieve input values
        hours = int(hours_per_day.get())
        score = int(target_score.get())
        math_proficiency = int(math_prof.get())
        reading_proficiency = int(reading_prof.get())
        writing_proficiency = int(writing.get())
        
        # Generate study plan
        study_plan = generate_study_plan(hours, score, {'Math': math_proficiency, 'Reading': reading_proficiency, 'Writing & Language': writing_proficiency}, datetime.date.today() + datetime.timedelta(days=30))
        study_plan_str = "Study Plan:\n------------\n"
        for date, subject, hours in study_plan[:-1]:
            study_plan_str += f"{date}: {subject} - {hours} hours\n"
        study_plan_str += f"\nYour SAT exam is scheduled for: {datetime.date.today() + datetime.timedelta(days=30)}"
        
        # Display study plan
        plan_text.config(state='normal')
        plan_text.delete(1.0, tk.END)
        plan_text.insert(tk.END, study_plan_str)
        plan_text.config(state='disabled')
        
        # Generate university suggestions
        uni_suggestions = suggest_universities(score)
        suggestion_str = "University Suggestions:\n------------------------\n"
        if uni_suggestions:
            suggestion_str += "\n".join(uni_suggestions)
        else:
            suggestion_str += "No universities found within the specified score range."
        
        # Display university suggestions
        suggestion_text.config(state='normal')
        suggestion_text.delete(1.0, tk.END)
        suggestion_text.insert(tk.END, suggestion_str)
        suggestion_text.config(state='disabled')
        
        # Generate and display calendar
        calendar_str = print_calendar(datetime.date.today().year, datetime.date.today().month, study_plan)
        calendar_text.config(state='normal')
        calendar_text.delete(1.0, tk.END)
        calendar_text.insert(tk.END, calendar_str)
        calendar_text.config(state='disabled')
        
    except ValueError:
        messagebox.showerror("Error", "Please select all options.")

root = tk.Tk()
root.title("SAT Preparation Program")
root.geometry("800x600")

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Create frame for input fields
input_frame = ttk.Frame(main_frame, padding=10, relief="raised")
input_frame.pack(side='left', padx=20, pady=10, fill='both', expand=True)

# Create time selection buttons
time_label = ttk.Label(input_frame, text="Select Time (hours/day):")
time_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
time_buttons = ttk.Frame(input_frame, padding=15)
time_buttons.grid(row=1, column=0, padx=5, pady=5, sticky='w')
hours_per_day = tk.StringVar()
for i in range(1, 6):
    btn = ttk.Button(time_buttons, text=str(i), width=4, command=lambda value=i: hours_per_day.set(value))
    btn.grid(row=0, column=i, padx=5, pady=5)

# Create target score selection buttons
score_label = ttk.Label(input_frame, text="Select Target Score:")
score_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
score_buttons = ttk.Frame(input_frame, padding=10)
score_buttons.grid(row=3, column=0, padx=5, pady=5, sticky='w')
target_score = tk.StringVar()
for i in range(1200, 1610, 50):
    btn = ttk.Button(score_buttons, text=str(i), width=4, command=lambda value=i: target_score.set(value))
    btn.grid(row=0, column=(i - 1200) // 50, padx=5, pady=5)

# Create proficiency level selection buttons
prof_label = ttk.Label(input_frame, text="Select Proficiency Levels:")
prof_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
prof_buttons = ttk.Frame(input_frame, padding=10)
prof_buttons.grid(row=5, column=0, padx=5, pady=5, sticky='w')
math_prof = tk.IntVar()
reading_prof = tk.IntVar()
writing = tk.IntVar()
prof_vars = [math_prof, reading_prof, writing]
prof_labels = ["Math", "Reading", "Writing"]
for i, prof in enumerate(prof_labels):
    ttk.Label(prof_buttons, text=prof).grid(row=i, column=0, padx=5, pady=5, sticky='w')
    for j in range(1, 6):
        btn = ttk.Button(prof_buttons, text=str(j), width=4, command=lambda value=j, var=prof_vars[i]: var.set(value))
        btn.grid(row=i, column=j, padx=5, pady=5)

# Create submit button
submit_button = ttk.Button(input_frame, text="Submit", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, pady=10)

# Create frame for study plan and suggestion
study_suggestion_frame = ttk.Frame(main_frame, padding=10, relief="raised")
study_suggestion_frame.pack(side='left', padx=20, pady=10, fill='both', expand=True)

# Create study plan text box
plan_label = ttk.Label(study_suggestion_frame, text="Study Plan")
plan_label.pack(pady=5)
plan_text = tk.Text(study_suggestion_frame, height=10, width=50)
plan_text.pack(pady=5)
plan_text.config(state='disabled')  # Disable editing

# Create suggestion text box
suggestion_label = ttk.Label(study_suggestion_frame, text="University Suggestions")
suggestion_label.pack(pady=5)
suggestion_text = tk.Text(study_suggestion_frame, height=10, width=50)
suggestion_text.pack(pady=5)
suggestion_text.config(state='disabled')  # Disable editing

# Create calendar frame
calendar_frame = ttk.Frame(root, padding=10, relief="raised")
calendar_frame.pack(side='left', padx=20, pady=10, fill='both', expand=True)

# Create calendar label
calendar_label = ttk.Label(calendar_frame, text="Study Plan Calendar")
calendar_label.pack(pady=5)

# Create calendar text box with scroll
calendar_text = tk.Text(calendar_frame, height=20, width=30)
calendar_text.pack(pady=5)
calendar_text.config(state='disabled')  # Disable editing
scroll = ttk.Scrollbar(calendar_frame, orient="vertical", command=calendar_text.yview)
scroll.pack(side='right', fill='y')
calendar_text.config(yscrollcommand=scroll.set)

root.mainloop()

