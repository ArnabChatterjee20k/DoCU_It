from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
# endpoints and routes
@app.route("/upload_file",methods=["POST"])
def save_file():
    return jsonify(request.json)

app.run()
