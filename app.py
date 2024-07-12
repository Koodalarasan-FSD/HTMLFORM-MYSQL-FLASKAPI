from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

"""
 I installed all packages(pip install flask mysql-connector) inside these project folder and so 
don't need env folder to run these project
"""

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="html-db-flaskapi"
    )
    return conn

# Route to display form and users
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle form submission and store data
@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# API endpoint to retrieve users
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# API endpoint to update a user
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    name = data['name']
    email = data['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User Updated successfully'})

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
