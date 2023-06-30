from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from tkinter.ttk import Combobox
import sqlite3
import Priority as pr
import os
import signal
from Login import CurrentUser

connection = sqlite3.connect('todolist.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Tasks(Task_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Task_Name VARCHAR NOT NULL, Due_Date VARCHAR NOT NULL, Due_Time VARCHAR NOT NULL, Difficulty CHAR NOT NULL, Priority INT NOT NULL, Completed INT NOT NULL)')
connection.commit()
cursor.execute("PRAGMA table_info(Tasks)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]
if "Saved_username" not in column_names:
    alter_table_sql = '''
        ALTER TABLE Tasks
        ADD COLUMN Saved_username TEXT REFERENCES login_info(Saved_username)
    '''
    cursor.execute(alter_table_sql)
    connection.commit()
def CRUD_display():

    def add_task():
        task_name = task_name_entry.get()
        due_date = due_date_spinbox.get()
        due_time = f"{hour_combobox.get()}:{minute_combobox.get()} {ampm_combobox.get()}"
        due_time_24h = ""
        if hour_combobox.get() and minute_combobox.get() and ampm_combobox.get():
            due_time_24h = datetime.strptime(due_time, "%I:%M %p").strftime("%H:%M")
        difficulty = difficulty_combobox.get()
        priority = 1
        completed = 0
        if task_name and due_date and due_time_24h:
            current_datetime = datetime.now()
            due_datetime = datetime.strptime(f"{due_date} {due_time}", "%Y-%m-%d %I:%M %p")
            if due_datetime > current_datetime:
                data_insert_query = '''INSERT INTO Tasks (Task_Name, Due_Date, Due_Time, Difficulty, Priority, Completed,Saved_username) VALUES(?,?,?,?,?,?,?)'''
                data_insert_tuple = (task_name, due_date, due_time_24h, difficulty, priority, completed, CurrentUser)
                cursor.execute(data_insert_query, data_insert_tuple)
                connection.commit()
                task_name_entry.delete(0, tk.END)
                due_date_spinbox.delete(0, tk.END)
                hour_combobox.delete(0, tk.END)
                minute_combobox.delete(0, tk.END)
                refresh_task_list()
            else:
                cruderror.config(text="Error: Due date and time must be in the future",foreground="red")
        else:
            cruderror.config(text="Error: Task name, due date, and due time cannot be empty",foreground="red")

    def edit_task():
        selected_task = task_treeview.focus()
        if selected_task:
            task_data = task_treeview.item(selected_task)
            task_name = task_data['values'][0]
            due_date = task_data['values'][1]
            due_time = task_data['values'][2]
            hour, minute, am_pm = due_time.split(":")[0], due_time.split(":")[1].split()[0], due_time.split(":")[1].split()[1]
            difficulty = task_data['values'][3]

            task_name_entry.delete(0, tk.END)
            task_name_entry.insert(0, task_name)
            due_date_spinbox.delete(0, tk.END)
            due_date_spinbox.insert(0, due_date)
            hour_combobox.set(hour)
            minute_combobox.set(minute)
            ampm_combobox.set(am_pm)
            difficulty_combobox.set(difficulty)
        
            update_button.config(state=tk.NORMAL)
        else:
            cruderror.config(text="Error: Please select a task to edit")


    def update_task():
        selected_task = task_treeview.focus()
        if selected_task:
            task_data = task_treeview.item(selected_task)
            task_id = task_data['text']
            task_name = task_name_entry.get()
            due_date = due_date_spinbox.get()
            due_time = f"{hour_combobox.get()}:{minute_combobox.get()} {ampm_combobox.get()}"
            due_time_24h = ""
            if hour_combobox.get() and minute_combobox.get() and ampm_combobox.get():
                due_time_24h = datetime.strptime(due_time, "%I:%M %p").strftime("%H:%M")
            difficulty = difficulty_combobox.get()
            if task_name and due_date and due_time_24h and difficulty:
                current_datetime = datetime.now()
                due_datetime = datetime.strptime(f"{due_date} {due_time}", "%Y-%m-%d %I:%M %p")
                if due_datetime > current_datetime:
                    update_query = '''UPDATE Tasks SET Task_Name=?, Due_Date=?, Due_Time=?, Difficulty=? WHERE Task_ID=?'''
                    update_tuple = (task_name, due_date, due_time_24h, difficulty, task_id)
                    cursor.execute(update_query, update_tuple)
                    connection.commit()
                    task_name_entry.delete(0, tk.END)
                    due_date_spinbox.delete(0, tk.END)
                    hour_combobox.delete(0, tk.END)
                    minute_combobox.delete(0, tk.END)
                    difficulty_combobox.delete(0, tk.END)
                    refresh_task_list()
                    update_button.config(state=tk.DISABLED)
                else:
                    cruderror.config(text="Error: Due date and time must be in the future",foreground="red")
            else:
                cruderror.config(text="Error: Task name, due date, and due time cannot be empty",foreground="red")
        else:
            cruderror.config(text="Error: Please select a task to update",foreground="red")


    def delete_task():
        selected_task = task_treeview.focus()
        if selected_task:
            task_id = task_treeview.item(selected_task)['text']
            delete_query = '''DELETE FROM Tasks WHERE Task_ID=?'''
            delete_tuple = (task_id,)
            cursor.execute(delete_query, delete_tuple)
            connection.commit()
            refresh_task_list()
        else:
            cruderror.config(text="Error: Please select a task to delete",foreground="red")

    def mark_as_completed():
        selected_task = task_treeview.focus()
        if selected_task:
            task_id = task_treeview.item(selected_task)['text']
            update_query = '''UPDATE Tasks SET Completed=1,Priority=0 WHERE Task_ID=?'''
            update_tuple = (task_id,)
            cursor.execute(update_query, update_tuple)
            connection.commit()
            refresh_task_list()
        else:
            cruderror.config(text="Error: Please select a task")

    def refresh_task_list():
        pr.priority_update(CurrentUser)
        task_treeview.delete(*task_treeview.get_children())
        refresh_query = "SELECT Task_ID, Task_Name, Due_Date, Due_Time, Difficulty, Priority, Completed FROM Tasks WHERE Saved_username=?"
        cursor.execute(refresh_query, (CurrentUser,))
        tasks = cursor.fetchall()
        for task in tasks:
            task_id = task[0]
            task_name = task[1]
            due_date = task[2]
            due_time = task[3]
            difficulty = task[4]
            priority = task[5]
            completed = task[6]

            time_obj = datetime.strptime(due_time, "%H:%M")
            formatted_time = time_obj.strftime("%I:%M %p")

            completion_status = get_completion_status(completed)

            task_treeview.insert("", "end", text=task_id, values=(task_name, due_date, formatted_time, difficulty, priority, completion_status), tags=(completion_status,))

        task_treeview.tag_configure("Completed", background="green")
        task_treeview.tag_configure("Pending", background="orange")
    
    
    def get_completion_status(completed):
        return "Completed" if completed else "Pending"

    def sortFunction(event=None):
        selected_sort = sort_dropdown.get()
        if selected_sort == "A-Z":
            sort_AZ(reverse=False)
        elif selected_sort == "Z-A":
            sort_AZ(reverse=True)
        elif selected_sort == "Due Date and Time":
            sorting_DT()
        elif selected_sort == "Priority":
            sorting_P()

    def sort_AZ(reverse=False):
        task_treeview.delete(*task_treeview.get_children())
        query_sort_AZ="SELECT Task_ID, Task_Name, Due_Date, Due_Time, Difficulty, Priority, Completed FROM Tasks WHERE Saved_username=? ORDER BY Task_Name COLLATE NOCASE" + (" DESC" if reverse else "")
        cursor.execute(query_sort_AZ,(CurrentUser,))
        tasks = cursor.fetchall()
        for task in tasks:
            task_id = task[0]
            task_name = task[1]
            due_date = task[2]
            due_time = task[3]
            difficulty = task[4]
            priority = task[5]
            completed = task[6]

            time_obj = datetime.strptime(due_time, "%H:%M")
            formatted_time = time_obj.strftime("%I:%M %p")

            completion_status = get_completion_status(completed)

            task_treeview.insert("", "end", text=task_id, values=(task_name, due_date, formatted_time, difficulty, priority, completion_status), tags=(completion_status,))

        task_treeview.tag_configure("Completed", background="green")
        task_treeview.tag_configure("Pending", background="orange")


    def sorting_DT():
        task_treeview.delete(*task_treeview.get_children())
        query_sorting_DT='SELECT Task_ID, Task_Name,Due_Date,Due_Time, Difficulty, Priority, Completed,date(Due_Date) as DueDate,time(Due_Time) as DueTime FROM Tasks WHERE Saved_username=? ORDER BY DueDate ASC, DueTime ASC'
        cursor.execute(query_sorting_DT,(CurrentUser,))
        tasks = cursor.fetchall()
        for task in tasks:
            task_id = task[0]
            task_name = task[1]
            due_date = task[2]
            due_time = task[3]
            difficulty = task[4]
            priority = task[5]
            completed = task[6]

            time_obj = datetime.strptime(due_time, "%H:%M")
            formatted_time = time_obj.strftime("%I:%M %p")

            completion_status = get_completion_status(completed)

            task_treeview.insert("", "end", text=task_id, values=(task_name, due_date, formatted_time, difficulty, priority, completion_status), tags=(completion_status,))

        task_treeview.tag_configure("Completed", background="green")
        task_treeview.tag_configure("Pending", background="orange")

    def sorting_P():
        task_treeview.delete(*task_treeview.get_children())
        query_sorting_P='SELECT Task_ID, Task_Name,Due_Date,Due_Time, Difficulty, Priority, Completed FROM Tasks WHERE Saved_username=? ORDER BY Priority ASC'
        cursor.execute(query_sorting_P,(CurrentUser,))
        tasks = cursor.fetchall()
        for task in tasks:
            task_id = task[0]
            task_name = task[1]
            due_date = task[2]
            due_time = task[3]
            difficulty = task[4]
            priority = task[5]
            completed = task[6]

            time_obj = datetime.strptime(due_time, "%H:%M")
            formatted_time = time_obj.strftime("%I:%M %p")

            completion_status = get_completion_status(completed)

            task_treeview.insert("", "end", text=task_id, values=(task_name, due_date, formatted_time, difficulty, priority, completion_status), tags=(completion_status,))

        task_treeview.tag_configure("Completed", background="green")
        task_treeview.tag_configure("Pending", background="orange")

    root = tk.Tk()
    import pushnotif as notif
    def stop_background_notification():
        os.kill(notif.pid, signal.SIGTERM)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW",stop_background_notification)


    root.title("Task Manager")
    root.geometry("750x400")

    task_name_label = tk.Label(root, text="Task Name:")
    task_name_label.place(x=10, y=10)
    task_name_entry = tk.Entry(root, width=80)
    task_name_entry.place(x=100, y=10)

    due_date_label = tk.Label(root, text="Due Date:")
    due_date_label.place(x=10, y=40)
    due_date_spinbox = DateEntry(root, width=12, date_pattern="yyyy-mm-dd", show=None)
    due_date_spinbox.place(x=100, y=40)

    due_time_label = tk.Label(root, text="Due Time:")
    due_time_label.place(x=250, y=40)

    difficulty_label = tk.Label(root, text="Difficulty:")
    difficulty_label.place(x=470, y=40)
    difficulty_combobox = Combobox(root, values=["Easy", "Hard"], width=8, state="readonly")
    difficulty_combobox.place(x=530, y=40)

    hour_combobox = Combobox(root, values=list(range(1, 13)), width=3, state="readonly")
    hour_combobox.place(x=330, y=40)

    minute_combobox = Combobox(root, values=list(range(60)), width=3, state="readonly")
    minute_combobox.place(x=370, y=40)

    ampm_combobox = Combobox(root, values=["AM", "PM"], width=3, state="readonly")
    ampm_combobox.place(x=410, y=40)

    add_task_button = tk.Button(root, text="Add Task", command=add_task)
    add_task_button.place(x=10, y=70)

    edit_task_button = tk.Button(root, text="Edit Task", command=edit_task)
    edit_task_button.place(x=100, y=70)

    update_button = tk.Button(root, text="Update Task", command=update_task, state=tk.DISABLED)
    update_button.place(x=190, y=70)

    delete_task_button = tk.Button(root, text="Delete Task", command=delete_task)
    delete_task_button.place(x=280, y=70)

    mark_completed_button = tk.Button(root, text="Mark Completed", command=mark_as_completed)
    mark_completed_button.place(x=370, y=70)

    sort_dropdown = Combobox(root, width=10, state="readonly")
    sort_dropdown['values'] = ("A-Z", "Z-A", "Date-Time", "Priority")
    sort_dropdown.place(x=530, y=70)

    sort_dropdown.current()
    sort_dropdown.bind("<<ComboboxSelected>>", sortFunction)

    sort_label = tk.Label(root, text="Sort")
    sort_label.place(x=500, y=70)

    cruderror = tk.Label(root, text="")
    cruderror.place(x=10, y=110)

    task_treeview = ttk.Treeview(root, columns=("Task Name", "Due Date", "Due Time", "Difficulty", "Priority", "Status"), show="headings")
    task_treeview.heading("Task Name", text="Task Name")
    task_treeview.heading("Due Date", text="Due Date")
    task_treeview.heading("Due Time", text="Due Time")
    task_treeview.heading("Difficulty", text="Difficulty")
    task_treeview.heading("Priority", text="Priority")
    task_treeview.heading("Status", text="Status")
    task_treeview.column("Task Name", width=200, anchor="center")
    task_treeview.column("Due Date", width=100, anchor="center")
    task_treeview.column("Due Time", width=100, anchor="center")
    task_treeview.column("Difficulty", width=100, anchor="center")
    task_treeview.column("Priority", width=100, anchor="center")
    task_treeview.column("Status", width=100, anchor="center")
    task_treeview.place(x=10, y=130)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=task_treeview.yview)
    scrollbar.place(x=710, y=130, height=230)
    task_treeview.configure(yscrollcommand=scrollbar.set)

    refresh_task_list()