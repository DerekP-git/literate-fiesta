# Copyright 2015 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
from flask import Flask


app = Flask(__name__)

# Database setup (using SQLite)
def create_table():
    conn = sqlite3.connect('intramural.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sport TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

SPORTS = ["Dodgeball", "Flag Football", "Soccer", "Volleyball", "Ultimate Frisbee"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        sport = request.form.get("sport")

        if not name or not sport:
            return render_template("register.html", sports=SPORTS, error="Please fill in all fields.")

        conn = sqlite3.connect('intramural.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO registrants (name, sport) VALUES (?, ?)", (name, sport))
            conn.commit()
            return redirect(url_for('registrants'))
        except sqlite3.Error as e:
            return render_template("register.html", sports=SPORTS, error=f"Database error: {e}")
        finally:
            conn.close()

    return render_template("register.html", sports=SPORTS, error=None)

@app.route("/registrants")
def registrants():
    conn = sqlite3.connect('intramural.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, sport FROM registrants")
    registrants = cursor.fetchall()
    conn.close()
    return render_template("registrants.html", registrants=registrants)

if __name__ == "__main__":
    app.run(debug=True)
