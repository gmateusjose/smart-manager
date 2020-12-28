import sqlite3

from flask import Flask, render_template, request, redirect


app = Flask(__name__)


@app.route('/')
def index():
    # Define a main route for the application    
    return render_template('index.html')


@app.route('/students', methods=['GET', 'POST'])
def students():
    # Define a route to deal with students
    if request.method == 'POST':
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())
        print(request.form)
        if 'add-field' in request.form.keys():
            student = request.form.get('add-field').lower().strip()
            teacher_id = c.execute('''
                SELECT id FROM professors WHERE name = ? 
                ''', (request.form.get('teacher').lower().strip(),))
            monthly = float(request.form.get('value'))

            # decide if the student is a scholar
            if 'scholar' in request.form.keys():
                c.execute('''
                    INSERT INTO students (name, teacher_id, monthly, scholar)
                    VALUES (?, ?, ?, TRUE)
                    ''', (student, teacher_id, monthly))
            else:
                c.execute('''
                    INSERT INTO students (name, teacher_id, monthly) 
                    VALUES (?, ?, ?)
                    ''', student, teacher_id, monthly)

        conn.commit()
        conn.close()
        return redirect('/students')
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())
        
        professors = [row[0].title() for row in c.execute('''SELECT name FROM
            professors''')]

        c.execute('''SELECT * FROM students''')
        students = c.fetchall()
        
        conn.close()
        return render_template('students.html', professors=professors, \
            students=students)


@app.route('/professors', methods=['GET', 'POST'])
def professors():
    # Define a route to deal with professors
    if request.method == 'POST':
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())

        if 'rem-field' in request.form.keys():
            professor = (request.form.get('rem-field').lower().strip(),)
            c.execute('''DELETE FROM professors WHERE name = ? ''', professor)
        else:
            professor = (request.form.get('add-field').lower().strip(),)
            try:
                c.execute('''INSERT INTO professors (name) VALUES (?)''', professor)
            except:
                error_msg = "There's already a professor with the same name"
                professors = [row[0].title() for row in c.execute('''SELECT \
                    name FROM professors''')]
                return render_template('professors.html', \
                    professors=professors, error_msg=error_msg)

        conn.commit()
        conn.close()
        return redirect('/professors')
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor() 
        c.executescript(open('queries/create_tables.sql').read()) 
        professors = [row[0].title() for row in c.execute('''SELECT name FROM professors''')]
        conn.close()
        return render_template('professors.html', professors=professors)
