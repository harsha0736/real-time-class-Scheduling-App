from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'class_scheduler.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for('signup'))

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            flash("Logged in successfully!", "success")
            return redirect(url_for('features'))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template('login.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        time = request.form.get('time')
        room = request.form.get('room')
        subject = request.form.get('subject')
        instructor = request.form.get('instructor')

        new_schedule = Schedule(time=time, room=room, subject=subject, instructor=instructor)
        db.session.add(new_schedule)
        db.session.commit()
        flash("Schedule added successfully!", "success")
        return redirect(url_for('schedule'))

    schedules = Schedule.query.all()
    return render_template('schedule.html', schedules=schedules)

@app.route('/view-database')
def view_database():
    """View all data in the database."""
    users = User.query.all()
    schedules = Schedule.query.all()
    
    return render_template('view_database.html', users=users, schedules=schedules)



# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()
    seed_data()

def seed_data():
    if not User.query.first():
        user = User(name="Admin", email="admin@example.com", password="password")
        db.session.add(user)

    if not Schedule.query.first():
        sample_schedule = Schedule(
            time="10:00 AM - 11:00 AM",
            room="101",
            subject="Mathematics",
            instructor="Dr. Smith"
        )
        db.session.add(sample_schedule)

    db.session.commit()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
