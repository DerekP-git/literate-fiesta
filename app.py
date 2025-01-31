from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory database for registrants
registrants = []

# List of available sports
sports = ["Dodgeball", "Flag Football", "Soccer", "Volleyball", "Ultimate Frisbee"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        sport = request.form['sport']
        registrants.append({'name': name, 'sport': sport})
        return redirect(url_for('registrants_list'))
    return render_template('register.html', sports=sports)

@app.route('/registrants')
def registrants_list():
    return render_template('registrants.html', registrants=registrants)

if __name__ == '__main__':
    app.run(debug=True)
