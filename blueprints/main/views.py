from flask import *

from flask_login import login_required

from . import main

from models import db, Game


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
    pass


@main.route('send')
def send():
    pass


@main.route('/form')
def form():
    pass


@main.route('delete')
def delete():
    pass
