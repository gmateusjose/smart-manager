import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Define a main route for the application
    if request.method == 'POST':
        year = request.form.get('year')
        month = request.form.get('month')

        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())
        
        c.execute('''SELECT month FROM payments GROUP BY month''')
        months = [row[0] for row in c.fetchall()]

        c.execute('''SELECT year FROM payments GROUP BY year''')
        years = [row[0] for row in c.fetchall()]

        c.execute('''SELECT name, id FROM professors ''')
        professors = []
        
        for row in c.fetchall():
            professor = {
                'name': row[0].title(),
                'data': [],
                'items': 0,
                'results': [],
                'total': 0
            }

            c.execute('''SELECT name, monthly, scholar FROM payments
                JOIN students ON payments.student_id = students.id
                WHERE (month = ? AND year = ?) AND students.teacher_id = ?
                ''', (month, year, int(row[1])))

            # Fetch all the professor data     
            for row in c.fetchall():
                if int(row[2]) == 1: 
                    data = (row[0].title(), float(row[1]), 'scholar')
                else:
                    data = (row[0].title(), float(row[1]), '')
                
                professor['data'].append(data)
                professor['items'] += 1

            professors.append(professor)

            # Compute all the expenses
            expenses = {}
            c.execute('''SELECT description, value FROM expenses''')
            for row in c.fetchall():
                expenses[row[0]] = float(row[1])
            
            for professor in professors:
                c.execute('''SELECT SUM(value) FROM expenses''')
                total_expenses = c.fetchall()[0][0]
                professor['results'] = [(row[1] - total_expenses)/2 for row in professor['data']]
                professor['total'] = sum(professor['results'])
            
        return render_template('index.html', years=years, months=months, \
            professors=professors, expenses=expenses, zip=zip)
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())
        
        c.execute('''SELECT month FROM payments GROUP BY month''')
        months = [row[0] for row in c.fetchall()]

        c.execute('''SELECT year FROM payments GROUP BY year''')
        years = [row[0] for row in c.fetchall()]

        return render_template('index.html', years=years, months=months)


@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    # Define a route to deal with expenses
    if request.method == 'POST':
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())
        
        for item in request.form.keys():
            try:
                c.execute('''INSERT INTO expenses (description, value) VALUES
                (?, ?)''', (item, float(request.form.get(item))))
            except:
                c.execute('''UPDATE expenses SET value = ? WHERE description =
                ?''', (float(request.form.get(item)), item))
        
        conn.commit()
        conn.close()
        return render_template('expenses.html')
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())
        c.execute('''SELECT * FROM expenses''')
        
        expenses = {}
        for row in c.fetchall():
            expenses[row[0]] = float(row[1])
        
        conn.close()
        return render_template('expenses.html', expenses=expenses)


@app.route('/payments', methods=['GET', 'POST'])
def payments():
    # Define a route to deal with payments
    if request.method == 'POST':
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())

        student_name = request.form.get('student').lower().strip()
        c.execute('''SELECT id, teacher_id FROM students WHERE name = ?''', \
            (student_name,))

        identifiers = c.fetchone()
        month = int(request.form.get('month')) 
        year = int(request.form.get('year'))

        c.execute('''
            INSERT INTO payments (student_id, teacher_id, month, year) VALUES
            (?, ?, ?, ?)
        ''', (identifiers[0], identifiers[1], month, year))
        
        conn.commit()
        conn.close()
        return redirect('/payments')
    else:
        conn = sqlite3.connect('smart-fluent.db')
        c = conn.cursor()
        c.executescript(open('queries/create_tables.sql').read())

        students = []
        for row in c.execute('''SELECT name, monthly FROM students'''):
            student = {'name': row[0].title(), 'value': row[1]}
            students.append(student)

        payments = []
        c.execute('''SELECT date_payment, name, monthly, month, year FROM
        students JOIN payments ON students.id = payments.student_id''')
        
        for row in c.fetchall():
            payment = {
                'datetime': row[0],
                'student': row[1].title(),
                'value': '${:,.2f}'.format(row[2]),
                'month': f"{row[4]}-{int(row[3]):02}"
            }
            payments.append(payment)

        conn.close()
        return render_template('payments.html', students=students, \
            payments=payments)


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
        
        # Verify if a form to delete
        elif 'rem-button' in request.form.keys():
            student_name = request.form.get('search-student').lower().strip()
            c.execute('''
                DELETE FROM students WHERE name = ?
                ''', (student_name,))
        
        # Verify if is a form to update some data
        else:
            pass

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
