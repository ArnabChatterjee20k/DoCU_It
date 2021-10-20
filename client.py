import re
from MY_PACKAGE.main_win import LogIn
from tkinter import *
from tkinter import ttk,messagebox
from PIL import ImageTk,Image
from functools import partial
import requests,threading
# import os
# os.startfile("server.py")#for starting the backend server
window=Tk()
title="DoCu_It"
window.title(title)

# server link
server_link_register="http://127.0.0.1:5000/register"
server_link_login="http://127.0.0.1:5000/login"
server_link_filelist="http://127.0.0.1:5000/allfile"

# text variables
email=StringVar()
password=StringVar()
email_reg=StringVar()
password_reg=StringVar()

email_placeholder="Enter your email"
password_placeholder="Enter your password"

place_holder={"email":email_placeholder,"password":password_placeholder}
#functions for buttons
def toggle_pass(entry_var,button):
    """to show/hide pass"""
    if entry_var.cget("show")=="*":
        entry_var.config(show="")
        button.config(text="Hide")
    elif entry_var.cget("show")=="":
        entry_var.config(show="*")
        button.config(text="Show")


def focus_out(place_hold_name=None,entry_var=None,button=None,textvar=None):
    """event handling when enter a field.""" 
    if button!=None:
        button.config(state="disabled")
        if textvar.get().strip()=="":
            textvar.set(place_holder["password"])
    if entry_var!=None:
        if entry_var.get().strip()=="":
            entry_var.set(place_holder[f"{place_hold_name}"])

def focus_in(place_hold_name=None,entry_var=None,button=None,textvar=None):
    """event handling when leave a field.""" 
    if button!=None:
        button.config(state="normal")
        if textvar.get().strip()==place_holder["password"]:
            textvar.set("")
    
    if entry_var!=None:
        if entry_var.get().strip()==place_holder[f"{place_hold_name}"]:
            entry_var.set("")

restrict=0#to restrict the number of windows
def login_init():
    global restrict
    def on_close():
        """to restrict the number of automate window opened"""
        global restrict
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            restrict=0
            main.destroy()
    data={
        "email":email.get().strip(),
        "password":password.get().strip()
    }
    # cross checking
    if (data["email"]=="" or data["email"]==email_placeholder) or (data["password"]=="" or data["password"]==password_placeholder):
        messagebox.showerror("DoCu_It","plz fill the details")
    else:
        try:
            # sending data to server database
            response=requests.post(url=server_link_login,data=data)
            status=response.json()
            email.set(email_placeholder)
            password.set(password_placeholder)
            messagebox.showinfo("DoCu_It",status["message"])
            if status.get("user") and restrict==0:#as it does not stop the code if key not found
                try:
                    credential=data["email"]
                    main=LogIn(email=credential)
                    restrict=1
                    window.wm_state('iconic')
                    main.protocol("WM_DELETE_WINDOW",on_close)
                    main.mainloop()
                except:
                    pass
            elif restrict==1:
                messagebox.showwarning(title,"At a time only window can be opened")
        except:
            messagebox.showerror("DOCu-It","Server connection not established")
def regester_init():
    data={
        "email":email_reg.get().strip(),
        "password":password_reg.get().strip()
    }
    # cross checking
    if (data["email"]=="" or data["email"]==email_placeholder) or (data["password"]=="" or data["password"]==password_placeholder):
        messagebox.showerror("DoCu_It","plz fill the details")
    
    else:
        try:
            response=requests.post(url=server_link_register,data=data)
            status=response.json()
            # print(status)
            email_reg.set(email_placeholder)
            password_reg.set(password_placeholder)
            messagebox.showinfo("DoCu_It",status["message"])
        except:
            messagebox.showerror("DOCu-It","Server connection not established")

def process(funcname):
    '''SO that window doesnot crashes while registering or login'''
    thread=threading.Thread(target=funcname)
    thread.daemon=True
    thread.start()


# colors
primary_color="#091353"#dark_blue


# configuring window
window.geometry("1500x700")
window.resizable(False,False)
# Making a layout
img_frame=Frame(window,bg=primary_color)
auth_img=Image.open("Images/auth.png")
auth_img=auth_img.resize((300,200))
auth_img=ImageTk.PhotoImage(auth_img)
ttk.Label(img_frame,image=auth_img).pack(ipady=300,ipadx=20)
img_frame.pack(side=LEFT,fill="y")

