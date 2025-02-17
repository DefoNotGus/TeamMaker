import json
import random
import tkinter as tk
from tkinter import messagebox

# Load students from JSON file
def load_students():
    try:
        with open("students.json", "r") as file:
            data = json.load(file)
            return data.get("students", [])
    except FileNotFoundError:
        messagebox.showerror("Error", "students.json not found!")
        return []

def create_groups(students, min_size=3, max_size=4):
    random.shuffle(students)
    groups = []
    
    while len(students) >= min_size:
        if len(students) <= max_size:
            groups.append(students[:])
            students = []
        else:
            groups.append(students[:max_size])
            students = students[max_size:]
    
    rest = students if students else []
    
    return groups, rest

def show_group_screen():
    try:
        min_size = int(min_entry.get())
        max_size = int(max_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for range.")
        return
    
    students = load_students()
    if not students:
        return
    
    groups, rest = create_groups(students, min_size, max_size)
    
    group_window = tk.Toplevel(root)
    group_window.title("Allocated Groups")
    group_window.geometry("500x600")
    
    tk.Label(group_window, text="Allocated Groups", font=("Arial", 16, "bold")).pack(pady=10)
    
    result_frame = tk.Frame(group_window)
    result_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    result_text = tk.Text(result_frame, height=30, width=60, font=("Arial", 12))
    result_text.pack(pady=10, padx=10)
    
    result_text.insert(tk.END, "==============================\n")
    result_text.insert(tk.END, "        Group Allocations        \n")
    result_text.insert(tk.END, "==============================\n\n")
    
    for i, group in enumerate(groups, start=1):
        result_text.insert(tk.END, f"Group {i}:\n")
        result_text.insert(tk.END, "------------------------------\n")
        result_text.insert(tk.END, f"{', '.join(group)}\n\n")
    
    if rest:
        result_text.insert(tk.END, "==============================\n")
        result_text.insert(tk.END, "        Rest Group        \n")
        result_text.insert(tk.END, "==============================\n")
        result_text.insert(tk.END, f"{', '.join(rest)}\n\n")
    
    total_groups = len(groups)
    total_students = sum(len(g) for g in groups) + len(rest)
    
    result_text.insert(tk.END, "==============================\n")
    result_text.insert(tk.END, f"Total Groups: {total_groups}\n")
    result_text.insert(tk.END, f"Total Students: {total_students}\n")
    result_text.insert(tk.END, "==============================\n")
    result_text.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Student Group Allocator")
root.geometry("400x200")

tk.Label(root, text="Random Student Group Allocator", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Group Size Range:").pack()
range_frame = tk.Frame(root)
range_frame.pack()

min_entry = tk.Entry(range_frame, width=5)
min_entry.pack(side=tk.LEFT, padx=5)
min_entry.insert(0, "3")

tk.Label(range_frame, text="to").pack(side=tk.LEFT)

max_entry = tk.Entry(range_frame, width=5)
max_entry.pack(side=tk.LEFT, padx=5)
max_entry.insert(0, "4")

tk.Button(root, text="Generate Groups", font=("Arial", 12), command=show_group_screen).pack(pady=10)

root.mainloop()