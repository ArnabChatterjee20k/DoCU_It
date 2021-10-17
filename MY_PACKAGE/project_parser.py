import requests 
from bs4 import BeautifulSoup
from docx import Document
class Parser:
    source_link="https://en.wikipedia.org/wiki/"
    def __init__(self,project_topic):
        self.project_topic = project_topic
        self.project_paras=0
        self.completed=None
        self.collection_paragraphs=None#it will contain the whole data

    def parse(self):
        response=requests.get(Parser.source_link+self.project_topic)
        if response.status_code!=200:
            print("""Some problem occured... Plz make sure the content is heading is correct. If correct then some connection issue"""
)
            return """Some problem occured... Plz make sure the content is heading is correct. If correct then some connection issue"""
        soup=BeautifulSoup(response.content,"html.parser")
        body=soup.body
        #deleting unnecessary content
        try:
            for i in body.find_all(class_="reference"):
                i.decompose()
        except:
            pass
        
        # parsing html paragraphs to text
        parsed_pragraphs="" #to store parsed paragraphs
        number_of_para=0 #to count number of para
        para_list=[]#it will contain a list of all paragrahs stored in different tuples
        html_para=body.find_all("p")
        
        for para in html_para:
            para_list_pointer=""
            number_of_para+=1
            parsed_pragraphs+=para.text
            para_list_pointer+=para.text
            para_list_pointer=para_list_pointer.encode("utf-8","ignore")
            para_list.append((para_list_pointer))
            para_list_pointer=""

        self.project_paras=number_of_para
        self.completed=parsed_pragraphs
        self.collection_paragraphs=para_list

    def save_docx(self,file):
        # with open(f"{file}.docx","w") as f:#saving in docx mode will not cause any problem of encoding
        #     f.write(self.completed)
        document = Document()
        document.add_heading('Document Title', 0)
        for i in self.collection_paragraphs:
            document.add_paragraph(str(i), style='Intense Quote')
        document.save(f'{file}.docx')
    def save_txt(self,file):
        with open(f"{file}.txt","w") as f:
            f.write(self.completed)
    def __repr__(self) :
        return(str(self.completed.encode("utf-8","ignore")))                
# obj1=Parser("data")
# obj1.parse()
# for i in obj1.collection_paragraphs[:4]:
#     print(i)
# obj1.save("text.text")


