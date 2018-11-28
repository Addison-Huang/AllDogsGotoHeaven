from util import db_updater as update
from flask import Flask,render_template,request,session,url_for,redirect,flash
from os import urandom

import sqlite3 #imports sqlite
DB_FILE="data/quackamoo.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor() #facilitates db operations

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('auth.html')

@app.route("/auth",methods=['GET','POST'])
def authPage():
    DB_FILE="data/AllDogsGoToHeaven.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    username=request.form['username']
    command = 'SELECT password FROM users WHERE users.username = "{0}"'.format(username)
    c.execute(command)
    password = c.fetchone()
    print(password[0])
    if password == []:
        flash('incorrect credentials')
        return redirect(url_for('home'))
    elif request.form['password'] == password[0]:
        session['username'] = username
        return render_template('home.html', Name = username)
    else:
        flash('incorrect credentials')
        return redirect(url_for('home'))

@app.route("/reg",methods=['GET','POST'])
def reg():
     return render_template('reg.html')

@app.route("/added",methods=['GET','POST'])
def added():
    DB_FILE="data/AllDogsGoToHeaven.db"
    newUsername = request.form['username']
    newPassword = request.form['password']
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()
    command = 'SELECT username FROM users;'
    c.execute(command)
    userList = c.fetchall()
    print(userList)
    if newUsername not in userList:
        insert = "INSERT INTO users VALUES(?,?,?)"
        params=(newUsername,newPassword,0)
        c.execute(insert,params)
        db.commit()
        db.close()
        #session['username'] = newUsername
        return redirect(url_for('home'))
    else:
        flash('Username Taken')
        return redirect(url_for('home'))

@app.route('/categories')
def startGame():
    url = "http://jservice.io/api/clues?value="
    urlList = []
    dataList = []
    for i in range(1,11):
        urlList.append(urllib.request.urlopen(url + str(i * 100)))
        dataList.append(json.loads(urlList[i-1].read()))
    del dataList[6]
    del dataList[8]
    for i in range(7):
        print(dataList[i][0]['question'])
    return render_template('categories.html')

@app.route('/play')
def play():
    '''
    jservice API
    '''
    url = urllib.request.urlopen("http://jservice.io/api/random")
    data = json.loads(url.read())
    print(data)

    return render_template('question.html', question = data[0]['question'], category = data[0]['category']['title'])

@app.route('/search')
def search_results():
    return 

if __name__ == '__main__':
    app.debug = True
    app.run()
