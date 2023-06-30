from win10toast_click import ToastNotifier
from datetime import datetime, timedelta
import sqlite3
import time
import os

pid = 0
running = True

def notif(msg):
    toaster = ToastNotifier()  # initialize
    toaster.show_toast(
        "To-Do List",  # title
        msg,  # message
        icon_path='C:/Users/justi/OneDrive - student.newinti.edu.my/ALL PROJECT/tdl.png',  # 'icon_path'
        duration=5,  # for how many seconds toast should be visible; None = leave notification in Notification Center
    )

def notif_loop():
    global pid
    pid = os.getpid()
    global running
    while running:
        connection = sqlite3.connect('todolist.db')
        cursor = connection.cursor()

        cursor.execute("SELECT Due_Date, Due_Time, Difficulty, Task_Name, Completed, Saved_username,Task_ID FROM Tasks")
        task_data = cursor.fetchall()
        current_datetime = datetime.now()

        for task in task_data:
            due_date = task[0]
            due_time = task[1]
            difficulty = task[2]
            task_name = task[3]
            status = task[4]
            User = str(task[5])
            task_id = task[6]
            due_datetime = datetime.strptime(due_date + " " + due_time, "%Y-%m-%d %H:%M")
            time_difference = due_datetime - current_datetime
            difference_in_seconds = time_difference.total_seconds()
            if status == 0:
                if difficulty == "Hard":
                    if difference_in_seconds <= 7200 and difference_in_seconds >= 7199:
                        msg = User + "\n" + task_name + ": " + "2 hours remaining"
                        notif(msg)
                else:
                    if difference_in_seconds <= 3600 and difference_in_seconds >= 3599:
                        msg = User + "\n" + task_name + ": " + "1 hour remaining"
                        notif(msg)

        time.sleep(1)

    notif_loop()
