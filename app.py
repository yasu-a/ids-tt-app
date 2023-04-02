from flask import *
from main import main

app = Flask(__name__)
app.register_blueprint(main, url_prefix='/main')


@app.route('/')
def hello():
    return redirect(url_for('main.index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
