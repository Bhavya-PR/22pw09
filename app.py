from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

@app.route('/add_user_into_db', methods=['POST'])
def add_user_into_db():
    if request.method == 'POST':
        car_number = request.form['carno']
        name = request.form['username']
        email_address = request.form['email']
        user_password = request.form['password']
        balance = request.form['amount']
        conn = sqlite3.connect('datbase/toll_management.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (carno, email, password, name, balance) VALUES (?, ?, ?, ?, ?)", (car_number, email_address, user_password, name, balance))
        conn.commit()
        conn.close()
        return render_template('result.html', msg="Registered successfully")

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login_detail", methods=["POST"])
def login_detail():
    if request.method == 'POST':
        user_email = request.form['username']
        user_pass = request.form['password']
        conn = sqlite3.connect('datbase/toll_management.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (user_email, user_pass))
        record = cur.fetchone()
        conn.close()
        if record:
            return render_template('user_data.html', data=record)
        return render_template('result.html', msg="Invalid username or password")

@app.route("/system")
def system():
    return render_template('password.html')

@app.route("/system_pwd_check_valid", methods=["POST"])
def password_valid():
    if request.method == 'POST':
        system_pass = request.form['password']
        if system_pass == "system@123":
            return render_template('system_input.html')
        return render_template('result.html', msg="Invalid password")

@app.route("/system_detail", methods=["POST"])
def system_detail():
    if request.method == 'POST':
        car_number = request.form['carno']
        toll_amount = request.form['amount']
        toll_date = request.form['date']
        conn = sqlite3.connect('datbase/toll_management.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE carno=?", (car_number,))
        user_data = cur.fetchone()
        if user_data:
            updated_balance = user_data[4] - int(toll_amount)
            cur.execute("INSERT INTO transactions (carno, amount, date) VALUES (?, ?, ?)", (car_number, toll_amount, toll_date))
            cur.execute("UPDATE users SET balance=? WHERE carno=?", (updated_balance, car_number))
            conn.commit()
            conn.close()
            return render_template('result.html', msg="Toll crossed successfully")
        conn.close()
        return render_template('result.html', msg="Invalid car number")

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/admin_detail", methods=["POST"])
def admin_detail():
    if request.method == 'POST':
        admin_pass = request.form['password']
        if admin_pass == "owner@123":
            conn = sqlite3.connect('datbase/toll_management.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM transactions")
            transaction_records = cur.fetchall()
            conn.close()
            return render_template('data_admin.html', data=transaction_records)
        return render_template('result.html', msg="Invalid password")

@app.route("/print")
def user_detail():
    conn = sqlite3.connect('datbase/toll_management.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    user_records = cur.fetchall()
    conn.close()
    return render_template('user_detail.html', data=user_records)

if __name__ == '__main__':
    app.run(debug=True)
