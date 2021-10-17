from tkinter import *
from tkinter import ttk,messagebox,colorchooser
from PIL import Image,ImageTk
import threading as td
from project_parser import Parser

class LogIn(Tk):
    max_height=1500
    max_width=700
    primary_color="#091353"
    def __init__(self):
        super().__init__()
        self.geometry(f"{self.max_height}x{self.max_width}")
        self.title("DOCU_It")
        self.resizable(0,0)
        self.any_project=False#needs to be false
        # self.any_project=True#needs to be false
        self.proj_title=None
        self.count_paras=0
        self.not_blank_position=0
        self.project_data=None
        self.color_choice=["black"]*5
        # text var
        self.search_var=StringVar()

        # Image frame
        self.img=Image.open("Images/icon.ico")
        self.img=self.img.resize((200,200))
        self.img=ImageTk.PhotoImage(self.img)
        self.img_frame=Frame(self)
        Label(self.img_frame,image=self.img,text="Project Automation",compound=TOP,font=("Microsoft JhengHei UI Light","16")).pack()
        self.img_frame.pack(side=LEFT,ipadx=10)

        

        # tabs
        self.tab=ttk.Notebook(self,height=self.max_height)
        self.tab.pack(fill=BOTH,pady=10)

        self.automate=Frame(self.tab,width=self.max_width,height=self.max_height,bg=self.primary_color)
        self.upload=Frame(self.tab,width=self.max_width,height=self.max_height)

        self.automate.pack(fill=BOTH)
        self.upload.pack(fill=BOTH)

        self.tab.add(self.automate,text="Automate")
        self.tab.add(self.upload,text="Upload")

        self.api_img=ImageTk.PhotoImage(Image.open("Images/internet.png"))
        Label(self.automate,image=self.api_img,bg=self.primary_color).pack()
        Label(self.automate,text="DoCu_IT",font=("Microsoft JhengHei UI Light","24","bold"),bg=self.primary_color,fg="#F0A500").pack(pady=(10,0))
        Label(self.automate,text="You search,Arnab Chatterjee will automate",font=("Microsoft JhengHei UI Light","15","bold"),bg=self.primary_color,fg="#F0A500").pack(pady=(4,0))

        self.search=Frame(self.automate,width=37)
        self.search.pack(pady=(2,40))

        self.search_bar=ttk.Entry(self.search,width=37,font=("Courier","18"),textvariable=self.search_var)
        self.search_bar.pack(side=LEFT)
        self.search_ico=ImageTk.PhotoImage(Image.open("Images/search.png"))

        self.search_btn=ttk.Button(self.search,image=self.search_ico,command=self.search_project)
        self.search_btn.pack(side=LEFT)
        

        self.btn_frame=Frame(self.automate,bg=self.primary_color)
        self.btn_frame.pack()
        
        self.automate_btn=ttk.Button(self.btn_frame,text="Automate")
        self.automate_btn.pack(side=LEFT,padx=(0,7))
        
        self.overview=ttk.Button(self.btn_frame,text="Overview",command=self.open_modal)
        self.overview.pack(side=LEFT)

        for child in self.btn_frame.winfo_children():
            if self.any_project==False:
                child["state"]="disabled"

    def search_project_initialiser(self,var):
        project_to_be_automated=var.get().strip()
        if project_to_be_automated!="":
            self.proj_title=project_to_be_automated
            project=Parser(project_to_be_automated)
            project.parse()
            self.project_data=project.collection_paragraphs
            # print(self.project_data)
            # print(project)
            for i in range(len(self.project_data)):
                if self.project_data[i].strip()!="":
                    break
            self.not_blank_position=i
            
            messagebox.showinfo("DOCu-It","Your project data is ready")
            self.count_paras=project.project_paras
            self.any_project=True
            for child in self.btn_frame.winfo_children():
                child["state"]="normal"
            self.btn_frame.update()
            
        else:
            messagebox.showinfo("DOCu-It","Please enter the project name")
    def search_project(self):
        """for search button. Thread has been used to conduct this process parallely and the window does not get irresponsive"""
        thread=td.Thread(target=self.search_project_initialiser,args=(self.search_var,))
        thread.daemon=True
        thread.start()

    def open_modal(self):
        def color_change(btn,button_index):
            selected_color = colorchooser.askcolor()[1]
            btn["bg"]=selected_color
            self.color_choice[button_index]=selected_color

        def view_para():
            para_number=int(para_count.get())-1
            project_display.delete("1.0",END)
            project_display.insert(INSERT,self.project_data[para_number])
            project_display.update()

        modal=Toplevel(self)
        modal.title(f"DOCu-It--Overview of ({self.proj_title})")
        modal.geometry("700x288")
        modal.resizable(0,0)
        project_display=Text(modal,width=40,height=17,relief=SUNKEN,bd=2,wrap=WORD,font=("10"),spacing2=5)
        project_display.pack(side=LEFT,pady=3,padx=4,anchor=N)

        project_display.insert(INSERT,self.project_data[self.not_blank_position])

        options_frame=Frame(modal,width=60,height=17,relief=SUNKEN,bd=2)
        options_frame.pack(anchor=CENTER,pady=20)

        para=LabelFrame(options_frame,text="See Para")
        para.grid(row=0,padx=6,pady=(10,15))
        para_count=ttk.Spinbox(para,from_=(self.not_blank_position+1),to=self.count_paras,width=5)
        
        para_count.set(f"{self.not_blank_position+1}")
        para_count.pack()

        para_count.bind("<Button-1>",lambda e:view_para())
        color=LabelFrame(options_frame,text="COLOR")
        color.grid(row=1,ipadx=3,padx=10)

        color_1=Button(color,width=2,height=1,command=lambda:color_change(color_1,0))
        color_1.grid(row=0,column=0)

        color_2=Button(color,width=2,height=1,command=lambda:color_change(color_2,1))
        color_2.grid(row=0,column=1)

        color_3=Button(color,width=2,height=1,command=lambda:color_change(color_3,2))
        color_3.grid(row=0,column=2)

        color_4=Button(color,width=2,height=1,command=lambda:color_change(color_4,3))
        color_4.grid(row=1,column=0)

        color_5=Button(color,width=2,height=1,command=lambda:color_change(color_5,4))
        color_5.grid(row=1,column=1)
        
        
        for i in color.winfo_children():
            i["padx"]="2"
            i["pady"]="2"
            i["bg"]="black"
            
        

    
        

a=LogIn()
# style=ttk.Style()
# style.theme_use('alt')
# print(style.theme_names())
a.mainloop()
# print(a.project_data)
# print(a.color_choice)