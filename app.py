from flask import Flask, render_template, redirect, url_for, request, flash
from LoginUser import LoginUser
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import pymysql
from pymysql.cursors import DictCursor
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdsnfioIFDnDOFHODhfsdfhOFDfF(d6f7^&&DF6s7f79S&D*'
login_manager = LoginManager(app)
login_manager.login_view = 'index'

conn = None
cursor = None

@app.before_request
def conn():
    global conn
    global cursor
    conn = pymysql.connect(
    host='91.239.233.38',
    user='fmewmhwr_test',
    password='6qSxJiLVe*z!',
    db='fmewmhwr_test',
    cursorclass=DictCursor
    )
    cursor = conn.cursor()


@login_manager.user_loader
def load_user(user_id):
    return LoginUser().fromDB(user_id, cursor)


@app.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        email = request.form['inputEmail']
        user = is_user(email)
        if user:
            mail_send(user['email'],user['link'])
        else:
            rem = is_hash()
            mail_send(email, rem)
            hash_remember(email, rem)
        flash('Check your email!')
    return render_template('index.html')

@app.route('/login')
@login_required
def login():
    return render_template('login.html', email=current_user.get_email(), count = current_user.get_count())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/<string:hash>')
def req(hash):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        cursor.execute('SELECT * FROM users WHERE link=%s', hash)
        res = cursor.fetchone()
        if res:
            userlogin = LoginUser().create(res)
            login_user(userlogin)
            count = res['count']
            email = res['email']
            cursor.execute('UPDATE users SET count = %s WHERE email = %s', (count+1, email))
            conn.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('index'))

def mail_send(rec, link):
    addr_from = "testfor123cv@gmail.com"
    password = "vehrf2010"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = rec
    msg['Subject'] = 'Magic Link'

    body = f"Your magic link - https://web-teach-main.herokuapp.com/{link}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()

def hash_gen():
    let = ''
    for x in range(6):
         let = let + random.choice(string.ascii_letters)
    return let

def is_user(email):
    cursor.execute('SELECT * FROM users WHERE email=%s', email)
    user = cursor.fetchone()
    if user:
        return user
    else:
        return False

def is_hash():
    while True:
        link = hash_gen()
        cursor.execute('SELECT * FROM users WHERE link=%s', link)
        res = cursor.fetchone()
        if res:
            link = hash_gen()
        else:
            break
    return link

def hash_remember(email, hash):
    cursor.execute('INSERT INTO users(email, link) VALUES (%s,%s)', (email, hash))
    conn.commit()

if __name__ == '__main__':
    app.run(debug=True)
