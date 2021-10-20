from tkinter import *
from tkinter import ttk,messagebox,colorchooser,filedialog
from PIL import Image,ImageTk
import threading as td
import requests
from MY_PACKAGE.project_parser import Parser#when calling this whole main_win as a module
# from project_parser import Parser #when we will use this main_win as an application


class LogIn(Toplevel):
    max_height=1500
    max_width=700
    primary_color="#091353"

    def __init__(self,email=None):
        
        super().__init__()

        self.email=email#for verfication and connecting to server
        
        self.geometry(f"{self.max_height}x{self.max_width}")
        self.name="DoCu_It"
        self.title(self.name)
        self.resizable(0,0)
        self.any_project=False#needs to be false. Used for enabling options and disabling options if nothing project is searched
        # self.any_project=True#needs to be false
        self.proj_title=None
        self.count_paras=0
        self.not_blank_position=0
        self.project_data_encoded=None
        self.docx_save=None
        self.color_choice=["000000"]*5
        # text var
        self.search_var=StringVar()
        self.upload_var=StringVar()
        

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
        self.rocket= Image.open(r'MY_PACKAGE\Images\rocket.png').resize((300,300))
        self.rocket= ImageTk.PhotoImage(self.rocket)
        Label(self.upload,image=self.rocket).pack()
        #upload
        self.file_upload_frame=LabelFrame(self.upload,text="Upload File",padx=8,pady=4)
        self.file_upload_frame.pack()
        self.upload_icon=Image.open(r"MY_PACKAGE\Images\upload.png")
        self.upload_icon=ImageTk.PhotoImage(self.upload_icon.resize((50,50)))
        Label(self.file_upload_frame,image=self.upload_icon).pack(side=LEFT)
        self.file_directory=ttk.Entry(self.file_upload_frame,width=50,textvariable=self.upload_var)
        self.file_directory.pack(side=LEFT)
        self.browse_file=ttk.Button(self.file_upload_frame,text="Browse",command=self.browse)
        self.browse_file.pack(side=LEFT,padx=5)
        self.upload_file=ttk.Button(self.file_upload_frame,text="Upload",command=self.upload_file)
        self.upload_file.pack(side=LEFT)
        
        #download
        self.file_download_frame=LabelFrame(self.upload,text="Download File",padx=4,pady=4)
        self.file_download_frame.pack(pady=50)
        self.download_icon= Image.open(r'MY_PACKAGE\Images\download.png').resize((50,50))
        self.download_icon= ImageTk.PhotoImage(self.download_icon)
        Label(self.file_download_frame,image=self.download_icon).pack(side=LEFT)
        self.file_view=ttk.Combobox(self.file_download_frame,width=50)
        self.file_view.pack(side=LEFT)
        self.download_file=ttk.Button(self.file_download_frame,text="Download",command=self.download_file)
        self.download_file.pack(side=LEFT,padx=5)
        
        self.download_file_options()
        
        
        

    def download_file_options(self):
        def process():
            uploded_file_link="http://127.0.0.1:5000/allfile"
            try:
                file_response= requests.post(uploded_file_link,data={"email":self.email})
                actual_data=file_response.json()
                data=[]
                for i in actual_data:
                    data.append(actual_data[i])
                self.uploaded_file_server=data
                self.file_view["values"]=data
                self.file_view.update()
            except:
                data=None
                self.file_view["values"]=tuple(data)
                self.file_view.update()
            
        thread=td.Thread(target=process,daemon=True)
        thread.start()
    def browse(self):
        file_types=[ ("Word file",".docx") ]
        location = filedialog.askopenfilename(initialdir="Your Projects",title="Select file",filetypes=file_types)
        self.upload_var.set(location)
    
    def upload_file(self):
        def process():
            if self.upload_var.get().strip()!="":
                try:
                    file_content=open(self.upload_var.get(),"rb")
                except:
                    messagebox.showerror(self.name,"Plz check the file location. Some error occured")
                data={
                    "email":self.email,
                }
                file={
                    "upload":file_content
                }
                link="http://127.0.0.1:5000/upload"
                res=requests.post(link,data=data,files=file)
                messagebox.showinfo(self.name,res.text)
                file_content.close()
                self.download_file_options()
            else:
                messagebox.showwarning(self.name,"Plz select a file")
        thread=td.Thread(target=process)
        thread.daemon=True  
        thread.start()

    def download_file(self):
        def process():
            req_file=self.file_view.get()
            if req_file.strip()!="":
                data={
                    "email":self.email,
                    "file":req_file
                }
                link="http://127.0.0.1:5000/download"
                res=requests.post(link,data=data)
                with open(fr"Your Projects\files from docuit server\{req_file}","wb") as f:
                        f.write(res.content)
                messagebox.showinfo(self.name,"Downloaded")
        thread=td.Thread(target=process)
        thread.daemon=True  
        thread.start()

        
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
            messagebox.showinfo(self.name,f"Saved {self.proj_title}.docx")
        except Exception as e:
            messagebox.showerror(self.name,f"Fail to save {self.proj_title}.docx")
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
    a=LogIn(email="arna")
    a.mainloop()
    print(a.color_choice)
