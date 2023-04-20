from tkinter import *
from tkinter import ttk
import sqlite3
import datetime

conn = sqlite3.connect('todolist.db') #create database
c= conn.cursor()
table_create_query = '''CREATE TABLE IF NOT EXISTS login_info
        (Saved_username TEXT PRIMARY KEY NOT NULL,Saved_password TEXT NOT NULL)
'''
conn.execute(table_create_query)
conn.close

root= Tk()

def register():
    root.title("Register Page")
    registerframe = ttk.Frame(root,padding="3 3 12 12")
    registerframe.grid(column=0,row=0, sticky=(N,W,E,S))

    register_username = StringVar()
    register_password = StringVar()
    confirm_register_password = StringVar()

    ttk.Label(registerframe, text="Username:").grid(column=1,row=1,sticky=W)
    ttk.Label(registerframe, text="Password:").grid(column=1,row=2,sticky=W)
    ttk.Label(registerframe, text="Confirm Password:").grid(column=1,row=3,sticky=W)
    error=ttk.Label(registerframe, text="")
    error.grid(column=1,row=4,sticky=W,columnspan=20)

    register_username_entry = ttk.Entry(registerframe,width=20,textvariable=register_username)
    register_username_entry.grid(column=2,row=1,sticky=(W,E))

    ONorOFF = IntVar()
    def showpass():
        if(ONorOFF.get()==1):
            register_password_entry.config(show="") 
            register_confirm_register_password.config(show="")
        else:
            register_password_entry.config(show="*") 
            register_confirm_register_password.config(show="*")

    ttk.Checkbutton(registerframe,text='Show password',command=showpass,variable=ONorOFF,onvalue=1, offvalue=0).grid(column=3,row=3,sticky=W)

    register_password_entry = ttk.Entry(registerframe,width=20,textvariable=register_password,show="*")
    register_password_entry.grid(column=2,row=2,sticky=(W,E))

    register_confirm_register_password = ttk.Entry(registerframe,width=20,textvariable=confirm_register_password,show="*")
    register_confirm_register_password.grid(column=2,row=3,sticky=(W,E))

    def confirm_register():
        saving_username= register_username_entry.get()
        saving_password=register_password_entry.get()
        compare_password=register_confirm_register_password.get()
        if not saving_password==compare_password:
            error.config(text="Error: Password does not match")
        else:
            c.execute("SELECT COUNT(*) from login_info WHERE Saved_username='"+saving_username+"'")
            result= c.fetchone()
            if int(result[0]) > 0:
                error.config(text="Error: This Username already exist.\nPlease enter another one.")
            else:    
                error.config(text="New user added.")
                data_insert_query='''INSERT INTO login_info
                (Saved_username, Saved_password) VALUES(?,?)'''
                data_insert_tuple = (saving_username,saving_password)
                c.execute(data_insert_query,data_insert_tuple)
                conn.commit() #commit changes
                register_button.config(text="Back to Login Page", command=mainloop)
                back_button.grid_remove()
                
    
    register_button=ttk.Button(registerframe, text="Register", command=confirm_register)
    register_button.grid(column=3,row=4,sticky=E)
    back_button=ttk.Button(registerframe, text="Back", command=mainloop)
    back_button.grid(column=1,row=5,sticky=W)
    
