from flask import *

from flask_login import login_required

from . import main

from models import db, Game

from models import db

import os
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import patches
from sqlalchemy import or_

@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/csv-entries')
def csv_entries():
    games = db.session.query(Game).all()
    return render_template(
        'main/csv_entries.html',
        entries=games,
        # mapping from <column key> to <display name of key>
        # currently just copy the keys to the display names
        keys=[(k, k) for k in ('date', 'name')]
    )


@main.route('/upload', methods=['GET'])
def upload():
    return render_template('main/upload.html')


@main.route('/upload', methods=['POST'])
def post_upload():
    contents = request.files.getlist('contents')

    if contents:
        for file in contents:
            file.save(file.name)


@main.route('/search')
def search():
    date = request.form['date']
    search = request.form['search']
    print(date, len(date))
    print(search, len(search))
    if len(date) == 0 and len(search) == 0:
        search_games = db.session.query(Game).order_by(db.desc(Game.id)).all()#('SELECT * FROM games ORDER BY id DESC').fetchall()
    elif len(date) != 0 and len(search) == 0:
        search_games = db.session.query(Game.date==date).order_by(db.desc(Game.id)).all()
        #cur.execute("SELECT * from games where date = (?) ORDER BY id DESC",
                                   #[date]).fetchall()
    elif len(date) == 0 and len(search) != 0:
        search_games = db.session.query(Game.name==search,Game.right_left==search).order_by(db.desc(Game.id)).all()#cur.execute(
            #"SELECT * from games where name = (?) or right_left = (?) ORDER BY id DESC",
            #[search, search]).fetchall()
    else:
        search_games = search_games = db.session.query(Game.date==date,or_(Game.name==search,Game.right_left==search)).order_by(db.desc(Game.id)).all()#cur.execute(
            #"SELECT * from games where date = (?) and (name = (?) or right_left = (?)) ORDER BY id DESC",
            #[date, search, search]).fetchall()
    games = []
    for row in search_games:
        games.append(
            {'id': row[0], 'day': row[1], 'name': row[2], 'right_left': row[3], 'contents': row[4]})
    #con.commit()
    #con.close()
    return render_template(
        'index.html',
        games=games
    )


