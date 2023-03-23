import os
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

DATABASE = 'database.db'

# --------------テーブル全削除のときのみ使用-------------
'''con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute("DROP table games")'''
# ----------------------------------------------------

con = sqlite3.connect(DATABASE)
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS games (id int PRIMARY KEY, date date, name text, right_left text, contents mediumblob)")


@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS games (id int PRIMARY KEY, day text, name text, right_left text, contents mediumblob)")
    db_games = cur.execute('SELECT * FROM games ORDER BY id DESC').fetchall()
    games = []
    for row in db_games:
        games.append(
            {'id': row[0], 'day': row[1], 'name': row[2], 'right_left': row[3], 'contents': row[4]})
    con.commit()
    con.close()

    return render_template(
        'index.html',
        games=games
    )


@app.route('/sear', methods=['post'])
def sear():
    date = request.form['date']
    search = request.form['search']
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS games (id int PRIMARY KEY, day text, name text, right_left text, contents mediumblob)")
    print(date, len(date))
    print(search, len(search))
    print("a")
    if len(date) == 0 and len(search) == 0:
        search_games = cur.execute('SELECT * FROM games ORDER BY id DESC').fetchall()
    elif len(date) != 0 and len(search) == 0:
        search_games = cur.execute("SELECT * from games where date = (?) ORDER BY id DESC",
                                   [date]).fetchall()
    elif len(date) == 0 and len(search) != 0:
        search_games = cur.execute(
            "SELECT * from games where name = (?) or right_left = (?) ORDER BY id DESC",
            [search, search]).fetchall()
    else:
        search_games = cur.execute(
            "SELECT * from games where date = (?) and (name = (?) or right_left = (?)) ORDER BY id DESC",
            [date, search, search]).fetchall()
    games = []
    for row in search_games:
        games.append(
            {'id': row[0], 'day': row[1], 'name': row[2], 'right_left': row[3], 'contents': row[4]})
    con.commit()
    con.close()
    return render_template(
        'index.html',
        games=games
    )


@app.route('/send', methods=['post', 'get'])
def send():
    num = request.form['id']
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * from games where id = (?)",
                [num])
    file_name = cur.fetchall()[0][4]

    # -------------データ分析の記述--------------------
    df = pd.read_csv(file_name)
    B = 0
    F = 0
    for row in df['02_RV_01']:
        if row == "B":
            B += 1
        elif row == "F":
            F += 1
    fig = plt.figure()
    labels = ['B', 'F']
    values = [B, F]
    lefts = np.arange(len(values))
    plt.bar(lefts, values, tick_label=labels, width=0.5, color="#b2b2b2")
    dirname = "flaskr/static/images/"
    os.makedirs(dirname, exist_ok=True)
    filename = dirname + "plot.png"
    fig.savefig(filename)

    # ----------------ここまでデータ分析の記述/それぞれ画像ファイルに保存-------------
    con.close()
    return render_template('display.html')


@app.route('/form')
def form():
    return render_template(
        'form.html'
    )


@app.route('/display')
def display():
    return render_template(
        'display.html'
    )


@app.route('/register', methods=['post', 'get'])
def register():
    date = request.form['date']
    name = request.form['name']
    right_left = request.form['right_left']
    contents = request.files.getlist('contents')

    if contents:
        for file in contents:
            fileName = file.filename
            file.save(fileName)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    sql = "SELECT count(*) FROM games"
    cur.execute(sql)
    id = cur.fetchall()[0][0]
    if id != 0:
        sql = "SELECT max(id) from games"
        cur.execute(sql)
        id = cur.fetchall()[0][0] + 1
    else:
        id += 1
    cur.execute('INSERT INTO games VALUES(?,?,?,?,?)',
                [id, date, name, right_left, fileName])
    con.commit()
    con.close()
    return redirect(url_for('index'))


@app.route('/delete')
def delete():
    return render_template(
        'delete.html'
    )


@app.route('/dele', methods=['post'])
def dele():
    number = int(request.form['id'])
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("DELETE from games where id = (?)",
                [number])
    con.commit()
    con.close()
    return redirect(url_for('index'))
