from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




SMTP_SERVER = "smtp.gmail.com"  # Use your email provider's SMTP server
SMTP_PORT = 587  # Port for Gmail SMTP (use 465 for SSL)
EMAIL_ADDRESS = "akshayalva030303@gmail.com"
recipient = "akshayalva030303@gmail.com"
EMAIL_PASSWORD = "fgpu uxzk mjxs tzkv"

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



        if not ticket_name or not ticket_email or not ticket_message:
            return 'Missing form data. Please fill out all fields.'

        new_task = Ticket(name=ticket_name, email=ticket_email, content=ticket_message)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient
        msg["Subject"] = "New Message from Website"
        body = ticket_name+" ("+ticket_email+") has sent the following message:\n\n"+ticket_message
        msg.attach(MIMEText(body, "plain"))

        msg2 = MIMEMultipart()
        msg2["From"] = EMAIL_ADDRESS
        msg2["To"] = ticket_email
        msg2["Subject"] = "Bharath Charitable Trust Message"
        body2 = "Your message to the Bharath Charitable Trust has been sent successfully. You will be contacted shortly.\nThank you."
        msg2.attach(MIMEText(body2, "plain"))

        try:
            db.session.add(new_task)
            db.session.commit()
            print("Ticket saved to database successfully!")  # Debugging
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # Secure connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
            server.sendmail(EMAIL_ADDRESS, ticket_email, msg2.as_string())
            server.quit()
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