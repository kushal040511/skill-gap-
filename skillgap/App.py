import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random
import os
import os.path

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection function for SQLite
def get_db_cursor():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'skillgap.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

# Initialize database with tables
def init_db():
    conn, cursor = get_db_cursor()
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    
    # Create skill_courses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS skill_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        course TEXT NOT NULL
    )''')
    
    # Create user_notes table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        note TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Insert sample subjects and their recommended courses if table is empty
    cursor.execute("SELECT COUNT(*) FROM skill_courses")
    if cursor.fetchone()[0] == 0:
        sample_courses = [
            ('Mathematics', 'Advanced Mathematics Course'),
            ('Physics', 'Fundamentals of Physics'),
            ('Chemistry', 'Organic Chemistry Basics'),
            ('Biology', 'Human Biology Introduction'),
            ('History', 'World History Overview'),
            ('Geography', 'Understanding Earth Systems'),
            ('Political Science', 'Political Systems 101'),
            ('Economics', 'Principles of Economics'),
            ('Psychology', 'Introduction to Psychology'),
            ('Sociology', 'Understanding Human Society'),
            ('Computer Science', 'Basics of Programming'),
            ('Information Technology', 'IT Infrastructure Basics'),
            ('Environmental Science', 'Climate Change Awareness'),
            ('Physical Education', 'Fitness and Health Fundamentals'),
            ('Business Studies', 'Business Management Essentials'),
            ('Accountancy', 'Introduction to Accounting'),
            ('Statistics', 'Fundamentals of Statistics'),
            ('English', 'Mastering English Communication'),
            ('French', 'French Language Basics'),
            ('German', 'German Language for Beginners')
        ]
        cursor.executemany("INSERT INTO skill_courses (subject, course) VALUES (?, ?)", sample_courses)
    
    conn.commit()
    conn.close()

# Motivational quotes
quotes = [
    "Believe you can and you're halfway there.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Stay focused and never give up.",
    "Success doesn't just find you. You have to go out and get it."
]

# Home redirects to login or upload based on session
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('upload'))
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn, cursor = get_db_cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('upload'))
        return "Invalid credentials. Try again."
    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn, cursor = get_db_cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Please choose another."
    return render_template('signup.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Skill gap analyzer
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    skill_gaps = []
    selected_quote = random.choice(quotes)

    conn, cursor = get_db_cursor()
    cursor.execute("SELECT note FROM user_notes WHERE username = ?", (session['username'],))
    note_result = cursor.fetchone()
    note_text = note_result[0] if note_result else ''
    conn.close()

    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                df = pd.read_excel(file)

                if 'Marks' in df.columns and 'Subject' in df.columns:
                    skill_gaps_list = df[df['Marks'] < 60]['Subject'].tolist()
                    conn, cursor = get_db_cursor()
                    for skill in skill_gaps_list:
                        cursor.execute("SELECT course FROM skill_courses WHERE subject = ?", (skill,))
                        result = cursor.fetchone()
                        if result:
                            skill_gaps.append((skill, result[0]))
                        else:
                            skill_gaps.append((skill, "No course suggestion found"))
                    conn.close()
                else:
                    return "Uploaded file must contain 'Marks' and 'Subject' columns."
            except Exception as e:
                return f"Error reading uploaded file: {e}"

    return render_template('index.html', skill_gaps=skill_gaps, username=session['username'], quote=selected_quote, note=note_text)

# Important insights page
@app.route('/important', methods=['GET', 'POST'])
def important():
    average_marks = None
    highest_subject = None
    lowest_subject = None
    weak_subjects = []

    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                df = pd.read_excel(file)

                if 'Marks' in df.columns and 'Subject' in df.columns:
                    marks = df['Marks'].dropna().tolist()
                    subjects = df['Subject'].dropna().tolist()

                    if marks:
                        average_marks = round(sum(marks) / len(marks), 2)
                        max_mark = max(marks)
                        min_mark = min(marks)

                        highest_subject = (subjects[marks.index(max_mark)], max_mark)
                        lowest_subject = (subjects[marks.index(min_mark)], min_mark)

                        weak_subjects = [(subj, mark) for subj, mark in zip(subjects, marks) if mark < 60]
                else:
                    return "Uploaded file must contain 'Marks' and 'Subject' columns."
            except Exception as e:
                return f"Error processing file: {e}"

    return render_template(
        'important.html',
        average_marks=average_marks,
        highest_subject=highest_subject,
        lowest_subject=lowest_subject,
        weak_subjects=weak_subjects
    )

# Save user note
@app.route('/save_note', methods=['POST'])
def save_note():
    if 'username' not in session:
        return redirect(url_for('login'))

    note_content = request.form.get('note_content', '').strip()
    conn, cursor = get_db_cursor()

    cursor.execute("SELECT id FROM user_notes WHERE username = ?", (session['username'],))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE user_notes SET note = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?", (note_content, session['username']))
    else:
        cursor.execute("INSERT INTO user_notes (username, note) VALUES (?, ?)", (session['username'], note_content))

    conn.commit()
    conn.close()
    return redirect(url_for('upload'))

# Books recommendation page
@app.route('/recommended-books')
def recommended_books():
    return render_template('recommended_books.html')

# Initialize database when app starts
if __name__ == '__main__':
    init_db()
    port = 5002
    print("=" * 50)
    print("Skill Gap Analyzer is starting...")
    print(f"Access the application at: http://127.0.0.1:{port}")
    print("=" * 50)
    app.run(debug=True, port=port)
