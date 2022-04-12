from flask import Flask
import datetime

app = Flask(__name__)


@app.route('/api/time')
def home():
    return {'time': datetime.datetime.today()}


if __name__ == '__main__':
    app.run(debug=True)
