from flask import Flask

app = Flask(__name__)


@app.route('/api/user')
def home():
    return {'id': 2, 'name': 'Andrej'}


if __name__ == '__main__':
    app.run(debug=True)
