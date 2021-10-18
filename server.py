import re
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import os
app=Flask(__name__)
# DATABASE
DB_NAME="DOCu_It.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

# It will work on one to many relationship
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    doc=db.relationship("ProjectFile",backref="user")

class ProjectFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    person_email = db.Column(db.String(100),db.ForeignKey("user.email"))

# since we have to send serializable object so this will help us.

# endpoints and routes
@app.route("/register",methods=["POST"])
def register():
    email=request.form.get("email")    
    password=request.form.get("password")    

    user=User.query.filter_by(email=email).first()
    if user:
        return {"message":"Email Already present"},409
    else:
        new_user=User(email=email,password=generate_password_hash(password,method="sha256"))
        db.session.add(new_user)
        db.session.commit()
        return {"message":"Registered"},201

@app.route("/login",methods=["POST"])
def login():
    email=request.form.get("email")    
    password=request.form.get("password")    
    user=User.query.filter_by(email=email).first()
    if user:
        #comparing hash and given password
        if check_password_hash(user.password,password):
            return {"user":True,"message":"Found"}
        else:
            return {"message":"Password Not Matching"},409
    else:
        return {"message":"User not found"},404
if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
