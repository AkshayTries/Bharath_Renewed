from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bharathDB.db'  # Corrected typo here
db = SQLAlchemy(app)  # Initialising the database

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contactus', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        ticket_name = request.form.get('name')
        ticket_email = request.form.get('email')
        ticket_message = request.form.get('message')

        # Debugging: Print the form data
        print(f"Form Data - Name: {ticket_name}, Email: {ticket_email}, Message: {ticket_message}")

        if not ticket_name or not ticket_email or not ticket_message:
            return 'Missing form data. Please fill out all fields.'

        new_task = Ticket(name=ticket_name, email=ticket_email, content=ticket_message)

        try:
            db.session.add(new_task)
            db.session.commit()
            print("Ticket saved to database successfully!")  # Debugging
            return redirect('/contactus')
        except Exception as e:
            print(f"Error: {e}")  # Debugging
            return 'There was an issue submitting your ticket.'
    else:
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

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True)