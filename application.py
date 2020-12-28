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
        print(request.form.keys())
        # Deciding if the form will add or will delete
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor() 
    
        # Creating all the pertinent tables
        c.executescript(open('queries/create_tables.sql').read())
        professor = (request.form.get('add-field'),)
        
        c.execute('''INSERT INTO professors (name) VALUES (?)''', professor)
        conn.commit()
        conn.close()
        return redirect('/professors')
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor() 
    
        # Creating the professors table
        c.executescript(open('queries/create_tables.sql').read()) 
        
        professors = [row[0] for row in c.execute('''SELECT name FROM professors''')]
        conn.close()
        return render_template('professors.html', professors=professors)
