from flask import Flask, json, request
import datetime

app = Flask(__name__)

METRICS_MAP = {
    'bleu': 'BLEU',
    'gleu': 'GLEU',
    'chrf': 'Character n-gram F-score',
    'nist': 'NIST',
    'meteor': 'METEOR',
    'rouge': 'ROUGE'
}


@app.route('/api/time')
def time():
    return {'time': datetime.datetime.today()}


@app.route('/api/available-metrics')
def available_gram_metrics():
    return json.dumps(METRICS_MAP)


if __name__ == '__main__':
    app.run(debug=True)
