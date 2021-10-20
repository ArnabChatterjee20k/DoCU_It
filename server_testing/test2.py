import requests


link="http://127.0.0.1:5000/"

# uploading
data={
    "email":"arna"
}
testfile=open(r"server_testing\new.txt","rb")
file={
    "upload":testfile
}
route="upload"
# response=requests.post(link+route,data=data,files=file)
testfile.close()
# print(response.status_code)
# print(response.text)

#downloading
route="download"
data={
    "email":"arna",
    # "file":"new.t"
    "file":"new.txt"
}
# response=requests.post(link+route,data=data)
# print(response.status_code)
# print(response.text)

route="allfile"
response=requests.post(link+route,data=data)
print(response.json())