@main.route('/send')
def send():
    num = request.form['id']
    #con = sqlite3.connect(DATABASE)
    #cur = con.cursor()
    search_games = db.session.query(Game.id==num)#cur.execute("SELECT * from games where id = (?)",
                #[num])
    file_name = search_games[0][4]

    # -------------データ分析の記述--------------------
    # -------------仮の分析---------------------------
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
    dirname = "static/images/"
    os.makedirs(dirname, exist_ok=True)
    filename = dirname + "plot.png"
    fig.savefig(filename)
    # ----------------仮の分析終わり-----------------------------------------------------
    # --------コース図--------------------------------------------------------------------
    F_f, FM_f, BM_f, B_f, FS_f, FMS_f, BMS_f, BS_f, F_s, FM_s, BM_s, B_s, FS_s, FMS_s, BMS_s, BS_s = map(
        int, [0] * 16)
    first = df['名前'][0]
    for row in df['名前']:
        if first != row:
            second = row
            break
    i = 0

    for row in df['01_SV_03']:
        if df['名前'][i] == first:
            if row == "F":
                F_f += 1
            elif row == "FM":
                FM_f += 1
            elif row == "BM":
                BM_f += 1
            elif row == "B":
                B_f += 1
            elif row == "FS":
                FS_f += 1
            elif row == "FMS":
                FMS_f += 1
            elif row == "BMS":
                BMS_f += 1
            elif row == "BS":
                BS_f += 1
        if df['名前'][i] == second:
            if row == "F":
                F_s += 1
            elif row == "FM":
                FM_s += 1
            elif row == "BM":
                BM_s += 1
            elif row == "B":
                B_s += 1
            elif row == "FS":
                FS_s += 1
            elif row == "FMS":
                FMS_s += 1
            elif row == "BMS":
                BMS_s += 1
            elif row == "BS":
                BS_s += 1
        i += 1
    print(F_f, FM_f, BM_f, B_f, FS_f, FMS_f, BMS_f, BS_f, F_s, FM_s, BM_s, B_s, FS_s, FMS_s, BMS_s,
          BS_s)
    # 画像のサイズ
    width = 600
    height = 400

    # 画像の作成
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 卓球台の描画
    draw.rectangle((50, 50, 550, 350), outline="green", width=3)
    draw.line((300, 50, 300, 350), fill="green", width=3)
    draw.line((50, 200, 550, 200), fill="green", width=3)
    draw.line((50, 50, 550, 50), fill="green", width=3)
    draw.line((50, 350, 550, 350), fill="green", width=3)
    draw.line((170, 50, 170, 350), fill="green", width=3)
    draw.line((420, 50, 420, 350), fill="green", width=3)

    # 点の描写
    for i in range(F_f):
        x = random.randint(60, 160)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(FM_f):
        x = random.randint(170, 290)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(BM_f):
        x = random.randint(310, 410)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(B_f):
        x = random.randint(430, 530)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(FS_f):
        x = random.randint(60, 160)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(FMS_f):
        x = random.randint(170, 290)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(BMS_f):
        x = random.randint(310, 410)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(BS_f):
        x = random.randint(430, 530)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    # フォントの設定
    font_path = "arial.ttf"  # フォントファイルのパス
    font_size = 40  # フォントサイズ
    font = ImageFont.truetype(font_path, font_size)

    # 文字列の描画
    text = first
    text_width, text_height = draw.textsize(text, font=font)
    x = 0
    y = 5
    draw.text((x, y), text, font=font, fill="black")

    filename = dirname + "plot1.png"
    image.save(filename)

    # 相手
    # 画像のサイズ
    width = 600
    height = 400

    # 画像の作成
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 卓球台の描画
    draw.rectangle((50, 50, 550, 350), outline="green", width=3)
    draw.line((300, 50, 300, 350), fill="green", width=3)
    draw.line((50, 200, 550, 200), fill="green", width=3)
    draw.line((50, 50, 550, 50), fill="green", width=3)
    draw.line((50, 350, 550, 350), fill="green", width=3)
    draw.line((170, 50, 170, 350), fill="green", width=3)
    draw.line((420, 50, 420, 350), fill="green", width=3)

    # 点の描写
    for i in range(F_s):
        x = random.randint(60, 160)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(FM_s):
        x = random.randint(170, 290)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(BM_s):
        x = random.randint(310, 410)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(B_s):
        x = random.randint(430, 530)
        y = random.randint(60, 190)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(FS_s):
        x = random.randint(60, 160)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(FMS_s):
        x = random.randint(170, 290)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(BMS_s):
        x = random.randint(310, 410)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    for i in range(BS_s):
        x = random.randint(430, 530)
        y = random.randint(210, 340)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="red")

    # フォントの設定
    font_path = "arial.ttf"  # フォントファイルのパス
    font_size = 40  # フォントサイズ
    font = ImageFont.truetype(font_path, font_size)

    # 文字列の描画
    text = second
    text_width, text_height = draw.textsize(text, font=font)
    x = 0
    y = 5
    draw.text((x, y), text, font=font, fill="black")

    filename = dirname + "plot2.png"
    image.save(filename)
    # ------コース図終わり---------------------------------------------------------
    # ----------------得点表------------------------------------------------------
    i = 0
    score1 = []
    score2 = []
    for i in range(len(df)):
        row = str(df['00_01_GameCount'][i])
        if row[0] == "n":
            break
        score1.append(int(row[0]))
        tmp = row[2:len(str(row))]
        score2.append(int(tmp))
        i += 1
    sum = i

    first_score = []
    second_score = []
    first_result = []
    second_result = []
    for i in range(sum):
        if i != 0 and (score1[i] > score1[i - 1] or score2[i] > score2[i - 1]):
            first_result.append(first_score)
            second_result.append(second_score)
            first_score = []
            second_score = []
            print("game_point")

        print(df['00_03_Point'][i], score1[i], score2[i])
        if df['00_03_Point'][i] == first:
            first_score.append(score1[i])
            second_score.append(-1)
        if df['00_03_Point'][i] == second:
            second_score.append(score2[i])
            first_score.append(-1)
    first_result.append(first_score)
    second_result.append(second_score)
    print(first_result)
    print(second_result)

    first_score_data = []
    second_score_data = []
    for i in range(len(first_result)):
        first_score_data.append({'名前': first, '得点': first_result[i]})
        first_score_data.append({'名前': second, '得点': second_result[i]})

    # 画像のサイズと背景色を設定する
    image_size = (700, 700)
    background_color = (255, 255, 255)

    # 画像を作成する
    img = Image.new('RGB', image_size, background_color)

    # 描画用のオブジェクトを作成する
    draw = ImageDraw.Draw(img)

    # フォントを指定する
    font = ImageFont.truetype('arial.ttf', 16)

    # データから表を描画する
    x = 50
    y = 50
    for d in first_score_data:
        name = d['名前']
        score = str(d['得点'])
        draw.text((x, y), name, font=font, fill=(0, 0, 0))
        draw.text((x + 150, y), score, font=font, fill=(0, 0, 0))
        y += 20
    for d in second_score_data:
        name = d['名前']
        score = str(d['得点'])
        draw.text((x, y), name, font=font, fill=(0, 0, 0))
        draw.text((x + 150, y), score, font=font, fill=(0, 0, 0))
        y += 20
    img.save('score_table.png')

    # ----------------ここまでデータ分析の記述/それぞれ画像ファイルに保存-------------
    con.close()
    return render_template('display.html')


@main.route('/form')
def form():
    return render_template(
        'form.html'
    )


@main.route('/delete')
def delete():
    return render_template(
        'delete.html'
    )

@main.route('/delete', methods=['post'])
def post_delete():
    number = int(request.form['id'])
    #con = sqlite3.connect(DATABASE)
    #cur = con.cursor()
    db.session.query(Game.id==number)#cur.execute("DELETE from games where id = (?)",
               # [number])
    #con.commit()
    #con.close()
    return redirect(url_for('index'))
