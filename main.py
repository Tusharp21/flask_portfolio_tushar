from flask import Flask,render_template,request,url_for
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os


file_path = os.path.join(os.path.dirname(__file__), 'config.json')

with open(file_path,'r') as c:
    params = json.load(c)["params"]
local_server = True

app = Flask(__name__,static_url_path='/static')

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT= '465',
    MAIL_USE_SSL= True,
    MAIL_USERNAME= params['gmail_user'],
    MAIL_PASSWORD= params['gmail_pass']

)
mail = Mail(app)

if (params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=True)


class Blogs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(120), nullable=False)
    posts = db.Column(db.String(120), nullable=False)
    img_url = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=True)


class Work_exp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(120), nullable=False)
    overview = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.String(120), nullable=False)
    end_date = db.Column(db.String(120), nullable=True)



# -----------------------------------------------------------------------------------------------
@app.route("/")
def index():
    posts = Blogs.query.filter_by().all()
    exp = Work_exp.query.filter_by().all()
    return render_template("index.html", params=params, posts=posts , work_exp=exp)


# -----------------------------------------------------------------------------------------------
@app.route("/blog/<string:slug>" , methods=['GET'])
def blogs(slug):
    posts = Blogs.query.filter_by(slug=slug).first()
    return render_template("blog.html", params=params, posts=posts)



# -----------------------------------------------------------------------------------------------
@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form.get('contactName')
        email = request.form.get('contactEmail')
        subject = request.form.get('contactSubject')
        temp_message = request.form.get('contactMessage')
        message =  email + temp_message 
        
        entry = Contacts(name=name, email=email, subject=subject, message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New Massage in Portfolio Name = '+name,
                        sender=email,
                        recipients=[params['gmail_user']],
                        body= message
                        )
        

    return render_template('index.html')    




# -----------------------------------------------------------------------------------------------
@app.route("/style.html" )
def style():

    return render_template("style.html", params=params)



app.run(debug=True)



