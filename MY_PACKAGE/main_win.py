from tkinter import *
from tkinter import ttk,messagebox,colorchooser
from PIL import Image,ImageTk
import threading as td
# from MY_PACKAGE.project_parser import Parser#when calling this whole main_win as a module
from project_parser import Parser #when we will use this main_win as an application


class LogIn(Toplevel):
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
        self.project_data_encoded=None
        self.docx_save=None
        self.color_choice=["000000"]*5
        # text var
        self.search_var=StringVar()

        # Image frame
        self.img=Image.open("MY_PACKAGE\Images\icon.ico")
        self.img=self.img.resize((200,200))
        self.img=ImageTk.PhotoImage(self.img)
        self.img_frame=Frame(self)
        self.img_label=Label(self.img_frame,image=self.img,text="Project Automation",compound=TOP,font=("Microsoft JhengHei UI Light","16"))
        self.img_label.pack()
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

        self.api_img1=Image.open("MY_PACKAGE\Images\internet.png")
        self.api_img=ImageTk.PhotoImage(self.api_img1)
        Label(self.automate,image=self.api_img,bg=self.primary_color).pack()
        Label(self.automate,text="DoCu_IT",font=("Microsoft JhengHei UI Light","24","bold"),bg=self.primary_color,fg="#F0A500").pack(pady=(10,0))
        Label(self.automate,text="You search,Arnab Chatterjee will automate",font=("Microsoft JhengHei UI Light","15","bold"),bg=self.primary_color,fg="#F0A500").pack(pady=(4,0))

        self.search=Frame(self.automate,width=37)
        self.search.pack(pady=(2,40))

        self.search_bar=ttk.Entry(self.search,width=37,font=("Courier","18"),textvariable=self.search_var)
        self.search_bar.pack(side=LEFT)
        self.search_ico=ImageTk.PhotoImage(Image.open("MY_PACKAGE\Images\search.png"))

        self.search_btn=ttk.Button(self.search,image=self.search_ico,command=self.search_project)
        self.search_btn.pack(side=LEFT)
        

        self.btn_frame=Frame(self.automate,bg=self.primary_color)
        self.btn_frame.pack()
        
        self.automate_btn=ttk.Button(self.btn_frame,text="Automate",command=self.save_project)
        self.automate_btn.pack(side=LEFT,padx=(0,7))
        
        self.overview=ttk.Button(self.btn_frame,text="Overview",command=self.open_modal)
        self.overview.pack(side=LEFT)

        for child in self.btn_frame.winfo_children():
            if self.any_project==False:
                child["state"]="disabled"


        # upload/download section
        
    def search_project_initialiser(self,var):
        project_to_be_automated=var.get().strip()
        try:
            if project_to_be_automated!="":
                self.proj_title=project_to_be_automated
                thread=td.Thread(target=lambda:messagebox.showinfo("DOCu-It","Getting connected"),daemon=True)
                thread.start()
                project=Parser(project_to_be_automated)
                project.parse()
                self.project_data_encoded=project.collection_paragraphs
                self.docx_save=project.para_to_be_docxed
                # print(self.project_data_encoded)
                # print(project)
                for i in range(len(self.project_data_encoded)):
                    if self.project_data_encoded[i].strip()!="":
                        break
                self.not_blank_position=i
                self.proj_title=project_to_be_automated
                messagebox.showinfo("DOCu-It","Your project data is ready.\nClick automate to save.\nClick overview to make changes")
                self.count_paras=project.project_paras
                self.any_project=True
                for child in self.btn_frame.winfo_children():
                    child["state"]="normal"
                self.btn_frame.update()
                
            else:
                messagebox.showerror("DOCu-It","Please enter the project name")
        except:
            messagebox.showerror("DOCu-It"," Network issuue")
    def search_project(self):
        """for search button. Thread has been used to conduct this process parallely and the window does not get irresponsive"""
        thread=td.Thread(target=self.search_project_initialiser,args=(self.search_var,))
        thread.daemon=True
        thread.start()

    def save_project(self):
        try:
            Parser.save_docx(self.proj_title,collection_paragraphs=self.docx_save,colors=self.color_choice)
            messagebox.showinfo(self.title,f"Saved {self.proj_title}.docx")
        except Exception as e:
            messagebox.showerror(self.title,f"Fail to save {self.proj_title}.docx")
            print(e)

    def open_modal(self):
        def color_change(btn,button_index):
            selected_color = colorchooser.askcolor()[1]
            btn["bg"]=selected_color
            self.color_choice[button_index]=selected_color.strip("#")
        def view_para():
            para_number=int(para_count.get())-1
            project_display.delete("1.0",END)
            project_display.insert(INSERT,self.project_data_encoded[para_number])
            project_display.update()
        
        def save():
            current_change=project_display.get("1.0",END)
            current_index=int(para_count.get())-1
            self.project_data_encoded[current_index]=current_change
            self.docx_save[current_index]=current_change
            messagebox.showwarning("DOCu-It","current para changed")
            

        modal=Toplevel(self)
        modal.title(f"DOCu-It--Overview of ({self.proj_title})")
        modal.geometry("700x288")
        modal.resizable(0,0)
        Label(modal,fg="red",text="Some symbols are meant for encoding.They will be alright in docx.").pack()
        project_display=Text(modal,width=40,height=17,relief=SUNKEN,bd=2,wrap=WORD,font=("10"),spacing2=5)
        project_display.pack(side=LEFT,pady=3,padx=4,anchor=N)

        project_display.insert(INSERT,self.project_data_encoded[self.not_blank_position])

        options_frame=Frame(modal,width=60,height=17,relief=SUNKEN,bd=2)
        options_frame.pack(anchor=CENTER,pady=20)

        para=LabelFrame(options_frame,text="See Para")
        para.grid(row=0,padx=6,pady=(10,15))
        para_count=ttk.Spinbox(para,from_=(self.not_blank_position+1),to=self.count_paras,width=5)
        
        para_count.set(f"{self.not_blank_position+1}")
        para_count.pack()

        para_count.bind("<Button-1>",lambda e:view_para())
        color=LabelFrame(options_frame,text="Choose Colors")
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
        
        save_btn=ttk.Button(options_frame,text="SAVE",command=save)
        save_btn.grid(row=2)
        

    
        
if __name__=="__main__":##to execute the file when it will be running as program not as a module 
    a=LogIn()
    # style=ttk.Style()
    # style.theme_use('alt')
    # print(style.theme_names())
    a.mainloop()
    # print(a.project_data_encoded)
    print(a.color_choice)
    # print(a.proj_title)