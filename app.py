from flask import Flask,render_template,request#request from browser
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
#URI address where database is running
#'postgresql://username:password@localhost/dbname'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:post1gres@localhost/height_collector' 
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgres://kwamqvjkmniiah:5809082c7a3d8362b2993ecc4880636e7d33b5f8190f34859722bca3cf9569cc@ec2-52-44-166-58.compute-1.amazonaws.com:5432/d762oq4r99u7qp?sslmode=require'
db=SQLAlchemy(app)

#Blueprint that hold database model
class Data(db.Model):  #subclass of other class constructed by SQLAlchemy
    __tablename__="data" 
    id=db.Column(db.Integer,primary_key=True)
    email_=db.Column(db.String(120),unique=True) #not more than 120 characters
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=['POST']) #implicit GET method 
def success():
    #to access email and data from post method
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            #create obj instance for Data Class
            data=Data(email,height) #passed to __init__ 
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count = db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            return render_template("success.html") 
    return render_template("index.html",text="Already existing email address...please enter new one")           


if __name__ == '__main__':
    app.debug=True   
    app.run() #default port 5000 or specify app.run(port=5001)
