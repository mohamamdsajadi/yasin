import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = 'database.sqlite'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all')
def all_():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM infos')
    infos = cur.fetchall()
    conn.close()
    return render_template('amar.html', informations=infos)


@app.route('/add', methods=['POST'])
def add():
    req_dict: dict = request.form
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO infos (phone_number,problem,tools,name,customer_name) VALUES (?,?,?,?,?)',
                (
                req_dict.get('phonenumber'),
                 req_dict.get('problem'),
                 req_dict.get('tools'),
                 req_dict.get('name'),
                 req_dict.get('customer_name'),))
    conn.commit()
    conn.close()
    return redirect(url_for('all_'))


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
