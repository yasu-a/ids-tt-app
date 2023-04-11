import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import render_template, request, redirect, url_for

import models

from . import main


@main.route('/')
def index():
    return render_template(
        'main/index.html'
    )


@main.route('/sear', methods=['post'])
def sear():
    # date = request.form['date']
    # search = request.form['search']
    # if len(date) == 0 and len(search) == 0:
    #     search_games = cur.execute('SELECT * FROM games ORDER BY id DESC').fetchall()
    # elif len(date) != 0 and len(search) == 0:
    #     search_games = cur.execute("SELECT * from games where date = (?) ORDER BY id DESC",
    #                                [date]).fetchall()
    # elif len(date) == 0 and len(search) != 0:
    #     search_games = cur.execute(
    #         "SELECT * from games where name = (?) or right_left = (?) ORDER BY id DESC",
    #         [search, search]).fetchall()
    # else:
    #     search_games = cur.execute(
    #         "SELECT * from games where date = (?) and (name = (?) or right_left = (?)) ORDER BY id DESC",
    #         [date, search, search]).fetchall()
    # games = []
    # for row in search_games:
    #     games.append(
    #         {'id': row[0], 'day': row[1], 'name': row[2], 'right_left': row[3], 'contents': row[4]})
    # con.commit()
    # con.close()
    # return render_template(
    #     'index.html',
    #     games=games
    # )
    return render_template(
        'main/index.html',
        games=[]
    )


@main.route('/send', methods=['post', 'get'])
def send():
    game_id = request.form['id']
    file_name = models.Game.query.filter(models.Game.id == game_id).first()[4]

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
    return render_template('main/display.html')


@main.route('/form')
def form():
    return render_template(
        'main/form.html'
    )


@main.route('/display')
def display():
    return render_template(
        'main/display.html'
    )


@main.route('/register', methods=['post', 'get'])
def register():
    date = request.form['date']
    name = request.form['name']
    right_left = request.form['right_left']
    content = request.files.getlist('content')

    if content:
        for file in content:
            fileName = file.filename
            file.save(fileName)

    print(date, name, right_left, content)

    game = models.Game(
        date=date,
        name=name,
        right_left=right_left,
        content=content
    )
    models.db.session.add(game)
    models.db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/delete')
def delete():
    return render_template(
        'main/delete.html'
    )


@main.route('/dele', methods=['post'])
def dele():
    game_id = int(request.form['id'])

    game = models.Game.query.filter(models.Game.id == game_id)
    models.db.session.delete(game)
    models.db.session.commit()

    return redirect(url_for('main.index'))
