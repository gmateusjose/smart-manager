from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    # Define a main route for the application    
    return render_template('index.html')


@app.route('/professors', methods=['GET', 'POST'])
def professors():
    # Define a route to deal with professors
    if request.method == 'POST':
        return render_template('professors.html')
    else:
        return render_template('professors.html')
