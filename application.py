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

        # Verify if the form is a adding one
        if 'add-field' in request.form.keys():
            student = request.form.get('add-field').lower().strip()
            c.execute('''SELECT id FROM professors WHERE name = ?
                ''', (request.form.get('teacher').lower().strip(),))
            teacher_id = c.fetchone()[0]
            monthly = float(request.form.get('value'))
            scholar = False

            # decide if the student is a scholar
            if 'scholar' in request.form.keys():
                scholar = True
            
            c.execute('''
                INSERT INTO students (name, teacher_id, monthly, scholar)
                VALUES (?, ?, ?, ?)
                ''', (student, teacher_id, monthly, scholar))
        
        conn.commit()
        conn.close()
        return redirect('/students')
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())
        
        professors = [row[0].title() for row in c.execute('''SELECT name FROM
            professors''')]
        
        students = []

        for row in c.execute('''SELECT * FROM students ORDER BY name'''):
            student = {
                'id': row[0],
                'name': row[1].title(),
                'teacher': row[2],
                'payment': '${:,.2f}'.format(row[3]),
                'scholar': ''
            }
            # Add the scholar value
            if row[4] == 1:
                student['scholar'] = 'scholar'

            # Append the student to list
            students.append(student)
        
        # Get all the professors name for each student
        for student in students:
            c.execute('''SELECT name FROM professors WHERE id = ?''', (student['teacher'],))
            student['teacher'] = c.fetchone()[0].title()

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