def mainloop():
    def login():
        username_enter= username_entry.get()
        c.execute("SELECT COUNT(*) from login_info WHERE Saved_username='"+username_enter+"'")
        userresult= c.fetchone()
        if int(userresult[0]) > 0:
            password_enter = password_entry.get()
            c.execute("SELECT COUNT(*) from login_info WHERE Saved_username='"+username_enter+"' AND Saved_password='"+password_enter+"'")
            passwordresult= c.fetchone()
            if int(passwordresult[0]) > 0:
                error.config(text="Successful Login")
            else:    
                error.config(text="Incorrect password")
        else:    
            error.config(text="User does not exist.\nPlease register.")

    root.title("Login Page")

    mainframe = ttk.Frame(root,padding="3 3 12 12")
    mainframe.grid(column=0,row=0, sticky=(N,W,E,S))
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0, weight=1)

    username= StringVar()
    username_entry = ttk.Entry(mainframe,width=20,textvariable=username)
    username_entry.grid(column=2,row=1,sticky=(W,E))

    password= StringVar()
    password_entry = ttk.Entry(mainframe,width=20,textvariable=password,show="*")
    password_entry.grid(column=2,row=2,sticky=(W,E))

    ONorOFF = IntVar()
    def showpass():
        if(ONorOFF.get()==1):
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    ttk.Checkbutton(mainframe,text='Show password',command=showpass,variable=ONorOFF,onvalue=1, offvalue=0).grid(column=3,row=2,sticky=W)

    ttk.Label(mainframe, text="Username:").grid(column=1,row=1,sticky=W)
    ttk.Label(mainframe, text="Password:").grid(column=1,row=2,sticky=W)
    error=ttk.Label(mainframe, text="")
    error.grid(column=1,row=6,sticky=W,columnspan=20)

    ttk.Button(mainframe, text="Login", command=login).grid(column=3,row=4,sticky=E)

    ttk.Button(mainframe, text="Register", command=register).grid(column=1,row=4,sticky=W)

    ttk.Button(mainframe, text="Forgot password", command=forgot_password).grid(column=1,row=5,sticky=W)

    root.mainloop()

def forgot_password():
    root.title("Login Page")

    fpframe = ttk.Frame(root,padding="3 3 12 12")
    fpframe.grid(column=0,row=0, sticky=(N,W,E,S))
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0, weight=1)
    
    ttk.Label(fpframe, text="Username:").grid(column=1,row=1,sticky=W)
    ttk.Label(fpframe, text="New Password:").grid(column=1,row=2,sticky=W)
    ttk.Label(fpframe, text="Confirm New Password:").grid(column=1,row=3,sticky=W)

    username= StringVar()
    username_entry = ttk.Entry(fpframe,width=20,textvariable=username)
    username_entry.grid(column=2,row=1,sticky=(W,E))

    new_password= StringVar()
    new_password_entry = ttk.Entry(fpframe,width=20,textvariable=new_password,show="*")
    new_password_entry.grid(column=2,row=2,sticky=(W,E))

    confirm_new_password= StringVar()
    confirm_new_password_entry = ttk.Entry(fpframe,width=20,textvariable=confirm_new_password,show="*")
    confirm_new_password_entry.grid(column=2,row=3,sticky=(W,E))

    ONorOFF = IntVar()
    def showpass():
        if(ONorOFF.get()==1):
            new_password_entry.config(show="") 
            confirm_new_password_entry.config(show="")
        else:
            new_password_entry.config(show="*") 
            confirm_new_password_entry.config(show="*")

    error=ttk.Label(fpframe, text="")
    error.grid(column=1,row=4,sticky=W,columnspan=20)

    ttk.Checkbutton(fpframe,text='Show password',command=showpass,variable=ONorOFF,onvalue=1, offvalue=0).grid(column=3,row=3,sticky=W)

    def resetpass():
        saving_username= username_entry.get()
        saving_new_password= new_password_entry.get()
        compare_password=confirm_new_password.get()

        if not saving_new_password==compare_password:
            error.config(text="Error: Password does not match")
        else:
            c.execute("SELECT COUNT(*) from login_info WHERE Saved_username='"+saving_username+"'")
            result= c.fetchone()
            if int(result[0]) > 0:
                error.config(text="Password updated.")
                data_insert_query='''UPDATE login_info SET Saved_password = ? WHERE Saved_username = ?
                '''
                data_insert_tuple = (saving_new_password,saving_username)
                c.execute(data_insert_query,data_insert_tuple)
                conn.commit() #commit changes
                change_pass_button.config(text="Back to Login Page", command=mainloop)
                back_button.grid_remove()
            else:    
                error.config(text="Error: This Username does not exist.\nPlease create one.")

    change_pass_button=ttk.Button(fpframe, text="Change password", command=resetpass)
    change_pass_button.grid(column=3,row=4,sticky=E)
    back_button=ttk.Button(fpframe, text="Back", command=mainloop)
    back_button.grid(column=1,row=5,sticky=W)


mainloop()