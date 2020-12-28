import sqlite3

from flask import Flask, render_template, request, redirect


app = Flask(__name__)


@app.route('/')
def index():
    # Define a main route for the application    
    return render_template('index.html')


@app.route('/professors', methods=['GET', 'POST'])
def professors():
    # Define a route to deal with professors
    if request.method == 'POST':
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor() 
    
        # Creating the professors table
        c.execute('''
        CREATE TABLE IF NOT EXISTS professors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );''') 
        professor = (request.form.get('add-field'),)
        
        print(professor)
        c.execute('''INSERT INTO professors (name) VALUES (?)''', professor)
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor() 
    
        # Creating the professors table
        c.execute('''
        CREATE TABLE IF NOT EXISTS professors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );''') 
        
        professors = [row[0] for row in c.execute('''SELECT name FROM professors''')]
        conn.close()
        return render_template('professors.html', professors=professors)
