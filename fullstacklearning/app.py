from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create Database Table
def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bowl_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            condition TEXT NOT NULL,
            bowl_note TEXT NOT NULL,
            rating INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/diet')
def diet():
    return render_template('diet.html')


@app.route('/reviews')
def reviews():
    return render_template('reviews.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


@app.route('/submit_review', methods=['POST'])
def submit_review():

    name = request.form['name']
    rating = request.form['rating']
    review = request.form['review']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reviews(name,rating,review) VALUES(?,?,?)",
        (name, rating, review)
    )

    conn.commit()
    conn.close()

    return "<h2>Review Submitted Successfully!</h2><a href='/'>Go Home</a>"


@app.route('/submit_bowl_review', methods=['POST'])
def submit_bowl_review():
    name = request.form['name']
    condition = request.form['condition']
    bowl_note = request.form['bowl_note']
    rating = request.form['rating']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bowl_reviews(name,condition,bowl_note,rating) VALUES(?,?,?,?)",
        (name, condition, bowl_note, rating)
    )

    conn.commit()
    conn.close()

    return "<h2>Bowl Review Submitted Successfully!</h2><a href='/diet'>Back to Diet Tracker</a>"


@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts(name,email,message) VALUES(?,?,?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return "<h2>Message Sent Successfully!</h2><a href='/'>Go Home</a>"


@app.route('/view')
def view():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()

    conn.close()

    html = """
    <h2>Contact Messages</h2>
    <table border='1' cellpadding='10'>
    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Email</th>
    <th>Message</th>
    </tr>
    """

    for row in data:
        html += f"""
        <tr>
        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>
        </tr>
        """

    html += "</table>"

    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)