from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    # Define a main route for the application    
    return render_template('index.html')


@app.route('/professors')
def professors():
    # Define a route to deal with professors
    return render_template('professors.html')
