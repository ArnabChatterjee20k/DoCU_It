import requests


link="http://127.0.0.1:5000/"

# uploading
data={
    "email":"arna",
    "file":"DATABASE.docx"
}
testfile=open(r"server_testing\DATABASE.docx","rb")
file={
    "upload":testfile
}
route="upload"
response=requests.post(link+route,data=data,files=file)
testfile.close()
print(response.status_code)
print(response.text)


# downloading
route="download"
data={
    "email":"arna",
    "file":"DATABASE.docx"
}
response=requests.post(link+route,data=data)
print(response.status_code)
print(response.text)

