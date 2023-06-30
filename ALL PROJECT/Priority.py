from datetime import datetime, timedelta
import sqlite3

def priority_update(CurrentUser):
    connection = sqlite3.connect('todolist.db')
    cursor = connection.cursor()

    list_diff_sec = []
    query_dddt="SELECT Due_Date, Due_Time FROM Tasks WHERE Saved_username=? AND NOT Priority=0"
    cursor.execute(query_dddt,(CurrentUser,))
    task_data = cursor.fetchall()
    current_datetime = datetime.now()

    for task in task_data:
        due_date = task[0]
        due_time = task[1]
        due_datetime = datetime.strptime(due_date + " " + due_time, "%Y-%m-%d %H:%M")
        time_difference = due_datetime - current_datetime
        difference_in_seconds = time_difference.total_seconds()
        list_diff_sec.append(difference_in_seconds)
    
    rankorder = sorted(range(len(list_diff_sec)), key=list_diff_sec.__getitem__)
    rankorder_1 = [1 + x for x in rankorder]
    n = 0
    query_Task_ID="SELECT Task_ID FROM Tasks WHERE Saved_username=? AND NOT Priority=0"
    cursor.execute(query_Task_ID,(CurrentUser,))
    Task_ID_list = cursor.fetchall()

    for i in rankorder_1:
        r_order_query = '''UPDATE Tasks SET priority = ? WHERE Task_ID = ?'''
        til = Task_ID_list[n][0]  # Retrieve Task_ID value from the tuple
        r_order_tuple = (i, til)
        n += 1
        cursor.execute(r_order_query, r_order_tuple)

    connection.commit()