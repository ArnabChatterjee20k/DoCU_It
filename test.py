from MY_PACKAGE import project_parser

WebScrap=project_parser.Parser("website")
WebScrap.parse()
# print(WebScrap.collection_paragraphs)
# print(WebScrap.project_paras)
# WebScrap.save("arnab")
j=0
for i in WebScrap.collection_paragraphs[:4]:
    j+=1
    print(j,i)
    print()
# WebScrap.save_docx("arnab")

