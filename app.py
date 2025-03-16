from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name  = db.Column(db.String(20),nullable=False)
    email= db.Column(db.String(30),nullable=False)
    content  = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contactus')
def contact():
    return render_template('contactus.html')

@app.route('/founders')
def founders():
    return render_template('founders.html')

@app.route('/health')
def health():
    return render_template('health.html')

@app.route('/education')
def education():
    return render_template('education.html')




if __name__ =="__main__":
    app.run(debug=True)