#Tabs_Frame
tabs_frame=Frame(window,height=700,width=1400)
tabs_frame.pack(side=LEFT,fill=BOTH)

tabs=ttk.Notebook(tabs_frame,height=800,width=1400)
tabs.pack(pady=(5,0),fill="both")

login_tab=Frame(tabs,width=1400,height=700,bg=primary_color)
register_tab=Frame(tabs,width=1400,height=700,bg=primary_color)

login_tab.pack(fill="both")
register_tab.pack(fill="both")

tabs.add(login_tab,text="LOGIN")
tabs.add(register_tab,text="REGISTER")

# adding components to login tab
log_image=Image.open("Images/login.png")
log_image=log_image.resize((100,100))
log_image=ImageTk.PhotoImage(log_image)
Label(login_tab,bg=primary_color,image=log_image).pack(pady=(0,40))
Label(login_tab,text="Login to get access to your saved automated projects.\nYour safety our first priority",bg=primary_color,font=("Courier","15","bold"),fg="#ffeb3b").pack(pady=(0,40))

email_entry=ttk.Entry(login_tab,width=40,font=("Courier","18"),textvariable=email)
email_entry.pack(pady=(20,70))

email.set(place_holder["email"])
email_entry.bind("<FocusIn>",lambda e:focus_in(place_hold_name="email",entry_var=email,button=None,textvar=None))
email_entry.bind("<FocusOut>",lambda e:focus_out(place_hold_name="email",entry_var=email,button=None,textvar=None))

pass_frame=ttk.Frame(login_tab)
pass_frame.pack()
password_entry=ttk.Entry(pass_frame,width=37,font=("Courier","18"),show="",textvariable=password)
show_pass=Button(pass_frame,text="Hide",state="disabled")
show_pass.pack(side=RIGHT,fill=BOTH)
show_pass.config(command=partial(toggle_pass,password_entry,show_pass))
password_entry.pack()

password.set(place_holder["password"])
password_entry.bind("<FocusIn>",lambda e:focus_in(textvar=password,entry_var=None,button=show_pass))#since evnts returns an event obejct so e 
password_entry.bind("<FocusOut>",lambda e:focus_out(textvar=password,entry_var=None,button=show_pass))

submit=ttk.Button(login_tab,text="LOG IN",command=partial(process,login_init))

submit.pack(pady=40)


# Register components
registration_image=Image.open("Images/register.png")
registration_image=registration_image.resize((100,100))
registration_image=ImageTk.PhotoImage(registration_image)

Label(register_tab,bg=primary_color,image=registration_image).pack(pady=(0,40))
Label(register_tab,text="Plz Register to enjoy our automation service",bg=primary_color,font=("Courier","15","bold"),fg="#ffeb3b").pack(pady=(0,40))

email_registry=ttk.Entry(register_tab,width=40,font=("Courier","18"),textvariable=email_reg)
email_registry.pack(pady=(20,70))

email_reg.set(place_holder["email"])
email_registry.bind("<FocusIn>",lambda e:focus_in(place_hold_name="email",entry_var=email_reg,button=None,textvar=None))
email_registry.bind("<FocusOut>",lambda e:focus_out(place_hold_name="email",entry_var=email_reg,button=None,textvar=None))



pass_reg_frame=ttk.Frame(register_tab)
pass_reg_frame.pack()
password_registry=ttk.Entry(pass_reg_frame,width=37,font=("Courier","18"),show="",textvariable=password_reg)
show_pass_reg=Button(pass_reg_frame,text="Hide",state="disabled")
show_pass_reg.pack(side=RIGHT,fill=BOTH)
show_pass_reg.config(command=partial(toggle_pass,password_registry,show_pass_reg))
password_registry.pack()

password_reg.set(place_holder["password"])
password_registry.bind("<FocusIn>",lambda e:focus_in(textvar=password_reg,entry_var=None,button=show_pass_reg))
password_registry.bind("<FocusOut>",lambda e:focus_out(textvar=password_reg,entry_var=None,button=show_pass_reg))

register=ttk.Button(register_tab,text="Register",command=partial(process,regester_init))
register.pack(pady=40)



window.mainloop()